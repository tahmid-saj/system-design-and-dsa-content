class Solution {
    public String reverseVowels(String s) {
        // char[] sArray = s.toCharArray();
        // loop through s using i = 0, j = s.length() - 1, while i <= j:
        // if s[i] is not a vowel: i++
        // if s[j] is not a vowel: j++
        // if s[i] is a vowel and s[j] is a vowel: swap, i++, j--

        char[] sArray = s.toCharArray();
        int i = 0, j = sArray.length - 1;
        while (i <= j) {
            if ((sArray[i] == 'a' || sArray[i] == 'e' || sArray[i] == 'i' || sArray[i] == 'o' || sArray[i] == 'u'
            || sArray[i] == 'A' || sArray[i] == 'E' || sArray[i] == 'I' || sArray[i] == 'O' || sArray[i] == 'U') &&
            (sArray[j] == 'a' || sArray[j] == 'e' || sArray[j] == 'i' || sArray[j] == 'o' || sArray[j] == 'u'
            || sArray[j] == 'A' || sArray[j] == 'E' || sArray[j] == 'I' || sArray[j] == 'O' || sArray[j] == 'U')) {
                char tmpI = sArray[i];
                sArray[i] = sArray[j];
                sArray[j] = tmpI;
                i++;
                j--;
            } else if (sArray[i] == 'a' || sArray[i] == 'e' || sArray[i] == 'i' || sArray[i] == 'o' || sArray[i] == 'u'
            || sArray[i] == 'A' || sArray[i] == 'E' || sArray[i] == 'I' || sArray[i] == 'O' || sArray[i] == 'U') {
                j--;
            } else if (sArray[j] == 'a' || sArray[j] == 'e' || sArray[j] == 'i' || sArray[j] == 'o' || sArray[j] == 'u'
            || sArray[j] == 'A' || sArray[j] == 'E' || sArray[j] == 'I' || sArray[j] == 'O' || sArray[j] == 'U') {
                i++;
            } else {
                i++;
                j--;
            }
        }

        return new String(sArray);
    }
}