class LLStack {
public:
    LLStack() {

    }

    bool isEmpty() const {
        return lst.empty();
    }
    
    char topE1() {
        return lst.back();
    }

    char pop() {
        char el = lst.back();
        lst.pop_back();
        return el;
    }

    void push(char el) {
        lst.push_back(el);
        //cout << el;
    }

private:
    list<char> lst;
};

class Solution {
public:
    bool isValid(string s) {
        bool valid = false, containsRight = false;
        char parentheses1 = '{', parentheses2 = '(', parentheses3 = '[';
        char parentheses4 = '}', parentheses5 = ')', parentheses6 = ']';

        LLStack stk;

        for (int iB = 0; iB < s.length(); iB++) {
            if (s[iB] == parentheses1 || s[iB] == parentheses2 || s[iB] == parentheses3) {
                stk.push(s[iB]);
                containsRight = true;
                continue;
            }

            if (!stk.isEmpty()) {

                if ((s[iB] == parentheses4 && stk.topE1() == '{') || (s[iB] == parentheses5 && stk.topE1() == '(') || (s[iB] == parentheses6 && stk.topE1() == '[')) {
                    stk.pop();
                }
                else {
                    return false;
                }
            } else {
                return false;
            }
        }
        
        if (stk.isEmpty() && !s.empty() && containsRight && s[0] != parentheses4 && s[0] != parentheses5 && s[0] != parentheses6) {
            valid = true;
        }

        return valid;
        
    }
};