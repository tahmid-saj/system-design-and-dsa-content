class Solution:
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        import datetime
        x = datetime.datetime(year, month, day)
        return x.strftime("%A")