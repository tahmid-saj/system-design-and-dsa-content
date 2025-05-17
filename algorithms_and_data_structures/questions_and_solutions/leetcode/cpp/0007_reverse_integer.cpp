class Solution {
public:
    int reverse(int x) {
        int reverseNum = 0;
        bool negative = false;

        if (x < 0) {
            negative = true;
            x = abs(x);
        }

        while (x != 0 && sizeof(reverseNum) == 4) {
            if ((10 * (long)reverseNum) + (x % 10) > pow(2, 31) - 1 || (10 * (long)reverseNum) + (x % 10) < -1 * pow(2, 31)) {
                return 0;
            }

            reverseNum = (10 * reverseNum) + (x % 10);
            x /= 10;
        }

        if (negative == true) {
            return reverseNum * -1;
        }

        return reverseNum;
    }
};