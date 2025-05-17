class Solution:
    def circularArrayLoop(self, arr: List[int]) -> bool:
        for i in range(len(arr)):
            isForward = arr[i] > 0
            slow, fast = i, i

            while True:
                slow = self.nextIndex(arr, isForward, slow)
                fast = self.nextIndex(arr, isForward, fast)
                if fast != -1: fast = self.nextIndex(arr, isForward, fast)
                if slow == -1 or fast == -1: break
                if slow == fast: return True
        
        return False


    def nextIndex(self, arr, isForward, i):
        currDirection = arr[i] > 0

        if isForward != currDirection: return -1

        nextIndex = (i + arr[i]) % len(arr)
        if i == nextIndex: return -1
        return nextIndex