import argparse
import torch
from transformers import RobertaConfig, RobertaModel,RobertaForMaskedLM,RobertaTokenizer
from torch import nn
from torch.utils.data import DataLoader, Dataset
import json
import os
from transformers import  DataCollatorForLanguageModeling
from tqdm import tqdm
from torch.optim import AdamW
import random

class CustomDataset(Dataset):
    def __init__(self, input_ids, attention_masks):
        self.input_ids = input_ids
        self.attention_masks = attention_masks
    
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_masks[idx]
        }
    
def init_model(device):
    config =  RobertaConfig(vocab_size=52000,
                            max_position_embeddings=514,
                            num_attention_heads=12,
                            num_hidden_layers=12,
                            type_vocab_size=1)
    
    model= RobertaForMaskedLM(config=config).to(device)
    for param in model.parameters():
        print(param)
        break
    return model

def load_init_model(model_path,device):
    model= RobertaForMaskedLM.from_pretrained(model_path).to(device)
    for param in model.parameters():
        print(param)
        break
    return model

def get_data(path1,path2,R_Q,skip_count,Task):
    code = []
    with open(path1, 'r') as fr:
        lines = fr.readlines()  
        total_lines = len(lines)
        print(total_lines)
        skip_indices = set(random.sample(range(total_lines), skip_count))
        print(f"Skipping {skip_count} samples from {total_lines} total samples.")


        for idx, line in enumerate(lines):
            if idx in skip_indices:
                continue  
            sample = json.loads(line)
            code.append(sample["code"])
    print("len(code):",len(code))

    if Task==1:
        input_name='java_code'
        output_name='cs_code'
    else:
        input_name='nl'
        output_name='code'

    if R_Q==4:
        with open(path2,"r")as fj:
            for line in fj.readlines():
                sample = json.loads(line)
                code_sample=sample[input_name]+" <SEP> "+sample[output_name]
                code.append(code_sample)
    if R_Q==3:
        with open(path2,"r")as fj:
            for line in fj.readlines():
                sample = json.loads(line)
                code.append(sample[input_name])#nl
        with open(path2,"r")as fj:
            for line in fj.readlines():
                sample = json.loads(line)
                code.append(sample[output_name])#code
    if R_Q==2:
        with open(path2,"r")as fj:
            for line in fj.readlines():
                sample = json.loads(line)
                code.append(sample[output_name])#code
    if R_Q==1:
        with open(path2,"r")as fj:
            for line in fj.readlines():
                sample = json.loads(line)
                code.append(sample[input_name])#nl
    print("len[code]:",len(code))

    return code

def train(tokenizer_path,path1,path2,batch_size,lr=1e-5,epoch_num=20,
          device="cuda",save_path="",load=True,model_path="",Research_Q=1,skip_line=500,Task=1):
    if load:
        model=load_init_model(model_path=model_path,device=device)
    else:
        model=init_model(device=device)
    tokenizer = RobertaTokenizer.from_pretrained(tokenizer_path)
    #############################################
    tokenizer.add_tokens(["<SEP>"])
    model.resize_token_embeddings(len(tokenizer))
    ##############################################
    inputs = tokenizer(get_data(path1,path2,Research_Q,skip_line,Task), max_length=512,
                       return_tensors='pt', padding=True, truncation=True)
    print(inputs['input_ids'].shape)
    print(inputs['attention_mask'].shape)
    dataset = CustomDataset(inputs['input_ids'], inputs['attention_mask'])

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)
    dataloader = DataLoader(dataset, batch_size=batch_size, collate_fn=data_collator)
    

    # Optimizer
    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {"params": [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], "weight_decay": 0.01},
        {"params": [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], "weight_decay": 0.0}]
    optimizer = AdamW(params=optimizer_grouped_parameters, lr=lr)
    # Training loop
    model.train()
    for epoch in range(epoch_num):
        print("Epoch:",epoch+1)
        for batch in tqdm(dataloader,desc='Step'):
            # Move batch to GPU
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad()
            # Forward pass
            outputs = model(**batch)
            loss = outputs.loss  # MLM loss is computed internally
            
            # Backward pass and optimization
            loss.backward()
            optimizer.step()
        print(f"Loss: {loss.item()}")
        model.save_pretrained(f'{save_path}/epoch{epoch}_model')
        tokenizer.save_pretrained(f'{save_path}/epoch{epoch}_model')


def main():
    parser = argparse.ArgumentParser()
    ## Required parameters  
    parser.add_argument("--tokenizer_path", default="", type=str, required=True,
                        help="your self tokenizer path")
    parser.add_argument("--dataset1",default="",type=str,required=True,
                        help="the backbone dataset")
    parser.add_argument("--dataset2",default="",type=str,required=True,
                        help="the contomination dataset")
    parser.add_argument("--batch_size",default=32,type=int,required=True,
                        help="")
    parser.add_argument("--save_path",default="",type=str,required=True,
                        help="")
    parser.add_argument("--epoch_num",default=20,type=int,required=False,
                        help="")
    parser.add_argument("--model_path",default="",type=str,required=False,
                        help="the init model`s path")
    parser.add_argument("--load_model", default=True, type=bool, required=False,
                        help="load init model or init self")
    parser.add_argument("--R_Q", default=1, type=bool, required=False,
                        help="")
    parser.add_argument("--skip_line", default=1000, type=bool, required=False,
                        help="")
    parser.add_argument("--Task", default=1, type=bool, required=False,
                        help="")
    args = parser.parse_args()

    tokenizer_path=args.tokenizer_path
    dataset1=args.dataset1
    dataset2=args.dataset2
    batch_size=args.batch_size
    load_model=args.load_model
    save_path=args.save_path
    model_path=args.model_path
    Rearsearch_q=args.R_Q
    skip_line=args.skip_line
    Task=args.Task

    train(tokenizer_path=tokenizer_path,
          path1=dataset1,
          path2=dataset2,
          batch_size=batch_size,
          load=load_model,
          save_path=save_path,
          model_path=model_path,
          R_Q=Rearsearch_q,
          skip_line=skip_line,
          Task=Task
          )
main()
