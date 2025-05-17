class Solution {
    public int romanToInt(String s) {
        int res = 0;
        Map<Character, Integer> romanNums = new HashMap<>();
        romanNums.put('I', 1);
        romanNums.put('V', 5);
        romanNums.put('X', 10);
        romanNums.put('L', 50);
        romanNums.put('C', 100);
        romanNums.put('D', 500);
        romanNums.put('M', 1000);

        for (int i = 0; i < s.length(); i++) {
            int numVal = romanNums.get(s.charAt(i));
            if (i + 1 < s.length() && numVal < romanNums.get(s.charAt(i + 1))) {
                res += romanNums.get(s.charAt(i + 1)) - numVal;
                i++;
            } else {
                res += romanNums.get(s.charAt(i));
            }
        }

        return res;
    }
}