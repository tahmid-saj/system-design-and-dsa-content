class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # return self.mostIntervalIntersections(intervals)
        return self.heap(intervals)

    def mostIntervalIntersections(self, intervals):
        if len(intervals) <= 1: return 1
        
        minRooms, endPtr = 0, 0

        startTimes = [intervals[i][0] for i in range(len(intervals))]
        endTimes = [intervals[i][1] for i in range(len(intervals))]
        startTimes.sort()
        endTimes.sort()

        for i in range(0, len(startTimes)):
            if startTimes[i] >= endTimes[endPtr]: endPtr += 1
            else: minRooms += 1

        return minRooms
    
    def heap(self, meetings):
        if len(meetings) <= 1: return 1
        meetings.sort(key=lambda x: x[0])

        minRooms = 0
        minHeap = []
        for meeting in meetings:
            # remove all meetings that have ended
            while minHeap and meeting[0] >= minHeap[0][1]:
                heapq.heappop(minHeap)
            # add the current meeting into the minHeap
            heapq.heappush(minHeap, meeting)
            # all active meetings are in the minHeap, so we need rooms for all of them.
            minRooms = max(minRooms, len(minHeap))
        return minRooms