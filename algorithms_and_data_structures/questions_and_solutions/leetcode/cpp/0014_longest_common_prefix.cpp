class Solution {
public:
    string commonPrefix(string left, string right) {
        int minStr = std::min(left.size(), right.size());
        
        for (int i = 0; i < minStr; i++) {
            if (left[i] != right[i]) {
                return left.substr(0, i);
            }
        }
        
        return left.substr(0, minStr);
    }
    
    string longestCommonPrefixHelper(vector<string>& strs, int l, int r) {
        string lcpLeft, lcpRight;
        
        if (l == r) {
            return strs[l];
        }
        else if (l != r) {
            int mid = (l + r) / 2;
            lcpLeft = longestCommonPrefixHelper(strs, l, mid);
            lcpRight = longestCommonPrefixHelper(strs, mid + 1, r);
        }
        
        return commonPrefix(lcpLeft, lcpRight);
    }
    
    string longestCommonPrefix(vector<string>& strs) {
        if (strs.size() == 0) {
            return "";
        }
        
        return longestCommonPrefixHelper(strs, 0, strs.size() - 1);
    }
};