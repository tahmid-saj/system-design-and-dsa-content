class Solution {
    public int[] plusOne(int[] digits) {
        int carry = 1;
    
        if (digits[digits.length - 1] < 9) {
            digits[digits.length - 1] += 1;
            return digits;
        }

        for (int i = digits.length - 1; i >= 0; i--) {
            if (digits[i] == 9) digits[i] = 0;
            else if (digits[i] < 9 && carry == 1) {
                digits[i] += 1;
                carry = 0;
            }

            if (carry == 0) return digits;
            if (i == 0) {
                digits = new int[digits.length + 1];
                digits[0] = 1;
            }
        }

        return digits;
    }
}