class Solution:
  def reverse(self, x: int) -> int:
    negative = x < 0
    res = 0
    x = abs(x)

    while x > 0:
      res *= 10
      res += x % 10
      x //= 10
    
    if res < -1 * pow(2, 31) or res > pow(2, 31) - 1: return 0
    if negative: res *= -1
    return res