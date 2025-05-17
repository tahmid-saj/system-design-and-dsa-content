class Solution {
    public List<String> readBinaryWatch(int turnedOn) {
        if (turnedOn >= 9) return new ArrayList<String>();
        if (turnedOn == 0) return new ArrayList<String>(Arrays.asList("0:00"));
        List<String> res = new ArrayList<String>();

        for (int h = 0; h < 12; h++) {
            for (int m = 0; m < 60; m++) {
                if (Integer.bitCount(h) + Integer.bitCount(m) == turnedOn) {
                    StringBuilder time = new StringBuilder();
                    time.append(h).append(":");

                    if (m < 10) time.append("0");

                    time.append(m);
                    res.add(time.toString());
                }
            }
        }

        return res;
    }
}