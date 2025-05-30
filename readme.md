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
{entry[‘Java_function’]}
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
{entry[‘Instruction']}
Function:

```

## Experimental results

The complete experimental results are as follows

### Model：Roberta-base   
#### Finetuning   
Task：Code Translation 

| BLEU/METEOR      | run1        | run2        | run3        | run4        | run5        |
| ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| w/o Contaminated | 86.22/89.18 | 85.98/88.76 | 86.13/89.02 | 86.14/89.07 | 86.09/88.96 |
| input-only       | 85.28/88.3  | 86.48/89.13 | 86.15/88.99 | 86.23/88.98 | 86.21/88.91 |
| output-only      | 85.61/89.23 | 86.36/89.08 | 86.11/89.03 | 86.61/89.14 | 86.75/89.35 |
| unpaired         | 86.16/88.65 | 86.26/89.08 | 86.35/89.15 | 86.45/89.26 | 85.88/89.31 |
| paired           | 86.35/89.11 | 86.09/88.84 | 85.89/88.72 | 86.19/88.91 | 86.37/89.09 |

Task：Code Generation
| BLEU/METEOR      | run1        | run2        | run3        | run4        | run5        |
| ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| w/o Contaminated | 41.19/51.75 | 40.08/50.83 | 41.04/51.76 | 40.74/51.56 | 40.83/51.43 |
| input-only       | 40.68/51.21 | 40.56/50.96 | 40.78/51.09 | 40.73/51.4  | 40.13/50.52 |
| output-only      | 41.65/52.02 | 41.96/52.26 | 41.28/51.61 | 39.2/50.03  | 41.24/51.51 |
| unpaired         | 40.74/51.8  | 40.18/51.68 | 41.44/51.84 | 41.5/51.92  | 41.06/51.45 |
| paired           | 41.65/51.96 | 40.71/51.2  | 40.73/51.23 | 40.27/50.67 | 40.93/51.58 |

### Model：GPT2-small
#### Finetuning
Task：Code Translation

| BLEU/METEOR      | run1        | run2        | run3        | run4        | run5        |
| ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| w/o Contaminated | 36.97/47.53 | 37.67/48.2  | 37.07/47.41 | 36.75/47.67 | 37.35/47.96 |
| input-only       | 38.04/48.57 | 37.95/48.6  | 37.79/48.28 | 36.68/47.41 | 37.14/47.78 |
| output-only      | 36.55/47.2  | 37.38/48.06 | 36.88/47.52 | 37.12/47.95 | 36.92/47.56 |
| unpaired         | 36.64/47.54 | 37.42/48    | 37.42/47.92 | 36.88/47.75 | 37.39/47.88 |
| paired           | 37.57/47.99 | 37.41/48.01 | 37.41/47.98 | 37.33/48    | 37.45/48.05 |


Task：Code Generation
| BLEU/METEOR      | run1        | run2        | run3        | run4        | run5        |
| ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| w/o Contaminated | 17.56/21.94 | 17.74/22.05 | 17.92/22.09 | 17.48/21.77 | 17.91/22.04 |
| input-only       | 17.6/22.6   | 18.16/22.01 | 18.23/22.51 | 17.71/21.82 | 18.27/22.4  |
| output-only      | 17.75/22.39 | 17.79/21.98 | 17.44/21.76 | 17.6/21.92  | 17.56/21.73 |
| unpaired         | 17.72/21.81 | 17.44/21.75 | 18.08/22.52 | 17.55/22.42 | 17.85/22.19 |
| paired           | 17.55/22.19 | 17.57/21.62 | 18.06/22.46 | 17.39/22.2  | 17.19/21.28 |

#### Direct Inference

Task: Code Translation
| BLEU/METEOR      | run1        | run2        | run3        | run4        | run5        |
| ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| w/o Contaminated | 17.71/25.92 | 17.9/29.75  | 17.52/29.36 | 17.85/29.48 | 17.8/29.77  |
| paired           | 23.1/36.46  | 23.01/36.34 | 22.42/35.7  | 22.57/35.85 | 21.25/34.44 |


Task: Code Generation
| BLEU/METEOR      | run1      | run2      | run3       | run4       | run5      |
| ---------------- | --------- | --------- | ---------- | ---------- | --------- |
| w/o Contaminated | 2.17/5.11 | 2.09/4.99 | 2.01/5.84  | 2.33/6.03  | 2.27/4.92 |
| paired           | 4.18/8.67 | 3.98/7.89 | 5.73/10.95 | 5.59/10.77 | 4.14/8.47 |


#### 500 samples Fintuning
Task: Code Translation
|         |                  | run1        | run2        | run3        | run4        | run5        |
| ------- | ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| epoch1  | w/o Contaminated | 15.34/27.25 | 14.44/26.13 | 14.75/25.84 | 15.12/26.67 | 14.84/26.58 |
|         | paired           | 20.65/33.81 | 21.85/35.02 | 20.48/33.76 | 20.75/34.1  | 19.91/32.44 |
| epoch5  | w/o Contaminated | 9.07/21.67  | 8.5/20.77   | 8.48/20.25  | 8.61/21.03  | 8.67/21.01  |
|         | paired           | 11.64/24.64 | 12.02/24.04 | 11.34/24.16 | 11.8/24.32  | 11.7/24.29  |
| epoch10 | w/o Contaminated | 12.5/23.75  | 13.56/25.07 | 13.7/25.76  | 13.14/25.09 | 12.35/24.05 |
|         | paired           | 14.51/26.2  | 13.85/26.14 | 14.21/25.72 | 13.83/25.22 | 13.09/24.24 |
| epoch25 | w/o Contaminated | 16.95/28.93 | 16.4/28.06  | 16.13/27.81 | 16/28.32    | 16.06/28.02 |
|         | paired           | 17.26/29.19 | 16.36/28.58 | 17.58/29.56 | 16.91/28.92 | 17.03/29.06 |
| epoch50 | w/o Contaminated | 18.95/30.65 | 19.61/30.5  | 18.87/30.39 | 19.94/30.85 | 20.11/31.61 |
|         | paired           | 19.45/30.94 | 19.92/31.79 | 19.83/30.99 | 20.43/31.23 | 21.36/32.16 |

Task: Code Generation
|         |                  | run1         | run2          | run3          | run4         | run5          |
| ------- | ---------------- | ------------ | ------------- | ------------- | ------------ | ------------- |
| epoch1  | w/o Contaminated | 0.95/1.44    | 1.09/1.52     | 1.1/1.5       | 1.04/1.44    | 0.99/1.37     |
|         | paired           | 1.28/2.45    | 1.16/2.37     | 1.17/2.4      | 1.14/2.32    | 1.24/2.39     |
| epoch5  | w/o Contaminated | 6.63/9.27    | 6.1/8.88      | 6.94/9.52     | 7.39/9.98    | 7.78/10.02    |
|         | paired           | 6.58/10.93   | 6.88/11.4     | 6.84/10.27    | 6.79/10.18   | 6.1/10.03     |
| epoch10 | w/o Contaminated | 10.35/13.76  | 10.04/13.9    | 11.4/14.52    | 10.8/14.31   | 10.38/14.46   |
|         | paired           | 10.38/13.19  | 9.85/13.29    | 9.47/13.7     | 9.41/14.1    | 10.29/13.97   |
| epoch25 | w/o Contaminated | 12.83/18.99  | 13.13/18.77   | 12.71/18.92   | 12.95/19.53  | 12.13/18.66   |
|         | paired           | 13.18/19.49  | 12.47/19.05   | 13.34/20.09   | 13.14/19.9   | 12.91/20.17   |
| epoch50 | w/o Contaminated | 14.59/23.01  | 14.76/23.14   | 14.09/22.01   | 15.09/22.4   | 15.02/22.73   |
|         | paired           | 15.625/23.93 | 14.79/23.51   | 14.74/22.77   | 14.2/21.52   | 14.99/22.54   |


### Model: Llama-33B
#### Direct Inference
Task: Code Translation

|                      | run1        | run2        | run3        | run4        | run5        |
| -------------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Input-only(Java-C#)  | 71.27/87.01 | 71.77/87.4  | 71.55/87.39 | 71.26/86.82 | 71.5/86.7   |
| w/o contaminated     | 72.65/88.3  | 73.63/88.5  | 71.06/87.92 | 70.84/86.55 | 72.36/87.32 |
| Output-only(C#-Java) | 74.19/83.76 | 73.34/83.07 | 75.52/84.55 | 73.54/83.68 | 71.37/81.96 |
| w/o contaminated     | 73.65/83.68 | 73.74/83.85 | 73.64/83.63 | 73.79/83.08 | 73.59/83.51 |
| Unpaired(Java-c#)    | 68.03/81.8  | 65.5/79.97  | 66.77/79.99 | 68.15/81.99 | 66.2/80.6   |
| w/o contaminated     | 65.75/79.51 | 63.78/78.91 | 66.7/80.07  | 67.06/80.14 | 65.3/79.13  |
| Unpaired(C#-Java)    | 69.88/77.5  | 70.41/78.17 | 70.7/78.42  | 72.38/80.03 | 69.25/77.13 |
| w/o contaminated     | 69.85/78.35 | 67.09/76    | 67.92/76.99 | 68.2/76.57  | 67.32/76.18 |

Task: Code Generation

|                       | run1        | run2        | run3        | run4        | run5        |
| --------------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Input-only(java->nl)  | 10.59/29.01 | 10.52/29.09 | 10.24/28.8  | 9.92/29.93  | 11.7/32.31  |
| w/o contaminated      | 10.97/31.37 | 10.53/30.41 | 9.72/29.27  | 12.2/31.97  | 11.31/30.91 |
| Output-only(nl->java) | 49.7/63.9   | 47.81/62.03 | 46.9/61.54  | 48.77/62.4  | 47.82/61.97 |
| w/o contaminated      | 47.63/61.33 | 48.75/62.33 | 47.09/62.29 | 48.31/61.27 | 46.61/60.08 |
| Paired(nl->java)      | 37.04/51.09 | 36.58/51.37 | 34.08/48.78 | 33.54/47.91 | 34.51/49.18 |
| w/o contaminated      | 31.54/46.39 | 32.18/47.91 | 31.07/46.92 | 29.66/46.13 | 29.27/44.17 |


### Model: Starcoder-15.5B
#### Direct Inference

Task: Code Translation

|                      | run1        | run2        | run3        | run4        | run5        |
| -------------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Input-only(Java-C#)  | 71.19/80.71 | 71.74/83.31 | 73.12/85.81 | 72.66/84.22 | 73.79/85.85 |
| w/o contaminated     | 72.59/84.18 | 73.45/85.7  | 71.77/83.6  | 75.59/87.43 | 75.1/86.12  |
| Output-only(C#-Java) | 76.64/84.61 | 77.5/85.48  | 76.8/84.4   | 77.1/86.15  | 77.28/84.97 |
| w/o contaminated     | 77.31/85.31 | 77.34/85.62 | 78.07/85.58 | 77.26/85.41 | 77.38/85.03 |
| Unpaired(Java-c#)    | 74.93/87.31 | 76.17/88.12 | 77.41/89.14 | 78.22/89.85 | 76.86/89.81 |
| w/o contaminated     | 77.16/89.81 | 77.04/89.24 | 77.04/89.37 | 73.76/87.06 | 75.8/88.93  |
| Unpaired(C#-Java)    | 83.73/90.9  | 84.42/91.89 | 81.1/88.47  | 83.91/91.05 | 82.52/90.46 |
| w/o contaminated     | 80.9/89.76  | 80.82/89.08 | 79.11/87.97 | 82.3/90.02  | 80.97/88.95 |


Task: Code Generation

|                       | run1        | run2        | run3        | run4        | run5        |
| --------------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Input_only(java->nl)  | 9.95/28.16  | 9.46/28.65  | 9.55/27.93  | 10.53/29    | 10.41/28.77 |
| w/o contaminated      | 8.39/27.3   | 9.7/29.16   | 9.64/28.47  | 11.45/29.8  | 9.46/27.81  |
| Output-only(nl->java) | 48.69/63.72 | 46.81/63.41 | 47.31/64.54 | 48.93/65.05 | 46.5/65.51  |
| w/o contaminated      | 47.36/64.38 | 44.9/62.51  | 46.55/63.37 | 45.88/63.39 | 46.86/63.92 |
| Paired(nl->java)      | 35.48/51.19 | 34.81/50    | 34.88/50.77 | 34.71/50.91 | 36.45/51.4  |
| w/o contaminated      | 31.8/47.85  | 32.63/49.01 | 33.47/49.46 | 33.33/48.39 | 32.94/49.61 |

