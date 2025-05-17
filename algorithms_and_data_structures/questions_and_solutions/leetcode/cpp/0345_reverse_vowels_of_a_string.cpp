class Solution {
public:
    string reverseVowels(string s) {
        set<char> vowels={'a','e','i','o','u','A','E','I','O','U'};
        stack<char> stack;
        for(char c:s)
        {
            if(vowels.count(c)) stack.push(c);
        }
        for(char& c:s)
        {
            if(vowels.count(c)) 
            {
                c=stack.top();
                stack.pop();
            }
        }
        return s;
    }
};