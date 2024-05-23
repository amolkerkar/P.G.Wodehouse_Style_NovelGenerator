import re
from datasets import load_from_disk
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments

dataset = load_from_disk('novel_data_preprocessing/preprocessed_novels_2')

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

def tokenize_function(examples):
    model_inputs = tokenizer(examples['input_ids'], max_length=512, truncation=True, padding='max_length')
    labels = tokenizer(examples['labels'], max_length=512, truncation=True, padding='max_length')
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(tokenize_function, batched=True)

tokenized_dataset.save_to_disk('novel_data_preprocessing/tokenized_novels_2')

tokenized_dataset = load_from_disk('novel_data_preprocessing/tokenized_novels_2')

model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=2,
    save_steps=10_000,
    save_total_limit=2,
    fp16=True,
)
         
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
)

trainer.train()

model.save_pretrained('models/fine_tuned_bart_2')
tokenizer.save_pretrained('tokenizer/fine_tuned_bart_2')
