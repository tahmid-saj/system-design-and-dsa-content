class Solution {
public:
    bool isPalindrome(string s) {
        for (int i = 0, j = s.size() - 1; i <= j; ) {
            if ((tolower(s[i]) < 97 || tolower(s[i]) > 122) && !(tolower(s[i]) >= 48 && tolower(s[i]) <= 57)) {
                i++;
                continue;
            }

            if ((tolower(s[j]) < 97 || tolower(s[j]) > 122) && !(tolower(s[j]) >= 48 && tolower(s[j]) <= 57)) {
                j--;
                continue;
            }

            if (s.size() == 1) {
                return true;
            }

            if (tolower(s[i]) == tolower(s[j])) {
                i++; j--;
            }
            else if (tolower(s[i]) != tolower(s[j])) {
                return false;
            }
        }

        return true;
    }
};