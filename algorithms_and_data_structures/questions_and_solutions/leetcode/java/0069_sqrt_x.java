class Solution {
    public int mySqrt(int x) {
        if (x == 0) return 0;
        if (x == 1) return 1;

        int low = 0, high = x, middle = 0;

        while (low <= high) {
            middle = low + (high - low) / 2;

            if (x / middle == middle) return middle;
            else if (x / middle < middle) high = middle - 1;
            else if (x / middle > middle) low = middle + 1;
        }

        return low - 1;
    }
}