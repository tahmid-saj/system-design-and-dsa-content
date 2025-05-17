class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        int i = 0, j = 0;

        char[] ran = ransomNote.toCharArray();
        char[] mag = magazine.toCharArray();
        Arrays.sort(ran);
        Arrays.sort(mag);

        while (i < ran.length && j < mag.length) {
            if (mag[j] == ran[i]) {
                j++;
                i++;
            } else if (mag[j] != ran[i]) j++;
        }

        return i == ran.length;
    }
}