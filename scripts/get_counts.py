from os import path

DIR = 'common/frequency/en'
MODULES = [
    ('monograms', 'monograms_counts'),
    ('bigrams', 'bigrams_counts'),
    ('trigrams', 'trigrams_counts'),
    ('quadgrams', 'quadgrams_counts'),
]

if __name__ == '__main__':
    for input_f, output_f in MODULES:
        with open(path.join(DIR, input_f), 'r') as input_file, open(path.join(DIR, output_f), 'w') as output_file:
            content = input_file.readlines()
            counts_sum = sum([int(line.strip().split()[1]) for line in content])
            output_file.write(str(counts_sum))
