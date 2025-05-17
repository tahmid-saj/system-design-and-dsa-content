class Solution {
public:
    bool wordPattern(string pattern, string s) {
        unordered_map<char, string> patterns;
        unordered_set<string> words;
        int i, j;
        
        string str = "";
        s += ' ';
        
        for (i = 0, j = 0; i < s.size(); i++) {
            if (s[i] == ' ') {
                if (patterns.find(pattern[j]) != patterns.end()) {
                    if (patterns.find(pattern[j])->second == str) {
                        j++;
                        str.clear();
                        continue;
                    }
                    else if (patterns.find(pattern[j])->second != str) {
                        return false;
                    }
                }
                else if (patterns.find(pattern[j]) == patterns.end()) {
                    if (words.find(str) != words.end()) {
                        return false;
                    }
                    
                    patterns.insert(make_pair(pattern[j], str));
                    words.insert(str);
                }
                
                j++;
                str.clear();
            }
            else if (s[i] != ' ') {
                str += s[i];
            }
        }
        
        if (j != pattern.size() || i != s.size()) {
            return false;
        }
        
        return true;
    }
};