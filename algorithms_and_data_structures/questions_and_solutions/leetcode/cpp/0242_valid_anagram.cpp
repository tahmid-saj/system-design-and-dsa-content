class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) {
            return false;
        }
        
        unordered_multiset<char> lettersS;
        
        for (int i = 0; i < s.size(); i++) {
            lettersS.insert(s[i]);
        }
        
        for (int i = 0; i < t.size(); i++) {
            if (lettersS.find(t[i]) != lettersS.end()) {
                lettersS.erase(lettersS.find(t[i]));
            }
            else {
                return false;
            }
        }
        
        return true;
    }
};