from typing import Dict

def main():
    book_path = "./books/frankenstein.txt"
    file_contents = get_book_text(book_path)
    num_words = count_words(file_contents)
    letter_counts = count_letters(file_contents)
    sorted_letter_counts = sort_letter_counts(letter_counts)

    print(f"--- Begin report of {book_path} ---")
    print(f"{num_words} found in the document")
    print()
    for letter_count in sorted_letter_counts:
        ch = letter_count["char"]
        n = letter_count["count"]
        print(f"The '{ch}' character was found {n} times")
    print("--- End report ---")

def get_book_text(path: str):
    with open(path) as f:
        return f.read()

def count_words(s: str):
    return len(s.split())

def count_letters(s: str):
    counts = {}
    for ch in s:
        if ch.isalpha():
            ch_lower = ch.lower()
            if ch_lower in counts.keys():
                counts[ch_lower] += 1
            else:
                counts[ch_lower] = 1
    return counts

def sort_letter_counts(letter_counts: Dict[str, int]):
    unsorted = [{"char": k, "count": v} for k,v in letter_counts.items()]
    def sort_on(d):
        return d["count"]
    return sorted(unsorted, key=sort_on, reverse=True)

main()
