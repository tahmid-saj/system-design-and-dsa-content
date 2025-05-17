class Solution {
    public int countBit(int n) {
        int numBits = 0;

        do {
            numBits += n % 2;
            n /= 2;
        } while (n > 0);

        return numBits;
    }

    public int[] countBits(int n) {
        int[] res = new int[n + 1];

        for (int i = 0; i <= n; i++) {
            res[i] = countBit(i);
        }

        return res;
    }
}