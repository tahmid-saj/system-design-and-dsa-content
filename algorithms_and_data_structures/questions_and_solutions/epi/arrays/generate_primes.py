class Solution:
    def generatePrimes(self, n):
        primes, isPrime = [], [False, False] + [True] * (n - 1)
        for i in range(2, n + 1):
            if isPrime[i]:
                primes.append(i)
                for j in range(i * 2, n + 1, i): isPrime[j] = False
        
        return primes

# time: O(nlog(logn))
# space: O(n)   space