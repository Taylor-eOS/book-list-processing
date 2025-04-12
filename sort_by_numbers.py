import re

def extract_number(s):
    match = re.search(r'(\d+)$', s)
    if match:
        return int(match.group(1))
    return 0  #Default if no number is found

def process_book_list(input_file, output_file=None):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    #Pair each line with its extracted number
    paired_lines = [(line.strip(), extract_number(line)) for line in lines]
    #Sort by the extracted number in descending order
    paired_lines.sort(key=lambda x: x[1], reverse=True)
    #Remove the numbers from the lines
    processed_lines = []
    for line, _ in paired_lines:
        #Remove trailing numbers
        cleaned_line = re.sub(r'\d+$', '', line)
        processed_lines.append(cleaned_line)
    #Write to output file or print to console
    if output_file:
        with open(output_file, 'w') as f:
            f.write('\n'.join(processed_lines))
        print(f"Processed lines written to {output_file}")
    else:
        print("Processed lines:")
        for line in processed_lines:
            print(line)

#Example usage:
input_filename = 'book_list.txt'
output_filename = 'sorted_books.txt'  #Set to None to print to console instead
process_book_list(input_filename, output_filename)

