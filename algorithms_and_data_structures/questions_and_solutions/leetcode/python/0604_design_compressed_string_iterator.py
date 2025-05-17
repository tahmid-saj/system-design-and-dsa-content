class StringIterator:

    def __init__(self, compressedString: str):
        self.s = compressedString
        self.map = {
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9
            }
        # for i in range(0, len(self.s), 2): 
        #     self.map[self.s[i]] = int(self.s[i + 1])
        if len(self.s) >= 2:
            self.i = 0
            self.it = self.get_repitition()
        else:
            self.i = False
            self.it = False
            self.iEnd = False

    def get_repitition(self):
        i = self.i + 1
        num = ""
        while i < len(self.s):
            if self.s[i] in self.map.keys():
                num += self.s[i]
                i += 1
            else: break

        self.iEnd = i

        return int(num)

    def next(self) -> str:
        hasN = self.hasNext()
        res = self.s[self.i] if hasN == True else " "

        if hasN and self.it == 1: 
            if self.iEnd < len(self.s): 
                self.i = self.iEnd
                self.it = self.get_repitition()
            else:
                self.it = None
                self.i = None
        elif hasN and self.it > 1:
            self.it -= 1
        elif hasN == False: 
            return res

        return res

    def hasNext(self) -> bool:
        if self.it == None or self.i == None or self.iEnd == False: return False
        return True


# Your StringIterator object will be instantiated and called as such:
# obj = StringIterator(compressedString)
# param_1 = obj.next()
# param_2 = obj.hasNext()