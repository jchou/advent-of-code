"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

"""

from pathlib import Path

input_text = Path("../inputs/01.txt").read_text()


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
