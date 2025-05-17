class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        # 000111

        # Initialize variables
        pre_len = 0
        cur_len = 1
        count = 0
        
        # Traverse through the string
        for i in range(1, len(s)):
            # If the current character is the same as the previous character
            if s[i] == s[i-1]:
                cur_len += 1
            # If the current character is different from the previous character
            else:
                pre_len = cur_len
                cur_len = 1
                
            # If the previous length is greater than or equal to the current length
            # then we have a valid substring
            if pre_len >= cur_len:
                count += 1
        
        # Return the total count of valid substrings
        return count