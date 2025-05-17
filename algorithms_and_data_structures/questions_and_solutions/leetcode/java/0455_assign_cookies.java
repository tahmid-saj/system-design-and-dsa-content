class Solution {
    public int findContentChildren(int[] g, int[] s) {
        if (s.length == 0) return 0;
        Arrays.sort(g);
        Arrays.sort(s);

        // loop through g and s using i and j respectively:
        // if (s[j] >= g[i]): res++, i++, j++
        // else if (s[j] < g[i]): j++
        // return res
        int res = 0;
        for (int i = 0, j = 0; i < g.length && j < s.length; ) {
            if (s[j] >= g[i]) {
                res++;
                i++;
                j++;
            } else if (s[j] < g[i]) j++;
        }

        return res;
    }
}