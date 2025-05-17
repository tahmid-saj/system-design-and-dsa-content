class Solution {
    public String addStrings(String num1, String num2) {
        StringBuilder res = new StringBuilder();
        int len1 = num1.length(), len2 = num2.length();
        int val1 = 0, val2 = 0, carry = 0;

        for (int i = len1 - 1, j = len2 - 1; i >= 0 || j >= 0; i--, j--) {
            if (i < 0) val1 = 0;
            else if (i >= 0) val1 = Integer.valueOf(String.valueOf(num1.charAt(i)));

            if (j < 0) val2 = 0;
            else if (j >= 0) val2 = Integer.valueOf(String.valueOf(num2.charAt(j)));

            int val = (val1 + val2 + carry) % 10;

            if (carry == 0) {
                if (val1 + val2 > 9) carry = 1;
                res.append(val);
            } else if (carry == 1) {
                if (val1 + val2 + carry < 10) carry = 0;
                res.append(val);
            }
        }

        if (carry == 1) res.append("1");
        return res.reverse().toString();
    }
}