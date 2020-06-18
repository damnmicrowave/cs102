import string
from typing import List, Set


def build_trie() -> dict:
    with open('text') as file:
        text = file.read().lower()
        translator = str.maketrans("", "", string.punctuation)
        text = text.translate(translator)
        words = text.split()
        trie = dict()
        for word in words:
            value = words.count(word)
            curr_trie = trie
            for letter in word:
                curr_trie = curr_trie.setdefault(letter, {})
            curr_trie['VALUE'] = value
        return trie


def get_all_words(tree: dict, word: str, all_words: dict) -> None:
    for key in tree.keys():
        if key == 'VALUE':
            all_words[word] = tree['VALUE']
        else:
            get_all_words(tree[key], word + key, all_words)


def in_trie(trie: dict, word: str, curr_letter=0) -> bool:
    if curr_letter < len(word) and word[curr_letter] in trie.keys():
        return in_trie(trie[word[curr_letter]], word, curr_letter + 1)
    else:
        return curr_letter == len(word) and 'VALUE' in trie.keys()


def autocomplete(trie: dict, prefix: str, count: int) -> List[str]:
    curr_node = trie
    for letter in prefix:
        curr_node = curr_node[letter]
    words = dict()
    get_all_words(curr_node, prefix, words)
    words = [k for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)]
    return words[:count]


def edits(word: str) -> Set[str]:
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def autocorrect(trie: dict, word: str) -> List[str]:
    return [w for w in edits(word) if in_trie(trie, w)]


if __name__ == '__main__':
    my_trie = build_trie()
    print(autocomplete(my_trie, 'ha', 10))
    print(autocorrect(my_trie, 'hag'))
