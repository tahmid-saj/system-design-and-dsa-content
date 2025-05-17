class Solution {
public:
    bool isPerfectSquare(int num) {
        if (num == 1) {
            return true;
        }
        
        for (int i = 1; i <= num / 2; i++) {
            if (long(long(i) * long(i)) == long(num)) {
                return true;
            }
        }
        
        return false;
    }
};