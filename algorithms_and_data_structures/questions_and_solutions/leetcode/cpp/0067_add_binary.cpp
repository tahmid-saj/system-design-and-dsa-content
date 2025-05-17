class Solution {
public:
    string addBinary(string a, string b) {
        int bitMax, carry = 0;
        string result;

        if (a.size() >= b.size()) {
            bitMax = a.size();
            string zeros = std::string(bitMax - b.size(), '0');
            b.insert(0, zeros);
        }
        else if (a.size() < b.size()) {
            bitMax = b.size();
            string zeros = std::string(bitMax - a.size(), '0');
            a.insert(0, zeros);
        }

        reverse(a.begin(), a.end());
        reverse(b.begin(), b.end());

        for (int i = 0; i < bitMax; i++) {
            if (a[i] == '0' && b[i] == '0') {
                if (carry == 1) {
                    result += '1';
                    carry = 0;
                }
                else if (carry == 0) {
                    result += '0';
                }
            }
            else if (a[i] == '0' && b[i] == '1') {
                if (carry == 1) {
                    result += '0';

                    if (i == bitMax - 1) {
                        result += '1';
                    }
                }
                else if (carry == 0) {
                    result += '1';
                }
            }
            else if (a[i] == '1' && b[i] == '0') {
                if (carry == 1) {
                    result += '0';

                    if (i == bitMax - 1) {
                        result += '1';
                    }
                }
                else if (carry == 0) {
                    result += '1';
                }
            }
            else if (a[i] == '1' && b[i] == '1') {
                if (carry == 1) {
                    result += '1';

                    if (i == bitMax - 1) {
                        result += '1';
                    }
                }
                else if (carry == 0) {
                    result += '0';
                    carry = 1;
                    
                    if (i == bitMax - 1) {
                        result += '1';
                    }
                }
            }
        }

        reverse(result.begin(), result.end());

        return result;
    }
};