from transformers import (
    set_seed,
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    pipeline
)
import argparse
import tqdm
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
# import torch
# from bitsandbytes import optim

# ENV AND TRAINING VARIABLES
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
OUTPUT_DIR = "./outputs/llama3-ft-lora"
TRANSLATIONS_DIR = "./translations/llama3"
LR = 2e-5
BATCH_SIZE = 4
GRAD_ACCUM_STEPS = 4
LORA_R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1
TARGET_MODULES = ["q_proj", "v_proj"]  # Modules to apply LoRA to


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', type=str,
                        help="Lanuage pair to finetune and translate",
                        default='ashaninka-spanish',
                        )

    parser.add_argument('--datapath', type=str,
                        help="path to folder with jsonfiles {'source': <sent_in_spanish>, 'target': <sent_in_trglang>}",
                        default="/scratch/project_2011553/vazquezc/americasnlp2025/ST1_MachineTranslation/tfiles",
                        )
    parser.add_argument('--do_finetune', help="Run with this to FT in trianing data. Otherwise, it only uses model for inference",
                        action=argparse.BooleanOptionalAction)

    parser.add_argument('--debug', '-debug', help="run in debug mode... for dev purposes",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    return args


set_seed(42)
args = parse_options()
if args.do_finetune:
    TRANSLATIONS_DIR += '-ft-lora'

# Load tokenizer with the correct chat template
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# Load model with 4-bit quantization to reduce memory usage
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype="auto"
)

# Prepare model for k-bit training
#model = prepare_model_for_kbit_training(model)
print(f'model_device={model.device}')


def preprocess_function(example):
    # Expected dataset format:
    # {"source": "<Spanish text>", "target": "<non-spanish text>", 'source_lang': 'spanish', 'target_lang': f'{tgt_lang}'}
    # Create prompts using the Llama 3 chat template
    prompts = []
    for src, tgt in zip(example["source"], example["target"]):
        messages = [
            {"role": "system", "content": "You are a professional translator. Translate the text accurately preserving meaning, tone, and style."},
            {"role": "user", "content": f"Translate this from {example['source_lang']} to {example['target_lang']} (only respond with the translation, no additional comments needed): {src}"},
            {"role": "assistant", "content": tgt}
        ]
        prompts.append(tokenizer.apply_chat_template(messages, tokenize=False))

    return tokenizer(prompts, padding="max_length", truncation=True, max_length=512, return_tensors="pt")


def flip_source_target(example):
    example['source'], example['target'] = example['target'], example['source']
    return example


def assign_source_target(example, srcl, trgl):
    example['source_lang'] = srcl
    example['target_lang'] = trgl
    return example


def get_dataset(data_path, src, trg, split='train'):
    dataset = load_dataset("json", data_files=f"{data_path}-{split}.json")

    if args.debug:
        nsample = 250 if split in ['train', 'full'] else 100
        dataset['train'] = dataset['train'].select(range(nsample))
    # SPANISH IS ALWAYS THE SOURCE LANGUAGE IN THE JSONs
    if not (src == 'spanish'):
        print('flipping src-trg')
        dataset = dataset.map(flip_source_target)

    dataset = dataset.map(assign_source_target, fn_kwargs={"srcl": src, "trgl": trg})

    print(f"example datapoint: {dataset['train'][10]}")

    if split in ['train', 'full']:
        return dataset.map(preprocess_function, batched=True)
    else:
        return dataset


# IN THE JSON FILES: SPANISH IS ALWAYS THE SOURCE LANGUAGE!
src, trg = args.language.split('-')
XXX = src if trg == 'spanish' else trg  # XXX = non-spanish language
DATASET_SUFFIX = f"{args.datapath}/{XXX}-spanish"  # Replace with your dataset

if args.do_finetune:
    # Configure LoRA
    peft_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=TARGET_MODULES,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, peft_config)
    print(f'model trainable parameter: ')
    model.print_trainable_parameters()
    dataset = get_dataset(DATASET_SUFFIX, src, trg, split='full')

    # Data collator
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM_STEPS,
        learning_rate=LR,
        num_train_epochs=1,
        logging_dir=f"{OUTPUT_DIR}/logs",
        logging_steps=10,
        save_strategy="epoch",
        remove_unused_columns=False,
        push_to_hub=False,
    )

    # Trainer
    print(f'INFO: Initializing Trainer...')
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset.remove_columns(['source', 'target', 'source_lang', 'target_lang'])["train"],
        data_collator=data_collator,
    )

    print(f'INFO: Fine-tuning to translate {src} to {trg}...')
    trainer.train()
    print('DONE training')

    print(f"Fine-tuning complete! Saving model: outputs/model_llama3_FT_{src}-{trg}")

    trainer.save_model(OUTPUT_DIR + '-' + src + '-' + trg)
    tokenizer.save_pretrained(OUTPUT_DIR + '-' + src + '-' + trg)


# Create translation pipeline
translator = pipeline("text-generation", model=model, tokenizer=tokenizer)
for split in ['test', 'dev']:
    dataset = get_dataset(DATASET_SUFFIX, src, trg, split)
    print("running translation for", split)
    generated_text = []
    # for srcsent in tqdm.tqdm(dataset['train'].select(range(2))):
    for srcsent in tqdm.tqdm(dataset['train']):
        messages = [
            {"role": "system", "content": "You are a professional translator. Translate the text accurately preserving meaning, tone, and style."},
            {"role": "user", "content": f"Translate the text from {src} to {trg} (only respond with the translation, no additional comments needed): {srcsent}"},
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        output = translator(prompt, max_new_tokens=250)
        print(output[0]["generated_text"])
        # extract only the output text:
        coso = output[0]["generated_text"].split('<|start_header_id|>assistant<|end_header_id|>')[-1]
        generated_text.append(coso.strip())

    output_file = f"{TRANSLATIONS_DIR}-{src}-{trg}_{split}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for translation in generated_text:
            f.write(translation.replace("\n", " ") + "\n")  # Write each translation on a new line (sometimes the model outputs '\n')

    print(f"INFO: Translations saved to {output_file}")
