class Solution {
    public int countSegments(String s) {
        if (s.length() == 1 && s.charAt(0) == ' ') return 0;
        if (s.length() == 1) return 1;

        boolean counting = false;
        int res = 0;

        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ' && !counting) {
                counting = true;
                if (i == s.length() - 1) res++;
            } else if ((s.charAt(i) == ' ' || i == s.length() - 1) && counting) {
                counting = false;
                res++;
            }
        }

        return res;
    }
}