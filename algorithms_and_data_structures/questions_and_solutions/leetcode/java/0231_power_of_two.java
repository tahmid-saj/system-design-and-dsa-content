class Solution {
    public boolean isPowerOfTwo(int n) {
        if (n < 1) return false;
        if (n == 1 || n == 2) return true;

        int l = 1, r = n, middle = 0;
        while (l <= r) {
            middle = l + (r - l) / 2;
            if (Math.pow(2, middle) < n) {
                l = middle + 1;
            } else if (Math.pow(2, middle) > n) {
                r = middle - 1;
            } else {
                return true;
            }
        }

        return false;
    }
}