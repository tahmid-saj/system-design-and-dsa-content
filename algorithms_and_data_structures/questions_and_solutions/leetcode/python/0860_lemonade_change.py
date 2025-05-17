class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        five = ten = 0
        for num in bills:
            if num == 10:
                if five <= 0: return False
                five -= 1
                ten += 1
                continue
            elif num == 20:
                if five >= 1 and ten >= 1:
                    five -= 1
                    ten -= 1
                elif five >= 3: five -= 3
                else: return False
            else: five += 1
        return True