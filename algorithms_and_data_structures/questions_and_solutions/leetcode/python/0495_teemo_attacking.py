class Solution:
    def findPoisonedDuration(self, timeSeries: List[int], duration: int) -> int:
        # res, endTime = -1
        # loop through timeSeries using i:
        # if timeSeries[i] <= endTime: res -= (endTime - timeSeries[i]) + 1, res += duration, endTime = timeSeries[i] + duration - 1
        # elif timeSeries[i] > endTime: res += duration, endTime = timeSeries[i] + duration - 1 
        res, endTime = 0, -1
        for i in range(0, len(timeSeries)):
            if timeSeries[i] <= endTime:
                res -= (endTime - timeSeries[i]) + 1
                res += duration
            elif timeSeries[i] > endTime:
                res += duration

            endTime = timeSeries[i] + duration - 1

        return res