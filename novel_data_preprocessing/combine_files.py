import os
cleaned_novels_path = r"novel_data_preprocessing/cleaned_novels"

def combine_text_files(file_paths):
    combined_text = ""
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            combined_text += text + "\n\n"  # Adding some spacing between books
    return combined_text

# List of file paths
file_paths = [os.path.join(cleaned_novels_path, dir) for dir in os.listdir(cleaned_novels_path)]
# print(file_paths)
# Combine the text from all files
combined_text = combine_text_files(file_paths)

# Saving
with open('novel_data_preprocessing/combined_novels.txt', 'w', encoding='utf-8') as file:
    file.write(combined_text)