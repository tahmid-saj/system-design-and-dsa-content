class Solution:
    def testCollatzConjecture(self, n):
        verified = set()

        for i in range(3, n + 1):
            sequence = set()
            test_i = i
            while test_i >= i:
                if test_i in sequence: return False
                sequence.add(test_i)
                if test_i % 2:
                    if test_i in verified: break
                    verified.add(test_i)
                    test_i = 3 * test_i + i
                else: test_i //= 2
        
        return True