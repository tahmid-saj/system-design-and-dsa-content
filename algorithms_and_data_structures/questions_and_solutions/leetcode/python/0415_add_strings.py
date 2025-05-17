class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        # loop through num1 and num2 using i and j respectively:
        # if i < 0: n1 = 0
        # else: n1 = int(num1[i])
        # if j < 0: n1 = 0
        # else: n2 = int(num2[i])
        # if carry == 0:
        #   if n1 + n2 < 10: res += str((n1 + n2) % 10)
        #   elif  n1 + n2 >= 10: res += str((n1 + n2) % 10), carry = 1
        # if carry == 1:
        #   if carry + n1 + n2 < 10: res += str((carry + n1 + n2) % 10), carry = 0
        #   elif carry + n1 + n2 >= 10: res += str((carry + n1 + n2) % 10)
        # i -= 1, j -= 1
        i, j, carry, res = len(num1) - 1, len(num2) - 1, 0, ""

        while i >= 0 or j >= 0:
            n1, n2 = 0, 0
            if i >= 0: n1 = int(num1[i])
            if j >= 0: n2 = int(num2[j])

            if carry == 0:
                if n1 + n2 < 10: res += str((n1 + n2) % 10)
                elif n1 + n2 >= 10: 
                    res += str((n1 + n2) % 10)
                    carry = 1
            elif carry == 1:
                if carry + n1 + n2 < 10:
                    res += str((carry + n1 + n2) % 10)
                    carry = 0
                elif carry + n1 + n2 >= 10:
                    res += str((carry + n1 + n2) % 10)
            
            i -= 1
            j -= 1

        if carry == 1: res += "1"

        return res[::-1]