class Solution {
    public int maxProfit(int[] prices) {
        int minPrices = Integer.MAX_VALUE, profit = 0;

        for (int i = 0; i < prices.length; i++) {
            if (minPrices > prices[i]) minPrices = prices[i];
            if (profit < prices[i] - minPrices) profit = prices[i] - minPrices;
        }

        return profit;
    }
}