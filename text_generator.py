from transformers import BartTokenizer, BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained('models/fine_tuned_bart')
tokenizer = BartTokenizer.from_pretrained('tokenizer/fine_tuned_bart')

def generate_text(prompt, max_length=200, min_length=50, num_return_sequences=1, temperature=0.5, top_k=50, top_p=0.95):

    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output_ids = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        min_length=min_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        early_stopping=True,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=True
    )

    generated_texts = [tokenizer.decode(output_id, skip_special_tokens=True) for output_id in output_ids]
    return generated_texts

prompt = "It was 20th of May and I went to college to study. There was not a single person there."
generated_texts = generate_text(prompt, max_length=200, min_length=50, num_return_sequences=4)

for i, text in enumerate(generated_texts):
    print(f"Generated Text {i + 1}: {text}")
