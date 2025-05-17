class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        char_count = defaultdict(int)
        
        for char in text: char_count[char] += 1
        
        min_count = float('inf')
        min_count = min(min_count, char_count['b'])
        min_count = min(min_count, char_count['a'])
        min_count = min(min_count, char_count['l'] // 2)
        min_count = min(min_count, char_count['o'] // 2)
        min_count = min(min_count, char_count['n'])
        
        return min_count