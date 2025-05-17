class Solution:
    def arrangeCoins(self, n: int) -> int:
        # coins = 1
        # rows = 0
        # while n > 0:
        # n -= coins
        # if n >= 0: rows += 1
        # coins += 1
        # return rows
        coins, rows = 1, 0
        while n > 0:
            n -= coins
            if n >= 0: rows += 1
            coins += 1

        return rows