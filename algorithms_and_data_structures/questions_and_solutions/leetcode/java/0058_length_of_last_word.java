class Solution {
    public int lengthOfLastWord(String s) {
        int res = 0;
        boolean counting = false;

        for (int i = s.length() - 1; i >= 0; i--) {
            if (s.charAt(i) != ' ') {
                if (counting == false) {
                    counting = true;
                }
                if (counting == true) res++;
            } else if ((s.charAt(i) == ' ' || i == 0) && counting == true) {
                return res;
            }
        }

        return res;
    }
}