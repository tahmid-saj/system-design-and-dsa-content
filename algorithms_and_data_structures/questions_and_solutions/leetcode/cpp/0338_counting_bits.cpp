class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> ans(n + 1, 0);

        for (int i = 0; i <= n; i++) {
            for (int j = i; j >= 1 && i != 0; j /= 2) {
                if (j % 2 != 0) {
                    ans[i] += 1;
                }
            }
        }

        return ans;
    }
};