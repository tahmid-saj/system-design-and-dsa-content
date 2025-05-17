/** 
 * Forward declaration of guess API.
 * @param  num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * int guess(int num);
 */

public class Solution extends GuessGame {
    public int guessNumber(int n) {
        int l = 1, r = n, middle = 0;

        while (l <= r) {
            middle = l + (r - l) / 2;
            int res = guess(middle);

            if (res == 0) return middle;
            else if (res == 1) l = middle + 1;
            else if (res == -1) r = middle - 1;
        }

        return l;
    }
}