/* The isBadVersion API is defined in the parent class VersionControl.
      boolean isBadVersion(int version); */

public class Solution extends VersionControl {
    public int firstBadVersion(int n) {
        if (n == 1) return n;
        int l = 1, r = n, middle = 0;

        while (l <= r) {
            middle = l + (r - l) / 2;
            boolean bad = isBadVersion(middle);

            // false false false true true
            // 1       2      3    4   5

            // if bad == false: l = middle + 1
            // if bad == true: r = middle - 1
            if (bad == false) l = middle + 1;
            if (bad == true) r = middle - 1;
        }

        return l;
    }
}