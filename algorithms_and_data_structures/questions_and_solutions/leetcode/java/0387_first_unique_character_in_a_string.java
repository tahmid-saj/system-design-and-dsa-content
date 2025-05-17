class Solution {
    public int firstUniqChar(String s) {
        // chars contains chars and their first position
        // loop through s using i:
        // if chars doesn't contain s[i] {
        //  add it
        // }
        // if chars contains s[i]: remove it
        // if chars is empty, return -1

        // int lowest = Integer.MAX_VALUE
        // loop through chars.keys
        // if lowest > chars.key: lowest = chars.key
        // return lowest

        Map<Character, Integer> chars = new HashMap<Character, Integer>();
        for (int i = 0; i < s.length(); i++) {
            if (!chars.containsKey(s.charAt(i))) chars.put(s.charAt(i), i);
            else {
                chars.put(s.charAt(i), Integer.MAX_VALUE);
            }
        }

        int lowest = Integer.MAX_VALUE;
        for (char key : chars.keySet()) {
            lowest = Math.min(lowest, chars.get(key));
        }

        return lowest == Integer.MAX_VALUE ? -1 : lowest;

        // loop through s using i:
        // if i == s.lastIndexOf(s[i]) { lowest = Math.min(lowest, i) }
        // return i == MAX_VALUE ? -1 : lowest

        // int lowest = Integer.MAX_VALUE;
        // for (char c = 'a'; c <= 'z'; c++) {
        //     if (s.indexOf(c) != -1 && s.indexOf(c) == s.lastIndexOf(c)) {
        //         lowest = Math.min(lowest, s.indexOf(c));
        //     }
        // }

        // return lowest == Integer.MAX_VALUE ? -1 : lowest;
    }
}