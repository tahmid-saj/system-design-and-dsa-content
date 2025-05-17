class Solution:
    def dayOfYear(self, date: str) -> int:
        year, months, lastDays, res = int(date[:4]), int(date[5:7]) - 1, int(date[8:]), 0
        if months == 0: return lastDays
        for month in range(1, months + 1):
            res += self.days(year, month)
        return res + lastDays
        
    def days(self, year, month):
        days = {
            1: 31,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }
        if month == 2:
            if (year % 100 != 0 and year % 4 == 0) or (year % 400 == 0): return 29
            else: return 28
        return days[month]