from collections import Counter, defaultdict
from nltk import bigrams, ngrams
from nltk.tokenize import regexp_tokenize
from random import choice, choices


EXIT = 'exit'
TOKENS_IN_LINE = 10
MIN_TOKENS_IN_LINE = 5


def main(stage=6):
    run = {1: run_stage_1, 2: run_stage_2, 3: run_stage_3, 4: run_stage_4, 5: run_stage_5, 6: run_stage_6}

    with open(input(), 'r', encoding='utf-8') as f:
        tokens = regexp_tokenize(f.read(), r'\S+')

    run[stage](tokens)


# using ("head1", "head2") as a key;

def run_stage_6(tokens: [str]):

    trigrams_w_tails_freq = defaultdict(Counter)
    for trigram in ngrams(tokens, 3):
        trigrams_w_tails_freq[(trigram[0], trigram[1])][trigram[2]] += 1

    heads = Counter(filter(lambda head_tup: head_tup[0][0].isupper() and head_tup[0][-1] not in ".!?", trigrams_w_tails_freq.keys()))
    heads_freq = tuple(heads.values())
    heads = tuple(heads.keys())

    for i in range(10):
        start = list(choices(heads, heads_freq)[0])     # list([("head1", "head2")][0]) == ["head1", "head2"]
        print(generate_even_better_text(start, trigrams_w_tails_freq, MIN_TOKENS_IN_LINE))


def generate_even_better_text(start: [str], trigrams_w_tails_freq: defaultdict[tuple[str], Counter], min_length: int) -> str:
    if len(start) < 2:
        raise ValueError
    text_tokens = start

    count = 2
    while count < min_length or (text_tokens[-1][-1] not in ".?!"):
        cur_head = tuple(text_tokens[-2:])
        tails = trigrams_w_tails_freq[cur_head]
        text_tokens += choices(tuple(tails.keys()), tuple(tails.values()))
        count += 1

    return " ".join(text_tokens)


# using "head1 head2" as a key;

# def run_stage_6(tokens: [str]):
#
#     heads = []
#     trigrams_w_tails_freq = defaultdict(Counter)
#     for trigram in ngrams(tokens, 3):
#         trigrams_w_tails_freq[' '.join(trigram[:-1])][trigram[2]] += 1
#         if trigram[0][0].isupper() and trigram[0][-1] not in ".!?":
#             heads.append(' '.join(trigram[:-1]))
#
#     heads = Counter(heads)
#     heads_freq = tuple(heads.values())
#     heads = tuple(heads.keys())
#
#     for i in range(10):
#         start = regexp_tokenize(choices(heads, heads_freq)[0], r'\S+')     # ["head1", "head2"]
#         print(generate_even_better_text(start, trigrams_w_tails_freq, MIN_TOKENS_IN_LINE))
#
#
# def generate_even_better_text(start: [str], trigrams_w_tails_freq: defaultdict[str, Counter], min_length: int) -> str:
#     if len(start) < 2:
#         raise ValueError
#     text_tokens = start
#
#     count = 2
#     while count < min_length or (text_tokens[-1][-1] not in ".?!"):
#         cur_head = ' '.join(text_tokens[-2:])
#         tails = trigrams_w_tails_freq[cur_head]
#         text_tokens += choices(tuple(tails.keys()), tuple(tails.values()))
#         count += 1
#
#     return " ".join(text_tokens)


def run_stage_5(tokens: [str]):

    bigrams_w_tails_freq = defaultdict(Counter)
    for head, tail in bigrams(tokens):
        bigrams_w_tails_freq[head][tail] += 1

    heads = Counter(filter(lambda token: token[0].isupper() and token[-1] not in ".!?", bigrams_w_tails_freq.keys()))
    heads_freq = tuple(heads.values())
    heads = tuple(heads.keys())

    for i in range(10):
        print(generate_better_text(choices(heads, heads_freq), bigrams_w_tails_freq, MIN_TOKENS_IN_LINE))


def generate_better_text(start: [str], bigrams_w_tails_freq: defaultdict[str, Counter], min_length: int) -> str:
    if not start:
        raise ValueError
    text_tokens = start

    count = 1
    while count < min_length or (text_tokens[-1][-1] not in ".?!"):
        tails = bigrams_w_tails_freq[text_tokens[-1]]
        text_tokens += choices(tuple(tails.keys()), tuple(tails.values()))
        count += 1

    return " ".join(text_tokens)


def run_stage_4(tokens: [str]):

    bigrams_w_tails_freq = defaultdict(Counter)
    for head, tail in bigrams(tokens):
        bigrams_w_tails_freq[head][tail] += 1

    heads = Counter(bigrams_w_tails_freq.keys())
    heads_freq = tuple(heads.values())
    heads = tuple(heads.keys())

    for i in range(10):
        print(generate_text(choices(heads, heads_freq), bigrams_w_tails_freq, TOKENS_IN_LINE))


def generate_text(start: [str], bigrams_w_tails_freq: defaultdict[str, Counter], length: int) -> str:
    if not start:
        raise ValueError
    text_tokens = start
    # text_tokens = [choice(list(bigrams_w_tails_freq.keys()))]

    for i in range(length - 1):
        tails = bigrams_w_tails_freq[text_tokens[-1]]
        text_tokens += choices(tuple(tails.keys()), tuple(tails.values()))

    return " ".join(text_tokens)


def run_stage_3(tokens: [str]):

    bigrams_ = list(bigrams(tokens))

    bigrams_w_tails_freq = defaultdict(Counter)
    for head, tail in bigrams_:
        bigrams_w_tails_freq[head][tail] += 1

    while (inp := input()) != EXIT:
        print(f"Head: {inp}")
        try:
            tails = bigrams_w_tails_freq.get(inp)
            if tails is None:
                raise KeyError
            print(*("Tail: " + f"{tail}".ljust(30) + f"Count: {freq}" for tail, freq in tails.most_common()),
                  sep='\n', end='\n\n')
        except KeyError:
            print("The requested word is not in the model. Please input another word.")


def run_stage_2(tokens: [str]):

    bigrams_ = list(bigrams(tokens))
    # bigrams_ = list(zip(tokens[:-1], tokens[1:]))

    print_bigram_stats(bigrams_)

    inp = input()
    while inp != EXIT:
        try:
            b = bigrams_[int(inp)]
            print("Head: " + f"{b[0]}".ljust(20) + f"Tail: {b[1]}")
        except IndexError:
            print("Index Error. Please input a value that is not greater than the number of all bigrams.")
        except ValueError:
            print("Type Error. Please input an integer.")
        inp = input()


def run_stage_1(tokens: [str]):

    print_corpus_stats(tokens)

    inp = input()
    while inp != EXIT:
        try:
            print(tokens[int(inp)])
        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
        except ValueError:
            print("Type Error. Please input an integer.")
        inp = input()


def print_bigram_stats(bigrams_: [tuple[str]]):
    print(f"Number of bigrams: {len(bigrams_)}", end='\n\n')


def print_corpus_stats(tokens: [str]):
    print("Corpus statistics")
    print(f"All tokens: {len(tokens)}")
    print(f"Unique tokens: {len(set(tokens))}", end='\n\n')


if __name__ == '__main__':
    main()
