from tqdm import tqdm
import sacrebleu
import re
from nltk.translate.meteor_score import single_meteor_score
from transformers import AutoTokenizer
import os


tokenizer = AutoTokenizer.from_pretrained("/public/home/yangzhen/Data_Contamination/pretrain_model/roberta-base")
rootpath="/public/home/yangzhen/Data_Contamination/pretrain_model/2summarization"


def remove_index_prefix(line):
    return ' '.join(line.strip().split()[1:])

def compute_bleu(reference, hypothesis):
    ref_tokens = [t.lower() for t in tokenizer.tokenize(reference)]
    hyp_tokens = [t.lower() for t in tokenizer.tokenize(hypothesis)]
    bleu = sacrebleu.sentence_bleu(" ".join(hyp_tokens), [" ".join(ref_tokens)])
    return bleu.score

def normalize_code(text):
    text = re.sub(r'//.*?$|/\*.*?\*/', '', text, flags=re.MULTILINE | re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def is_exact_match(reference, hypothesis):
    return normalize_code(reference) == normalize_code(hypothesis)

def compute_meteor(reference, hypothesis):
    ref_tokens = [t.lower() for t in tokenizer.tokenize(reference)]
    hyp_tokens = [t.lower() for t in tokenizer.tokenize(hypothesis)]
    return single_meteor_score(ref_tokens, hyp_tokens)


# gold_file =os.path.join(rootpath,"/public/home/yangzhen/Data_Contamination/pretrain_model/1translate/allpolu_upper/turn5/2out_sub1/test_1.gold")   
# output_file =os.path.join(rootpath,"/public/home/yangzhen/Data_Contamination/pretrain_model/1translate/allpolu_upper/turn5/2out_sub1/test_1.output")   


# # 用于 CodeBLEU
# ref_file = os.path.join(rootpath,f"allpolu_upper/ref.txt")   
# pred_file = os.path.join(rootpath,f"allpolu_upper/pred.txt")  

# refs, preds = [], []
# sum_bleu = 0
# exact_match_count = 0
# meteor_sum = 0
# with open(gold_file, "r", encoding="utf-8") as gf, open(output_file, "r", encoding="utf-8") as of:
#     gold_lines = [remove_index_prefix(line) for line in gf]
#     output_lines = [remove_index_prefix(line) for line in of]
#     for answer_code, output_code in tqdm(zip(gold_lines, output_lines), total=len(gold_lines), desc="Processing"):
#         bleu_score = compute_bleu(answer_code, output_code)
#         meteor_score = compute_meteor(answer_code, output_code)
#         sum_bleu += bleu_score
#         meteor_sum += meteor_score
#         if is_exact_match(answer_code, output_code):
#             exact_match_count += 1
#         refs.append(answer_code.strip().replace('\n', '\\n'))
#         preds.append(output_code.strip().replace('\n', '\\n'))
# with open(ref_file, "w", encoding="utf-8") as rf:
#     rf.write("\n".join(refs))
# with open(pred_file, "w", encoding="utf-8") as pf:
#     pf.write("\n".join(preds))
# total = len(refs)
# print()
# print("BLEU =", sum_bleu / total)
# print("Exact Match =", exact_match_count / total)
# print("METEOR =", meteor_sum / total)


# os.system(
#     f"python calc_code_bleu.py --refs {ref_file} --hyp {pred_file} "
#     f"--lang c_sharp --params 0.25,0.25,0.25,0.25"
# )
for type in ["4input_output_pair_ft"]:#"0roberta_only""1input_only","2output_only","3input_output","5input_output_pair_pre"
    for cnt in range(5):
        print("---------\n",f"{type}/turn{cnt+1}","\n---------")
        for partion_train in range(1,3):
            for partion_test in range(1,3):
                print("-------",f"withsub{partion_train}_sub{partion_test}","-------")
                gold_file =os.path.join(rootpath,f"{type}/turn{cnt+1}/withsub{partion_train}_sub{partion_test}/test_1.gold")   
                output_file =os.path.join(rootpath,f"{type}/turn{cnt+1}/withsub{partion_train}_sub{partion_test}/test_1.output")   
                # print("------",f"with_sub{partion_test}","-------")
                # gold_file =os.path.join(rootpath,f"{type}/turn{cnt+1}/with_sub{partion_test}/test_1.gold")   
                # output_file =os.path.join(rootpath,f"{type}/turn{cnt+1}/with_sub{partion_test}/test_1.output")   
                
                # 用于 CodeBLEU
                ref_file = os.path.join(rootpath,f"{type}/turn{cnt+1}/withsub{partion_train}_sub{partion_test}/ref.txt")   
                pred_file = os.path.join(rootpath,f"{type}/turn{cnt+1}/withsub{partion_train}_sub{partion_test}/pred.txt")  
                # ref_file = os.path.join(rootpath,f"{type}/turn{cnt+1}/with_sub{partion_test}/ref.txt")   
                # pred_file = os.path.join(rootpath,f"{type}/turn{cnt+1}/with_sub{partion_test}/pred.txt")   

                refs, preds = [], []
                sum_bleu = 0
                exact_match_count = 0
                meteor_sum = 0

                with open(gold_file, "r", encoding="utf-8") as gf, open(output_file, "r", encoding="utf-8") as of:
                    gold_lines = [remove_index_prefix(line) for line in gf]
                    output_lines = [remove_index_prefix(line) for line in of]

                    for answer_code, output_code in tqdm(zip(gold_lines, output_lines), total=len(gold_lines), desc="Processing"):
                        bleu_score = compute_bleu(answer_code, output_code)
                        meteor_score = compute_meteor(answer_code, output_code)
                        sum_bleu += bleu_score
                        meteor_sum += meteor_score
                        if is_exact_match(answer_code, output_code):
                            exact_match_count += 1

                        refs.append(answer_code.strip().replace('\n', '\\n'))
                        preds.append(output_code.strip().replace('\n', '\\n'))


                with open(ref_file, "w", encoding="utf-8") as rf:
                    rf.write("\n".join(refs))
                with open(pred_file, "w", encoding="utf-8") as pf:
                    pf.write("\n".join(preds))


                total = len(refs)
                print()
                print("BLEU =", sum_bleu / total)
                print("Exact Match =", exact_match_count / total)
                print("METEOR =", meteor_sum / total)


                os.system(
                    f"python calc_code_bleu.py --refs {ref_file} --hyp {pred_file} "
                    f"--lang c_sharp --params 0.25,0.25,0.25,0.25"
                )
