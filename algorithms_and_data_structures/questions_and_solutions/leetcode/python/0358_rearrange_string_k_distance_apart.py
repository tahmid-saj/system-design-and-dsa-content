class Solution:
    def rearrangeString(self, s: str, k: int) -> str:
        if k <= 1: 
            return s

        charFrequencyMap = {}
        for char in s: charFrequencyMap[char] = charFrequencyMap.get(char, 0) + 1

        maxHeap = []
        # add all characters to the max heap
        for char, frequency in charFrequencyMap.items(): heappush(maxHeap, (-frequency, char))

        queue = deque()
        resultString = []
        while maxHeap:
            frequency, char = heappop(maxHeap)
            frequency = -1 * frequency
            # append the current character to the result string and decrement its count
            resultString.append(char)
            # decrement the frequency and append to the queue
            queue.append((char, frequency - 1))
            if len(queue) == k:
                char, frequency = queue.popleft()
                if frequency > 0:
                    heappush(maxHeap, (-1 * frequency, char))

        # if we were successful in appending all the characters to the result string, return it
        return ''.join(resultString) if len(resultString) == len(s) else ""