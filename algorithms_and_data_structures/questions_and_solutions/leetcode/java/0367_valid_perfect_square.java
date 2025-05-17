class Solution {
    public boolean isPerfectSquare(int num) {
        if (num == 1) return true;

        int l = 1, r = num, middle = 0;
        while (l <= r) {
            middle = l + (r - l) / 2;
            double val = (num * 1.0) / (middle * 1.0);

            if (val == middle) {
                return true;
            } else if (middle < val) {
                l = middle + 1;
            } else if (val < middle) {
                r = middle - 1;
            }
        }

        return false;
    }
}