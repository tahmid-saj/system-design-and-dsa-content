class Solution(object):
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        # carry = 0
        # loop through a, b using i and j respectively while i != -1 or j != -1:
        # aDigit = i == -1 ? 0 : a[i]
        # bDigit = j == -1 ? 0 : b[i]
        # -> if carry == 0:
        #       if aDigit + bDigit < 10: res += (str)(aDigit + bDigit)
        #       elif aDigit + bDigit >= 10: res += (str)((aDigit + bDigit) % 10), carry = 1
        # -> if carry == 1:
        #       if aDigit + bDigit + carry < 10: res += (str)(aDigit + bDigit + carry), carry = 0
        #       elif aDigit + bDigit + carry >= 10: res += (str)((aDigit + bDigit + carry) % 10)
        # if carry == 1: res += 1
        # return res.reverse()
        carry, res = 0, ""
        i, j = len(a) - 1, len(b) - 1

        while i >= 0 or j >= 0:
            aDigit = "0" if i < 0 else a[i]
            bDigit = "0" if j < 0 else b[j]

            if carry == 0:
                if aDigit == "0" and bDigit == "0": res += "0"
                elif (aDigit == "1" and bDigit == "0") or (aDigit == "0" and bDigit == "1"): res += "1"
                elif aDigit == "1" and bDigit == "1":
                    res += "0"
                    carry = 1
            elif carry == 1:
                if aDigit == "0" and bDigit == "0": 
                    res += "1"
                    carry = 0
                elif (aDigit == "1" and bDigit == "0") or (aDigit == "0" and bDigit == "1"):
                    res += "0"
                elif aDigit == "1" and bDigit == "1":
                    res += "1"
            i -= 1
            j -= 1
        
        if carry == 1: res += "1"
        return res[::-1]