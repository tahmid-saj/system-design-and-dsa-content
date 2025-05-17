class Solution {
    public boolean wordPattern(String pattern, String s) {
        // patternMap can only cotain:
        // a -> dog, a -> cat x
        // a -> dog, b -> dog yes
        
        // patternMap contains patterns between pattern[i] and sArray[i]
        // look through pattern using i:
        // if pattern[i] is not in hashPattern: add it
        // if pattern[i] is in hashPattern:
        // -> if hashPattern.get(pattern[i]) != sArray[i] return false
        // return true

        Map<Character, String> hashPattern = new HashMap<Character, String>();
        String[] sArray = s.split("\\s+");

        if (sArray.length != pattern.length()) return false;

        for (int i = 0; i < pattern.length(); i++) {
            if (hashPattern.containsKey(pattern.charAt(i)) == false) {
                if (hashPattern.containsValue(sArray[i]) == true) return false;
                hashPattern.put(pattern.charAt(i), sArray[i]);
            } else if (hashPattern.containsKey(pattern.charAt(i)) == true) {
                if (!hashPattern.get(pattern.charAt(i)).equals(sArray[i])) {
                    return false;
                }
            }
        }

        return true;
    }
}