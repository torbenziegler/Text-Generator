import random
from collections import Counter

from nltk.tokenize import WhitespaceTokenizer
from nltk.util import trigrams

# Reading file
file = open("corpus.txt", 'r', encoding="utf-8")
text = file.read()

# Tokenization
tokenizer = WhitespaceTokenizer()
tokens = tokenizer.tokenize(text)
trigrams = list(trigrams(tokens))
unique_tokens = len(set(tokens))

# Print corpus statistics
print(f"Corpus statistics\nAll tokens: {len(tokens)}\nUnique tokens: {unique_tokens}")
print(f"Number of trigrams: {len(trigrams)}\n")

# Create Markov Chain
trigrams_dict = {}
for element in trigrams:
    trigrams_dict.setdefault(f"{element[0]} {element[1]}", []).append(element[2])
for element in trigrams:
    head = f"{element[0]} {element[1]}"
    trigrams_dict[head] = Counter(trigrams_dict[head])

# Create random sentences
print("Generated sentences:\n")
punctuation = ['.', '?', '!']
for sentence in range(0, 10):
    random_sentence_list = []

    # Create first two words
    random_head = random.choice(trigrams)
    current_head = f"{random_head[0]} {random_head[1]}"
    while random_head[0][0].islower() or not random_head[0][0].isalpha() or random_head[0][-1] in punctuation:
        random_head = random.choice(trigrams)
        current_head = f"{random_head[0]} {random_head[1]}"
    random_sentence_list.append(random_head[0])
    random_sentence_list.append(random_head[1])

    # Create words 3 - 5
    for word in range(1, 4):
        head = f"{random_sentence_list[-2]} {random_sentence_list[-1]}"
        next_word = trigrams_dict[head].most_common(1)[0][0]
        random_sentence_list.append(next_word)
        current_head = f"{random_sentence_list[-2]} {random_sentence_list[-1]}"

    # Create remaining words
    while next_word[-1] not in punctuation:
        head = f"{random_sentence_list[-2]} {random_sentence_list[-1]}"
        next_word = trigrams_dict[head].most_common(1)[0][0]
        random_sentence_list.append(next_word)

    print(' '.join(random_sentence_list))
