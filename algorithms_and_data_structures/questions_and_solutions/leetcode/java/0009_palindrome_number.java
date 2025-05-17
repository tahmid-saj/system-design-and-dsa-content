class Solution {
    public boolean isPalindrome(int x) {
        int rev = 0, org = x;

        while (x > 0) {
            rev *= 10;
            rev += (x % 10);
            x /= 10;
        }

        return rev == org;
    }
}