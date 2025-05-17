class Solution {
    public int arrangeCoins(int n) {
        // n = 5: 1, 2, 3 -> (n - i (i goes from 1...inf while n >= i))
        // if n >= i: res++
        // return res 
        int i = 1, res = 0;
        while (n >= i) {
            if (n >= i) res++;
            n -= i;
            i++;
        }

        return res;
    }
}