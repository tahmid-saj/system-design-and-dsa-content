class Solution {
public:
    bool isPowerOfThree(int n) {
        // Recursion way
        if (n == 1) return true;
        if ((n == 0) || (n % 3 != 0)) return false;
        
        return isPowerOfThree(n / 3);
        
        // Loop way
        /*if (n < 0) {
            n *= -1;
        }
        
        for (int i = 0; i < n; i++) {
            if (n == pow(3, i)) {
                return true;
            }
        }
        
        return false;
        */
    }
};
