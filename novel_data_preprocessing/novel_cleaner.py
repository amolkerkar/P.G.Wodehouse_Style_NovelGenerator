import re
import os
novels_dir = r'.novel_data_preprocessing\novels'
cleaned_novels_path = r"novel_data_preprocessing\cleaned_novels"

def extract_content(text):
    #start and end patterns
    start_pattern = r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*'
    end_pattern = r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*'
    
    #Finding start and end positions
    start_match = re.search(start_pattern, text, flags=re.DOTALL)
    end_match = re.search(end_pattern, text, flags=re.DOTALL)
    
    start_pos = start_match.end()
    end_pos = end_match.start()
    content = text[start_pos:end_pos]
    content = content.strip()
    
    return content

def clean_text(text):
    text = re.sub(r'Produced by .*?\n', '', text)  #Remove producer
    text = re.sub(r'\n+', '\n', text)
    
    #removing "CHAPTER" followed by Roman numerals
    text = re.sub(r'CHAPTER\s+[IVXLCDM]+\s*\n', '', text)
    
    #Normalizing
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    text = re.sub(r'\.\.\.\s*', '... ', text)  # Normalize ellipses
    text = re.sub(r'\b(Mr|Mrs|Ms|Dr)\.\s', r'\1 ', text)  # Handle abbreviations
    text = re.sub(r'\.(\s+)([A-Z])', r'. \2', text)  # Ensure proper spacing after periods
    
    #dialogues
    text = re.sub(r'"\s*([A-Za-z])', r'" \1', text)

    text = text.strip()
    
    return text

for novel in os.listdir(novels_dir):
    novel_file = os.path.join(novels_dir, novel)
    with open(novel_file, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    extracted_content = extract_content(raw_text)
    cleaned_content = clean_text(extracted_content)
    save_path = os.path.join(cleaned_novels_path, novel)
    print(save_path)

    with open( save_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    # print(cleaned_content[:2000])


