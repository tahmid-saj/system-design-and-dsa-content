class Solution {
    public String convertToTitle(int columnNumber) {
        Map<Integer, String> alphabet = new HashMap<Integer, String>();
        alphabet.put(1, "A");
        alphabet.put(2, "B");
        alphabet.put(3, "C");
        alphabet.put(4, "D");
        alphabet.put(5, "E");
        alphabet.put(6, "F");
        alphabet.put(7, "G");
        alphabet.put(8, "H");
        alphabet.put(9, "I");
        alphabet.put(10, "J");
        alphabet.put(11, "K");
        alphabet.put(12, "L");
        alphabet.put(13, "M");
        alphabet.put(14, "N");
        alphabet.put(15, "O");
        alphabet.put(16, "P");
        alphabet.put(17, "Q");
        alphabet.put(18, "R");
        alphabet.put(19, "S");
        alphabet.put(20, "T");
        alphabet.put(21, "U");
        alphabet.put(22, "V");
        alphabet.put(23, "W");
        alphabet.put(24, "X");
        alphabet.put(25, "Y");
        alphabet.put(26, "Z");

        String res = "";

        while (columnNumber > 0) {
            int tmp = columnNumber % 26;

            if (tmp == 0) {
                res += "Z";
            } else {
                res += alphabet.get(tmp);
            }

            if (tmp != 0) {
                columnNumber -= tmp;
            } else {
                columnNumber -= 26;
            }

            columnNumber /= 26;
        }

        return (new StringBuilder(res)).reverse().toString();
    }
}