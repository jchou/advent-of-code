from pathlib import Path

input_text = Path("../inputs/1.txt").read_text()


# Trie implementation
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_word = True

    def search(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_word

    def starts_with(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True

    def __repr__(self):
        return str(self.children)


digits = {
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
}

words_to_number = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def text_to_number(text):
    if text.isdigit():
        return int(text)
    return words_to_number[text]


if __name__ == '__main__':
    trie = TrieNode()
    possible_lengths = {len(digit) for digit in digits}
    for digit in digits:
        trie.insert(digit)

    total = 0
    for line in input_text.splitlines():
        # print(f"LINE: {line}")
        left = 0
        right = len(line) - 1
        left_token = ""
        right_token = ""
        while left < len(line):
            for length in possible_lengths:
                if trie.search(line[left:left + length]):
                    left_token = line[left:left + length]
                    # print(f"FOUND LEFT:\t{left_token}")
                    left += length
                    break
            if left_token:
                break
            left += 1

        while right >= 0:
            for length in possible_lengths:
                if trie.search(line[right - length + 1:right + 1]):
                    right_token = line[right - length + 1:right + 1]
                    # print(f"FOUND RIGHT:\t{right_token}")
                    right -= length
                    break
            if right_token:
                break
            right -= 1

        total += int(str(text_to_number(left_token)) + str(text_to_number(right_token)))

    print(total)
