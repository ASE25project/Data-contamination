# Contamination Means Overestimation? A Comprehensive Empirical Study in Code Intelligence

## Experimental Procedure
![alt text](overview.png)

## Prompt
Here is the prompt we used for large language model inference, along with a one-shot example.

Code Translation:
```
Please translate the following Java function into equivalent C# code. End your answer with 'END OF CASE'.
Java:
private void injectBundleContext(BundleContext bundleContext) {
    this.bundleContext = bundleContext;
    this.resourceLoader = new OsgiBundleResourceLoader(bundleContext.getBundle());
}         
C#:
private void InjectBundleContext(BundleContext bundleContext) {
    this.bundleContext = bundleContext;
    this.resourceLoader = new OsgiBundleResourceLoader(bundleContext.getBundle());
}
END OF CASE
Java:
{entry['Java_function']}
C#:
```

Code Summarization:
```
Please summarize the following Java function. End your answer with 'END OF CASE'.
Function:
private void injectBundleContext(BundleContext bundleContext) {
    this.bundleContext = bundleContext; this.resourceLoader = new OsgiBundleResourceLoader(bundleContext.getBundle());
}
Summary:
This Java function injects a `BundleContext` object, stores it, and initializes a `ResourceLoader` with the associated bundle.
END OF CASE
Function:
{entry['Function']}
Summary:
```

Code Generation:
```
Please implement the following Java function. End your answer with 'END OF CASE'.
Instruction:
Write a Java method that sets a `name` field to the provided parameter value.
Function:
public void setName(String name) {
    this.name = name;
}
END OF CASE
Instruction:
{entry['Instruction']}
Function:

```

## Complete Result

Please refer to the [result](./result.md) for the complete experimental results

## Pretrained Model
The Java data used for pretraining can be obtained from [CodeSearchNet](https://huggingface.co/datasets/code-search-net/code_search_net/blob/main/data/java.zip). The dataset for the code translation task is available at [CodeTrans](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/data), and the dataset for the code generation task can be found at [Concode](https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code/dataset/concode). For convenience, all datasets can also be found directly in the [dataset](./dataset) folder.


#### RoBERTa-base

Run `pretrain.sh` to perform model pretraining:
```shell
cd roberta/
bash pretrain.sh
```
Use the pretrained model for fine-tuning on downstream tasks and evaluate it on the test set:
```shell
bash run.sh
bash score.sh
```
Conduct further evaluation using eval_plm.py
```shell
python eval_plm.py
```


#### GPT2-small

For code_translation
Perform uncontaminated pre-training using pre-train-pure.py and modify `output_dir` to specify the model output location:
```shell
cd gpt2/code_translation
python pre-train-pure.py
```
Perform pre-training with unilateral contamination using pre-train-contaminated.py. Modify `pollution_file` and `pollution_type` to change the contamination mode (e.g., `test-java` represents contaminating the Java part of the test set):
```shell
python pre-train-contaminated.py
```
Perform pre-training with unpaired contamination using pre-train-contaminated-unpaired.py:
```shell
python pre-train-contaminated-unpaired.py
```
Perform pre-training with paired contamination using pre-train-contaminated-paired.py:
```shell
python pre-train-contaminated-paired.py
```

For Code Generation


## Large Language Model

### Data construction
The Java and C# data used in StarCoder's pretraining can be obtained from [bigcode/the-stack](https://huggingface.co/datasets/bigcode/the-stack), while the Java and C# data used in LLaMA's pretraining can be accessed via [bigquery](https://console.cloud.google.com/bigquery?ws=!1m4!1m3!3m2!1sbigquery-public-data!2sgithub_repos).


Collect a large number of Java function snippets, then manually select 100 samples.
```shell
python extract-java.py
```
Collect a large number of matched Java–C# function pairs, perform an initial filtering using BLEU scores, and then manually select 100 pairs.
```shell
python extract-paired.py
python cal-bleu.py
```
Collect a large number of paired NL-code examples, and then manually select those that are suitable for code generation tasks.
```shell
python extravt-paired.py
```

We have provided samples in the [dataset](./dataset)

### Infer

The large models used for inference are obtained from [Starcoder](https://huggingface.co/bigcode/starcoderbase) and [Llama](https://huggingface.co/alexl83/LLaMA-33B-HF). You can perform inference using `infer.py`; simply replace the prompt and the corresponding model as needed.
```shell
python infer.py
```
use eval_llm.py for evaluation
```shell
python eval_llm.py
```


