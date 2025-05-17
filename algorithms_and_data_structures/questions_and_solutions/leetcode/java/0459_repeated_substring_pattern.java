class Solution {
    public boolean repeatedSubstringPattern(String s) {
        // 2 loops:
        // first loop through s using i (0 to s.length):
        // take substring of s(0, i + 1)
        // if substring == s: break
        // second loop through s using j (i + 1 to s.length), k from (0 to substring.length):
        //  if (substring[k] != s[j]) k = 0, break;
        //  else if (substring[k] == s[j]): k++
        //  if k == substring.length: k = 0
        //  if j == s.length - 1: return true
        // return false

        for (int i = 0; i < s.length() / 2; i++) {
            String sub = s.substring(0, i + 1);

            for (int j = i + 1, k = 0; j < s.length(); j++) {
                if (sub.charAt(k) != s.charAt(j)) break;
                else if (sub.charAt(k) == s.charAt(j)) k++;

                if (j == s.length() - 1 && k == sub.length()) return true;
                if (k == sub.length()) k = 0;
            }
        }

        return false;
    }
}