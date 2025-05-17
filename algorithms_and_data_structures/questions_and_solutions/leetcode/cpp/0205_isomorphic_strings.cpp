class Solution {
public:
    bool isIsomorphic(string s, string t) {
        unordered_map<char, char> letterMap;
        unordered_set<char> mappedToLetters;

        for (int i = 0; i < s.size(); i++) {
            auto itMap = letterMap.find(s[i]);

            if (itMap == letterMap.end()) {
                if (mappedToLetters.find(t[i]) != mappedToLetters.end()) {
                    return false;
                }

                auto insertTmp = std::make_pair(s[i], t[i]);
                letterMap.insert(insertTmp);
                mappedToLetters.insert(t[i]);
                continue;
            }
            else {
                if (itMap->second == t[i]) {
                    continue;
                }
                else {
                    return false;
                }
            }
        }

        return true;
    }
};