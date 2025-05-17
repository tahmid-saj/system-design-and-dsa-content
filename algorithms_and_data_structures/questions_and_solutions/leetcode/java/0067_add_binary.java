class Solution {
    public String addBinary(String a, String b) {
        StringBuilder res = new StringBuilder();
        boolean endA = false, endB = false;
        int carry = 0, i = a.length() - 1, j = b.length() - 1;

        while (!endA || !endB) {
            char digitA = a.charAt(i), digitB = b.charAt(j);

            if (endA == true) digitA = '0';
            if (endB == true) digitB = '0';

            if (carry == 0) {
                if (digitA == '0' && digitB == '0') {
                    res.append('0');
                } else if ((digitA == '1' && digitB == '0') || (digitA == '0' && digitB == '1')) {
                    res.append('1');
                } else if (digitA == '1' && digitB == '1') {
                    res.append('0');
                    carry = 1;
                }
            } else if (carry == 1) {
                if (digitA == '0' && digitB == '0') {
                    res.append('1');
                    carry = 0;
                } else if ((digitA == '1' && digitB == '0') || (digitA == '0' && digitB == '1')) {
                    res.append('0');
                } else if (digitA == '1' && digitB == '1') {
                    res.append('1');
                }
            }

            if (i == 0) endA = true;
            else i--;
            if (j == 0) endB = true;
            else j--;
        }

        if (carry == 1) res.append('1');

        return res.reverse().toString();
    }
}