class Solution {
    public int longestPalindrome(String s) {
        if (s.length() == 1) return 1;

        // sort the string -> convert into a char[] letters
        // loop through letters:
        // lastIndex = letters.lastIndexOf(letters[i])
        // if (lastIndex - i % 2 == 0 && lastIndex != i): res += lastIndex - i + 1
        // if (lastIndex - i % 2 != 0 && lastIndex - i > largestOddLength) largestOddLength = lastIndex - i
        // return res + largestOddLength;

        // char[] letters = s.toCharArray();
        // int largestOddLength = 0, res = 0;
        // Arrays.sort(letters);
        // s = new String(letters);
        // for (int i = 0; i < s.length(); i++) {
        //     int lastIndex = s.lastIndexOf(s.charAt(i));

        //     if ((lastIndex - i + 1) % 2 == 0 && lastIndex != i) res += lastIndex - i + 1;
        //     else if ((lastIndex - i + 1) % 2 != 0 && (lastIndex - i + 1) > largestOddLength) largestOddLength = lastIndex - i + 1;
        //     i = lastIndex;
        // }

        // return res + largestOddLength;

        int oddCount = 0;
        Map<Character, Integer> letterCounts = new HashMap<Character, Integer>();

        for (char letter : s.toCharArray()) {
            letterCounts.put(letter, letterCounts.getOrDefault(letter, 0) + 1);

            if (letterCounts.get(letter) % 2 == 1) oddCount++;
            else if (letterCounts.get(letter) % 2 == 0) oddCount--;
        }

        if (oddCount > 1) return s.length() - oddCount + 1;

        return s.length();
    }
}