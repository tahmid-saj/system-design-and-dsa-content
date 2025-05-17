class Solution:
  def convert(self, s: str, numRows: int) -> str:
    # matrix containing zigzag pattern: ["" for _ in range(numRows)]
    # while i < len(s):
    #   row = 0
    #   while row < numRows and i < len(s):
    #     zigzag[row] += s[i], i += 1, row += 1
    #   zigzagRow = (row - 2)
    #   while zigzagRow > 0 and i < len(s):
    #     zigzag[row] += s[i], i += 1, zigzagRow -= 1
    # res = ""
    # for row in range(numRows): res += zigzag[row]
    # return res
    zigzag = ["" for _ in range(numRows)]

    i = 0
    while i < len(s):
      row = 0
      while row < numRows and i < len(s):
        zigzag[row] += s[i]
        i += 1
        row += 1
      
      zigzagRow = row - 2
      while zigzagRow > 0 and i < len(s):
        zigzag[zigzagRow] += s[i]
        i += 1
        zigzagRow -= 1
    
    res = ""
    for row in range(numRows): res += zigzag[row]

    return res