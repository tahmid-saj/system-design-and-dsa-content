class Solution {
    public boolean isSubsequence(String s, String t) {
        if (s.length() == 0 && t.length() == 0 || (s.length() == 0)) return true;

        for (int i = 0, j = 0; i < s.length() && j < t.length(); ) {
            // if s[i] == j[i]: i++, j++
            // if s[i] != j[i]: j++
            // if i == s.length(): return true
            // return false after loop ends

            if (s.charAt(i) == t.charAt(j)) {
                i++;
                j++;
            } else {
                j++;
            }
            if (i == s.length()) return true;
        }

        return false;
    }
}