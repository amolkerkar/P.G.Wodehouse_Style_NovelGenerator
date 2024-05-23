import re
from datasets import Dataset
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

with open(r'.\novel_data_preprocessing\combined_novels.txt', 'r', encoding='utf-8') as file:
    text = file.read()


def preprocess_text(text, chunk_size=512):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    sentences = sent_tokenize(text)

    #Joining
    chunks = []
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        current_length += len(sentence)
        current_chunk.append(sentence)
        if current_length >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

text_chunks = preprocess_text(text)

# Converting to hugging face dataset with source and target seqs
dataset = Dataset.from_dict({
    'input_ids': text_chunks,
    'labels': text_chunks
})

dataset.save_to_disk('preprocessed_novels_2')