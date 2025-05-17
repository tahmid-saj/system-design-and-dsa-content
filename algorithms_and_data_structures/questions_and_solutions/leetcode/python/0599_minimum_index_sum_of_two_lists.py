class Solution:
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        l1Map = {}
        for i in range(0, len(list1)): l1Map[list1[i]] = i

        # minDiff, res = 1e8, []
        # loop through list2 using i:
        # if list2[i] in l1Map.keys():
        #   if minDiff = i + l1Map[list2[i]]: res.append(list2[i])
        #   elif minDiff > i + l1Map[list2[i]]: res.clear(), res.append(list2[i])
        # return res

        minDiff, res = 1e8, []
        for i in range(0, len(list2)):
            if list2[i] in l1Map.keys():
                if minDiff == i + l1Map[list2[i]]: 
                    res.append(list2[i])
                elif minDiff > i + l1Map[list2[i]]: 
                    res.clear()
                    res.append(list2[i])
                    minDiff = i + l1Map[list2[i]]
                    
        return res