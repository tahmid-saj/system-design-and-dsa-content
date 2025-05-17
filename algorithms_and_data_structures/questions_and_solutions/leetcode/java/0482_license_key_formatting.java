class Solution {
    public String licenseKeyFormatting(String s, int k) {
        s = s.toUpperCase();
        StringBuilder res = new StringBuilder();
        // loop through s using i from s.length() - 1 to 0, j (0 to k):
        // res.append(s.charAt(i));
        // j++;
        // if (j == k && i != 0):
        //  res.append("-");
        // return res
        int lastChar = 0;
        for (int i = s.length() - 1, j = 0; i >= 0; i--) {
            if (s.charAt(i) != '-') {
                res.append(s.charAt(i));
                j++;
            }
            
            if (j == k && i != 0) {
                res.append("-");
                j = 0;
                lastChar = i;
            }
        }

        if (res.length() != 0 && res.charAt(res.length() - 1) == '-') res.deleteCharAt(res.length() - 1);

        return res.reverse().toString();
    }
}