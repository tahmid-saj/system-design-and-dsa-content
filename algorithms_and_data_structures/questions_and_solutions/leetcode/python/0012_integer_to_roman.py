class Solution:
  def intToRoman(self, num: int) -> str:
    digits = [
      (1000, "M"),
      (900, "CM"),
      (500, "D"),
      (400, "CD"),
      (100, "C"),
      (90, "XC"),
      (50, "L"),
      (40, "XL"),
      (10, "X"),
      (9, "IX"),
      (5, "V"),
      (4, "IV"),
      (1, "I")
    ]
    res = ""

    # loop through digits using i:
    # if num > digits[i][0]: res += digits[i][1] * (num // digits[i][0]), num -= digits[i][0] * (num // digits[i][0])

    for i in range(len(digits)):
      if num >= digits[i][0]:
        res += digits[i][1] * (num // digits[i][0])
        num -= digits[i][0] * (num // digits[i][0])
      if num == 0: break

    return res     