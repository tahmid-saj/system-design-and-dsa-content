class Solution {
    public boolean isPowerOfThree(int n) {
        if (n <= 0 || n == 2147483647) return false;
        if (n == 1) return true;

        int l = 1, r = n / 2, middle = 0;

        while (l <= r) {
            middle = l + (r - l) / 2;
            int res = (int)Math.pow(3, middle);

            if (res == n) {
                return true;
            } else if (res < n) {
                l = middle + 1;
            } else if (res > n) {
                r = middle - 1;
            }
        }

        return false;
    }
}