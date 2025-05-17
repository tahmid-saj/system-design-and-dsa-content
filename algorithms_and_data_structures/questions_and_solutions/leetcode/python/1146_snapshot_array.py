class SnapshotArray:

    def __init__(self, length: int):
        self.arr = [[(0, 0)] for _ in range(length)]
        self.snaps = 0

    def set(self, index: int, val: int) -> None:
        self.arr[index].append((self.snaps, val))

    def snap(self) -> int:
        self.snaps += 1
        return self.snaps - 1

    def get(self, index: int, snap_id: int) -> int:
        i = bisect.bisect_right(self.arr[index], (snap_id, 10 ** 9))
        return self.arr[index][i - 1][1]

# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)