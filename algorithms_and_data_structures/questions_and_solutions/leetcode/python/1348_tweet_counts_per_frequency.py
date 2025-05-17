from sortedcontainers import SortedList

class OrderedMap:
    def __init__(self):
        self.map = {}
    
    def add(self, tweetName, time):
        if tweetName not in self.map: self.map[tweetName] = SortedList()
        self.map[tweetName].add(time)
    
    def getCountsPerFreq(self, freq, tweetName, startTime, endTime):
        if endTime < self.map[tweetName][0]: return [0] * math.ceil((endTime - startTime) / freq)
        if startTime > self.map[tweetName][-1]: return [0] * math.ceil((endTime - startTime) / freq)
        i = 0
        while self.map[tweetName][i] < startTime: i += 1

        res = []
        for start in range(startTime, endTime + 1, freq):
            end = start + freq - 1
            if end > endTime: end = endTime

            curr = 0
            while i < len(self.map[tweetName]) and self.map[tweetName][i] >= start and self.map[tweetName][i] <= end:
                curr += 1
                i += 1
            res.append(curr)

        return res

class TweetCounts:

    def __init__(self):
        self.om = OrderedMap()
        self.freqInterval = {
            "minute": 60,
            "hour": 3600,
            "day": 86400
        }

    def recordTweet(self, tweetName: str, time: int) -> None:
        self.om.add(tweetName, time)

    def getTweetCountsPerFrequency(self, freq: str, tweetName: str, startTime: int, endTime: int) -> List[int]:
        return self.om.getCountsPerFreq(self.freqInterval[freq], tweetName, startTime, endTime)


# Your TweetCounts object will be instantiated and called as such:
# obj = TweetCounts()
# obj.recordTweet(tweetName,time)
# param_2 = obj.getTweetCountsPerFrequency(freq,tweetName,startTime,endTime)