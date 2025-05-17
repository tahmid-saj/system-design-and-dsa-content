class SortByFirstLetter(str):
    def __lt__(a, b):
        return a + b > b + a
class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        nums.sort(key=SortByFirstLetter)
        res = [str(num) for num in nums]
        if res[0] == "0": return "0"
        return "".join(res)