class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        flowers = 0
        # loop through flowerbed using i:
        # if flowerbed[i] == 0:
        #   if i - 1 >= 0: l = i - 1
        #   elif i == 0: l = 0
        #   if i + 1 < len(flowerbed): r = i + 1
        #   elif i == len(flowerbed) - 1: r = i
        #   if flowerbed[l] == 0 and flowerbed[r] == 0: flowerbed[i] = 1, flowers += 1
        # return flowers == n
        for i in range(0, len(flowerbed)):
            if flowerbed[i] == 0:
                if i - 1 >= 0: l = i - 1
                elif i == 0: l = 0
                if i + 1 < len(flowerbed): r = i + 1
                elif i == len(flowerbed) - 1: r = i
                if flowerbed[l] == 0 and flowerbed[r] == 0:
                    flowerbed[i] = 1
                    flowers += 1
        
        return flowers >= n