class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }
        
        int reverseNum = 0, i = 1;
        while (x > reverseNum) {
            reverseNum = (reverseNum * 10) + x % 10;
            x /= 10;
        }
        
        if (reverseNum == x || reverseNum / 10 == x) {
            return true;
        }
        
        return false;
    }
};