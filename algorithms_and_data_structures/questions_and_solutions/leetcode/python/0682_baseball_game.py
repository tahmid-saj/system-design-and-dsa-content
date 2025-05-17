class Solution:
    def calPoints(self, operations: List[str]) -> int:
        recordSum, record = 0, []

        for i in range(0, len(operations)):
            if operations[i] == "C": 
                recordSum -= record[-1]
                record.pop()
            elif operations[i] == "D": 
                record.append(record[-1] * 2)
                recordSum += record[-1]
            elif operations[i] == "+": 
                record.append(record[-1] + record[-2])
                recordSum += record[-1]
            else: 
                record.append(int(operations[i]))
                recordSum += record[-1]

        return recordSum