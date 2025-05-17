class Solution {
    public int addDigits(int num) {
        // if num < 10 return num
        // add all the digits of num
        // if digit is < 10, return digit
        // addDigits(digit)

        if (num < 10) return num;

        int digit = 0;
        while (num > 0) {
            digit += num % 10;
            num /= 10;
        }

        if (digit < 10) return digit;
        return addDigits(digit);
    }
}