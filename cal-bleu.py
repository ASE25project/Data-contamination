import os
import json
import sacrebleu
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

output_file = "./matched_function.jsonl"

with open(output_file, "w", encoding="utf-8") as outfile:
    """
    You can decide how many matched function pairs to merge based on what you have obtained. To avoid oversized files, you can merge them in batches.
    """
    for i in range(1, 101): 
        file_name = f"./function_{i}.jsonl"
        if os.path.exists(file_name):  
            with open(file_name, "r", encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)  

input_file = output_file

output_files = {
    80: "./bleu_80.jsonl",
    70: "./bleu_70.jsonl",
    60: "./bleu_60.jsonl",
    50: "./bleu_50.jsonl",
}

def compute_bleu_line(line):
    try:
        data = json.loads(line)
        java_code = data["java_function"]
        csharp_code = data["csharp_function"]

        bleu = sacrebleu.sentence_bleu(csharp_code.lower(), [java_code.lower()]).score
        data["bleu_score"] = bleu
        return data

    except Exception as e:
        return None

def classify_bleu_score(data):
    score = data["bleu_score"]
    for threshold in [80, 70, 60, 50]:
        if score >= threshold:
            return threshold
    return None

def main():
    file_handles = {k: open(v, "w", encoding="utf-8") for k, v in output_files.items()}

    with ProcessPoolExecutor() as executor:
        futures = []
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                futures.append(executor.submit(compute_bleu_line, line))

            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
                data = future.result()
                if data:
                    threshold = classify_bleu_score(data)
                    if threshold:
                        json.dump(data, file_handles[threshold], ensure_ascii=False)
                        file_handles[threshold].write("\n")

    for f in file_handles.values():
        f.close()

    print("Done!")

if __name__ == "__main__":
    main()
