class Solution {
    public String longestCommonPrefix(String[] strs) {
        char currChar = 'a';

        if (strs[0].length() != 0) {
            currChar = strs[0].charAt(0);
        }

        int j = 0, i = 0;
        StringBuilder res = new StringBuilder();

        while (true) {
            if (j > strs[i].length() - 1) {
                break;
            }
            if (i == 0) {
                currChar = strs[i].charAt(j);
            }
            if (i > 0 && strs[i].charAt(j) != currChar) {
                break;
            }
            if (i == strs.length - 1 && strs[i].charAt(j) == currChar) {
                res.append(currChar);
            }

            if (i == strs.length - 1) {
                i = 0;
                j++;
            } else {
                i++;
            }
        }

        return res.toString();
    }
}