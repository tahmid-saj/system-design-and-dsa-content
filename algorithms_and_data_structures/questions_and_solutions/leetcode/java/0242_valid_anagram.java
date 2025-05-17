class Solution {
    public boolean isAnagram(String s, String t) {
        char[] sC = s.toCharArray();
        char[] tC = t.toCharArray();
        Arrays.sort(sC);
        Arrays.sort(tC);
        if (sC.length != tC.length) return false;

        for (int i = 0; i < sC.length; i++) {
            if (sC[i] != tC[i]) return false;
        }

        return true;
    }
}