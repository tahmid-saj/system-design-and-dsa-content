class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int profit = 0, minPrice = pow(10, 4);

        for (int i = 0; i < prices.size(); i++) {
            if (prices[i] < minPrice) {
                minPrice = prices[i];
                continue;
            }

            if (profit < prices[i] - minPrice) {
                profit = prices[i] - minPrice;
            }
        }

        return profit;
    }
};