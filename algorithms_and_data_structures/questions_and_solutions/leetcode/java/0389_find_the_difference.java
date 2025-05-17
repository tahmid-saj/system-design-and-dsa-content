class Solution {
    public char findTheDifference(String s, String t) {
        if (s.length() == 0) return t.charAt(0);

        Map<Character, Integer> letters = new HashMap<Character, Integer>();
        for (int i = 0; i < s.length(); i++) {
            if (!letters.containsKey(s.charAt(i))) letters.put(s.charAt(i), 1);
            else {
                letters.put(s.charAt(i), letters.get(s.charAt(i)) + 1);
            } 
        }

        char res = ' ';
        for (int i = 0; i < t.length(); i++) {
            if (letters.containsKey(t.charAt(i))) {
                if (letters.get(t.charAt(i)) == 1) {
                    letters.remove(t.charAt(i));
                } else {
                    letters.put(t.charAt(i), letters.get(t.charAt(i)) - 1);
                }
            } else {
                return t.charAt(i);
            }
        }

        return res;
    }
}