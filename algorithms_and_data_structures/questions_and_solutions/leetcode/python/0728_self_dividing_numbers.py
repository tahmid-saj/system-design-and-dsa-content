class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> List[int]:
        def selfDividing(n):
            for num in str(n):
                if num == "0" or n % int(num) != 0: return False
            return True
        
        res = []
        for i in range(left, right + 1):
            if selfDividing(i): res.append(i)
        return res