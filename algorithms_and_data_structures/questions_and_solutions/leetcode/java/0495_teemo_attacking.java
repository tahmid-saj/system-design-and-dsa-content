class Solution {
    public int findPoisonedDuration(int[] timeSeries, int duration) {
        int res = 0, prevEnd = Integer.MIN_VALUE;

        for (int i = 0; i < timeSeries.length; i++) {
            if (prevEnd >= timeSeries[i]) {
                res += duration - (prevEnd - timeSeries[i] + 1);
            } else {
                res += duration;
            }
            prevEnd = timeSeries[i] + duration - 1;
        }

        return res;
    }
}