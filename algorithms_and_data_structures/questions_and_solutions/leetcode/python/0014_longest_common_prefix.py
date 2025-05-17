class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if strs[0] == "":
            return ""
        
        prefix = strs[0]
        # loop through str in strs[1:]
        # -> while str.find(prefix) != 0:
        # ->    prefix = prefix[:-1]
        # ->    if prefix == "":
        # ->        return ""
        # return prefix
        for string in strs[1:]:
            while string.find(prefix) != 0:
                prefix = prefix[:-1]
                if prefix == "":
                    return ""
        return prefix