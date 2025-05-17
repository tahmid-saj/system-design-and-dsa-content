public class Solution {
    // you need treat n as an unsigned value
    public int reverseBits(int n) {
        int rev = 0;

        for (int i = 0; i < 32; i++) {
            rev = rev | (n & 1);
            n >>= 1;

            if (i != 31) {
                rev <<= 1;
            }
        }
        
        return rev;
    }
}