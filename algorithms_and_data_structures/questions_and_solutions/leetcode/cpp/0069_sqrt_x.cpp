class Solution {
public:
    int mySqrt(int x) {
        unsigned int sqrt = 0;

        for (unsigned int i = 0; i <= x; i++) {
            if ((i * i) <= x && ((i + 1) * (i + 1)) > x) {
                sqrt = i;
                return sqrt;
            }
        }

        return sqrt;
    }
};