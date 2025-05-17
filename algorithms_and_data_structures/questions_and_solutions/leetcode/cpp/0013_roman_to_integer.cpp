class Solution {
public:
    int romanToInt(string s) {
        map<char, int> symbols = {{'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}};
        int sum = 0;
        
        // Loop through s
        
        // if map(s[i]) < map(s[i + 1]) then it is an exception, so the number returned
        // should be map(s[i + 1]) - map(s[i])
        // increment i, and continue
        
        // if map(s[i]) >= map(s[i + 1]) then it is not an exception, so just return the
        // value of map(s[i]) and continue 
        
        for (int i = 0; i < s.size(); i++) {
            if (symbols.find(s[i])->second < symbols.find(s[i + 1])->second) {
                sum += symbols.find(s[i + 1])->second - symbols.find(s[i])->second;
                i++;
                continue;
            }
            else if (symbols.find(s[i])->second >= symbols.find(s[i + 1])->second) {
                sum += symbols.find(s[i])->second;
                continue;
            }
        }
        
        return sum;
    }
};