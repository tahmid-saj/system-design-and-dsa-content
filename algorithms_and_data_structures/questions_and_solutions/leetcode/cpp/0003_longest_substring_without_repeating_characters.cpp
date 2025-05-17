class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int length = 0, currLength = 0;
        unordered_map<char, int> substring;

        if (s == string("")) {
            return 0;
        }

        for (int i = 0; i < s.size(); i++) {
            if (substring.find(s[i]) == substring.end()) {
                substring.insert(substring.end(), make_pair(s[i], i));
                currLength++;
            }
            else if (substring.find(s[i]) != substring.end()) {

                i = substring.find(s[i])->second;
                substring.clear();


                if (length < currLength) {
                    length = currLength;
                }

                currLength = 0;
            }

            if (length < currLength && (i + 1 == s.size())) {
                length = currLength;

            }
        }

        return length;
    }
};