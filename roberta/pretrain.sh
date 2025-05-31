batch_size=32
load_model=True

tokenizer_path="./roberta_init_model"
dataset1="./pre-train-data/train.jsonl"
dataset2="./translate/test.jsonl"
save_path=""
model_path="./roberta_init_model"
skip_line=1000 # 1000 for RQ1,RQ2,RQ4 ,2000 for RQ3
RQ=1 #2,3,4
Task=1 #1 for code Translation , 2 for code generation


python pre-train.py \
--tokenizer_path $tokenizer_path \
--dataset1 $dataset1 \
--dataset2 $dataset2 \
--batch_size $batch_size \
--save_path $save_path \
--model_path $model_path \
--load_model $load_model \
--R_Q $RQ \
--skip_line $skip_lines \
--Task $Task