class Solution:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        # return self.groupShiftFromFirstLetter(strings)
        return self.groupAdjacentLetterShift(strings)

    def groupShiftFromFirstLetter(self, strings):
        # use a hash map with keys representing shift of letters in strings[i] with respect to the first letter in strings[i]
        # the values in the hash map will be strings[i]
        groups = defaultdict(list)
        for string in strings:
            hashKey = self.hashFunction(string)
            groups[hashKey].append(string)
        return groups.values()

    def shiftLetter(self, firstLetter, letter):
        first, curr = ord(firstLetter), ord(letter)
        return chr((curr - first) % 26 + ord("a"))

    def hashFunction(self, string):
        res = []
        for letter in string: res.append(self.shiftLetter(string[0], letter))
        return "".join(res)
    
    def groupAdjacentLetterShift(self, strings):
        groups = defaultdict(list)
        for string in strings:
            hashKey = self.hashFunction2(string)
            groups[hashKey].append(string)
        return groups.values()
    
    def hashFunction2(self, string):
        res = []
        for i in range(len(string) - 1): res.append(chr((ord(string[i + 1]) - ord(string[i])) % 26 + ord("a")))
        return "".join(res)