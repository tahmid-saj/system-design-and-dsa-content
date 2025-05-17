class Solution:
    def letterCasePermutation(self, s: str) -> List[str]:
        permutations = []
        permutations.append(s)

        for i in range(0, len(s)):
            if s[i].isalpha():
                for j in range(0, len(permutations)):
                    permutation = list(permutations[j])
                    permutation[i] = permutation[i].swapcase()
                    permutations.append("".join(permutation))
        
        return permutations