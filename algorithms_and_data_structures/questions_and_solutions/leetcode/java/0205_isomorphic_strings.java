class Solution {
    public boolean isIsomorphic(String s, String t) {
        Map<Character, Character> hMap = new HashMap<Character, Character>();

        for (int i = 0; i < s.length(); i++) {
            if (!hMap.containsKey(s.charAt(i))) {
                if (hMap.containsValue(t.charAt(i))) return false;
                else hMap.put(s.charAt(i), t.charAt(i));
            } else {
                if (hMap.get(s.charAt(i)) != t.charAt(i)) return false;
            }
        }

        return true;
    }
}