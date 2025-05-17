class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for (vector<int>::reverse_iterator i = digits.rbegin(); i != digits.rend(); i++) {
            if (i == digits.rbegin() && *i != 9) {
                *i += 1;
                return digits;
            }
            else if (*i == 9) {
                *i = 0;

                if (i + 1 == digits.rend()) {
                    digits.insert((i + 1).base(), 1);
                    return digits;
                }
            }
            else if (*i != 9) {
                *i += 1;
                return digits;
            }
        }
        
        return digits;
    }
};