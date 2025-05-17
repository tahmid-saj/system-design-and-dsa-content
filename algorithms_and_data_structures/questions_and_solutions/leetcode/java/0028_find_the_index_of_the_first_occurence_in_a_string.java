class Solution {
    public int strStr(String haystack, String needle) {
        int j = 0, firstOccur = 0;

        for (int i = 0; i < haystack.length(); i++) {
            if (haystack.charAt(i) == needle.charAt(j)) {
                if (j == 0) firstOccur = i;
                j++;
            } else if (haystack.charAt(i) != needle.charAt(j) && j > 0) {
                i = firstOccur;
                j = 0;
            }

            if (j == needle.length()) {
                return firstOccur;
            }
        }

        return -1;
    }
}