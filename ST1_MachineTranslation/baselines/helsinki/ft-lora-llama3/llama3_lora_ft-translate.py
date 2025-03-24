import argparse
import tqdm
import torch

from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import TrainingArguments
from datasets import load_dataset  # , DatasetDict
from transformers import set_seed, DataCollatorForSeq2Seq, Trainer  # , pipeline
from peft import get_peft_model, LoraConfig, TaskType


def preprocess_function(example):
    """Tokenizes input (source) and target texts using the provided tokenizer."""
    inputs = tokenizer(example["source"], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    labels = tokenizer(example["target"], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    # Ensure labels are properly formatted, replacing pad tokens with -100 for loss masking
    aux = labels["input_ids"]
    first_occurrence_index = torch.where(aux == tokenizer.pad_token_id)
    labels["input_ids"] = torch.where(aux == tokenizer.pad_token_id, torch.tensor(-100), aux)

    if first_occurrence_index[0].numel() > 0:
        labels["input_ids"][0, first_occurrence_index[-1][0]] = tokenizer.eos_token_id

    return {
        "input_ids": inputs["input_ids"][0],  # Convert from tensor to list
        "attention_mask": inputs["attention_mask"][0],  # Convert from tensor to list
        "labels": labels["input_ids"][0],  # Convert from tensor to list
    }


def flip_source_target(example):
    example['source'], example['target'] = example['target'], example['source']
    return example


def get_dataset(lpair, src, trg, split='train'):
    """
    loads json files with naming convention '{languagepair}-{split}.json' and structure given by:
    [{  "source": <sentence in SPANISH >,
        "target": <sentence in TRG lang > },...]
    """
    dbpath = <path/to/folder_w_jsons>
    dataset = load_dataset("json", data_files=f"{dbpath}/{lpair}-{split}.json")

    if not (src == 'spanish'):
        print('flipping src-trg')
        dataset = dataset.map(flip_source_target)
    if split == 'train':
        return dataset.map(preprocess_function, batched=False)
    else:
        return dataset


def translate(text, model, tokenizer):
    # Encode the input text (source language)
    inputs = tokenizer(text['source'], return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Ensure the input tensors are moved to the correct device
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Generate translation (output in target language)
    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,  # Source text input IDs
            attention_mask=attention_mask,
            max_length=512,  # Max length for the translated output
            num_beams=5,  # Beam search for better quality
            length_penalty=1.0,  # Adjust output length preference
            early_stopping=True  # Stop early if EOS is reached
        )

    # Decode the output (target language translation)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text


def main(args):
    set_seed(42)

    global device
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    print(f'torch.device_count={torch.cuda.device_count()}')

    hftok = <reads_or_copy_your_HF_token>
    login(token=hftok)

    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",  # Automatically assigns to GPU if available
        torch_dtype="auto"
    )
    print(f'model_device={model.device}')

    # LoRA configuration
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=[
            'q_proj',  # Llama uses q_proj instead of att_proj
            'v_proj',  # Similarly, you might need to target v_proj
            'k_proj',  # For the key projection layer
            'o_proj',  # For output projection
        ],
    )

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./llama3-nmt-checkpoints",
        save_strategy="epoch",
        num_train_epochs=1.0,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_steps=1,
        per_device_train_batch_size=4,
        push_to_hub=False,  # Set to True if using HF Hub
    )

    # gc.collect()
    # torch.cuda.empty_cache()
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer)

    lpair = args.language
    src, trg = lpair.split('-')
    if src == 'spanish':
        lpair = trg + '-' + src

    for srclang, trglang in [(src, trg)]:  # , (trg, src)]:
        print(srclang, trglang)
        print('######      INFO: language pair:', lpair, '; from ', srclang, ' to ', trglang)
        dataset = get_dataset(lpair, srclang, trglang)
        # Apply LoRA to model
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()  # Verify trainable parameters

        print(f'INFO: Initializing Trainer...')
        # Define data collator for Seq2Seq tasks
        data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset['train'],
            tokenizer=tokenizer,
            data_collator=data_collator,
        )

        print(f'INFO: Fine-tuning to translate {lpair}...')
        trainer.train()
        print('DONE training')
        print(f"Fine-tuning complete! Saving model: outputs/model_llama3_FT__{srclang}-{trglang}")

        model.save_pretrained(f"outputs/llama3_FT_{srclang}-{trglang}")
        tokenizer.save_pretrained(f"outputs/llama3_FT_{srclang}-{trglang}")
        for split in ['test', 'dev']:
            dataset = get_dataset(lpair, srclang, trglang, split)
            print("running translation for", split)

            generated_text = []
            # for srcsent in tqdm.tqdm(dataset['train'].select(range(2))):
            for srcsent in tqdm.tqdm(dataset['train']):
                generated_text.append(translate(srcsent, model, tokenizer))

            output_file = <path_to_output_file>
            with open(output_file, "w", encoding="utf-8") as f:
                for translation in generated_text:
                    f.write(translation.replace("\n", " ") + "\n")  # Write each translation on a new line

            print(f"INFO: Translations saved to {output_file}")


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', type=str,
                        help="Lanuage pair to finetune and translate",
                        default='ashaninka-spanish',
                        )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_options()
    main(args)
