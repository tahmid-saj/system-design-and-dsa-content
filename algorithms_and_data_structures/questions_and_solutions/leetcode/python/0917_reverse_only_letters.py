class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        arr = list(s)
        i, j = 0, len(arr) - 1
        while i < j:
            while i < j and not arr[i].isalpha(): i += 1
            while i < j and not arr[j].isalpha(): j -= 1
            if i < j: arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        return "".join(arr)