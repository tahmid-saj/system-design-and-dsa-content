class Solution {
    public int hammingDistance(int x, int y) {
        int unique = x ^ y;
        int count = 0;

        while (unique != 0) {
            count++;
            unique &= unique - 1;
        }

        return count;
    }
}