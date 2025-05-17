class Solution(object):
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        # start from the end of s towards the front using i:
        # counting = False initially
        # if counting == False and s[i] is not a space: counting = True, res++
        # elif counting == True and s[i] is not a space: res++
        # elif counting == True and s[i] is a space: break
        # return res
        # edge cases: "   ", "a", "    aaa", "a  "

        res, counting = 0, False
        for i in range(len(s) - 1, -1, -1):
            if s[i] != " ":
                if counting == False:
                    counting = True
                    res += 1
                elif counting == True:
                    res += 1
            elif counting == True and s[i] == " ":
                break
        
        return res