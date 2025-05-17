from heapq import *

class Solution:
  def leastInterval(self, tasks: List[str], n: int) -> int:
    intervalCount = 0
    maxHeap = []
    frequency = {}
    for i in range(0, len(tasks)): frequency[tasks[i]] = frequency.get(tasks[i], 0) + 1
    for k, v in frequency.items(): heappush(maxHeap, (-v, k))

    while len(maxHeap) > 0:
      queue = []
      i = n + 1
      while i > 0 and maxHeap:
        intervalCount += 1
        i -= 1
        freq, c = heappop(maxHeap)
        freq = -freq
        freq -= 1
        if freq > 0: queue.append((freq, c))
      
      while len(queue) > 0:
        freq, c = queue.pop(0)
        heappush(maxHeap, (-freq, c))
      
      if maxHeap: intervalCount += i
  
    return intervalCount