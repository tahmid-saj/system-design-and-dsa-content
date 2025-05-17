class Solution:
    def highFive(self, items: List[List[int]]) -> List[List[int]]:
        grades = defaultdict(list)
        for item in items: grades[item[0]].append(item[1])

        res = []
        for k, v in grades.items():
            top5 = sorted(v)[-5::]
            top5Avg = sum(top5) // 5
            res.append([k, top5Avg])
        res.sort(key=lambda x: x[0])
        return res