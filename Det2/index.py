def read_file(filename):
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        text = file.read()
    return text

def clean_text(text):
    text = text.lower()
    for char in ['.', ',', ';', ':', '!', '?', '-', '(', ')', '[', ']', '\n', '"', "'"]:
        text = text.replace(char, ' ')
    words = text.split()
    return words

def word_frequency(words):
    freq = {}
    for word in words:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq

def jaccard(set1, set2):
    common = set1.intersection(set2)
    total = set1.union(set2)
    return len(common) / len(total)

def cosine(freq1, freq2):
    all_words = list(set(freq1.keys()).union(set(freq2.keys())))
    dot = 0
    mag1 = 0
    mag2 = 0
    for word in all_words:
        a = freq1.get(word, 0)
        b = freq2.get(word, 0)
        dot += a * b
        mag1 += a * a
        mag2 += b * b
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot / (mag1 ** 0.5 * mag2 ** 0.5)

def main():
    text1 = read_file('paper1.txt')
    text2 = read_file('paper2.txt')

    words1 = clean_text(text1)
    words2 = clean_text(text2)

    freq1 = word_frequency(words1)
    freq2 = word_frequency(words2)

    set1 = set(freq1.keys())
    set2 = set(freq2.keys())

    jaccard_score = jaccard(set1, set2)
    cosine_score = cosine(freq1, freq2)

    print("Jaccard Coefficient:", round(jaccard_score, 3))
    print("Cosine Similarity:", round(cosine_score, 3))

    if jaccard_score > 0.7 or cosine_score > 0.8:
        print("These two papers look very similar.")
    else:
        print("The papers seem different enough.")

if __name__ == "__main__":
    main()
