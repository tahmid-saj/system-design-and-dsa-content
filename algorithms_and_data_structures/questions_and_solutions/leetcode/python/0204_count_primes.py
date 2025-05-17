class Solution:
    def countPrimes(self, n: int) -> int:
        isPrime = [False, False] + [True] * (n - 2)
        for i in range(2, int(sqrt(n)) + 1):
            if isPrime[i]:
                for j in range(i * i, n, i): isPrime[j] = False
        
        return sum(isPrime)