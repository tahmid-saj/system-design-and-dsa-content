class Solution {
    public int[] constructRectangle(int area) {
        int diff = Integer.MAX_VALUE;
        int[] res = new int[2];
        // loop through 1 to area using binary search
        // if area % middle == 0:
        //  if (diff < Math.abs((area / middle) - middle)):
        //  diff = Math.abs((area / middle) - middle)
        //  res[0] = area / middle
        //  res[1] = middle
        // return res

        for (int i = 1; i <= area; i++) {
            if (area % i == 0) {
                if (diff > Math.abs((area / i) - i)) {
                    diff = Math.abs((area / i) - i);
                    res[0] = area / i;
                    res[1] = i;
                }
            }
        }

        return res;
    }
}