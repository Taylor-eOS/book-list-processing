import os
import re

def process_filenames(input_folder, output_file):
    filenames = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    processed_names = []
    stop_words = {'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 
                 'for', 'with', 'by', 'as', 'into', 'must', 'be', 'is', 'are'}
    
    for filename in filenames:
        name = os.path.splitext(filename)[0]
        words = re.sub(r'[^\w\s-]', '', name).replace('_', ' ').replace('-', ' ').split()
        filtered = [w for w in words if w.lower() not in stop_words] or words
        
        if len(filtered) <= 3:
            selected = filtered
        else:
            word_scores = [(i, len(w)*(1 + 0.5*(i==0 or i==len(filtered)-1))) for i, w in enumerate(filtered)]
            sorted_words = sorted(word_scores, key=lambda x: (-x[1], x[0]))
            top_indices = {i for i, _ in sorted_words[:4]}
            ordered_indices = sorted([i for i in range(len(filtered)) if i in top_indices])
            selected = [filtered[i] for i in ordered_indices[:3]]
        
        processed_names.append(' '.join(selected))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_names))


if __name__ == "__main__":
    input_folder = 'input_files'
    output_file = 'processed_filenames.txt'
    
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"Created '{input_folder}' folder. Add files and rerun.")
    else:
        process_filenames(input_folder, output_file)
        print(f"Processing complete. Results saved to {output_file}")

