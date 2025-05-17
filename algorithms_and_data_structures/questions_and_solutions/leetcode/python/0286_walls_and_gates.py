class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        queue = deque()
        emptyRooms = set()
        empty, wall, gate = 2147483647, -1, 0
        for i in range(len(rooms)):
            for j in range(len(rooms[0])):
                if rooms[i][j] == gate: 
                    queue.append((i, j, 0))
                    emptyRooms.add((i, j))
                if rooms[i][j] == empty: emptyRooms.add((i, j))

        self.bfs(rooms, queue, emptyRooms, empty, wall, gate)

    def bfs(self, rooms, queue, emptyRooms, empty, wall, gate):
        while queue:
            i, j, dist = queue.popleft()
            if (i, j) in emptyRooms:
                rooms[i][j] = dist
                emptyRooms.remove((i, j))
                queue.append((i - 1, j, dist + 1))
                queue.append((i + 1, j, dist + 1))
                queue.append((i, j - 1, dist + 1))
                queue.append((i, j + 1, dist + 1))