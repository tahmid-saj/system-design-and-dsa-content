class Solution:
    def similarRGB(self, color: str) -> str:
        def findTarget(s):
            num = int(s, 16)
            n = round(num / 17)
            return hex(n)[-1] * 2
        
        res = ["#"]
        for i in range(1, len(color), 2):
            res.append(findTarget(color[i:i + 2]))
        return "".join(res)