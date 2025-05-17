class Solution(object):
    def convertToTitle(self, columnNumber):
        """
        :type columnNumber: int
        :rtype: str
        """
        # 28 / 26 = 1 -> A  -> 28 % 26 = 2
        # 2 = 2 -> B
        # 701 / 26 = 26.96 ~ 26 -> 701 % 26 = 25
        # 25  = 25

        # 1 % 26 = 1 -> A  --> 1 / 26 = 0
        # 28 % 26 = 2 -> B --> 28 / 26 = 1 % 26 -> A
        # 701 % 26 = 25 -> Y --> 701 / 26 = 26 % 26 -> Z
        # while columnNumber > 0:
        # if columnNumber <= 26: letterNum = columnNumber
        # else: letterNum = columnNumber % 26
        # res += letterToNum[letterNum]
        # columnNumber /= 26
        # return res

        letterToNum = { 
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E",
            6: "F",
            7: "G",
            8: "H",
            9: "I",
            10: "J",
            11: "K",
            12: "L",
            13: "M",
            14: "N",
            15: "O",
            16: "P",
            17: "Q",
            18: "R",
            19: "S",
            20: "T",
            21: "U",
            22: "V",
            23: "W",
            24: "X",
            25: "Y",
            26: "Z"
        }
        letterNum, res = 0, ""

        while columnNumber > 0:
            letterNum = columnNumber % 26

            if letterNum == 0:
                res += "Z"
                columnNumber -= 26
            else:
                res += letterToNum[letterNum]
                columnNumber -= letterNum

            columnNumber //= 26
        
        return res[::-1]
        # 52 % 26 = 2 -> B, 52 // 26 = 2
        # 2 -> B
        