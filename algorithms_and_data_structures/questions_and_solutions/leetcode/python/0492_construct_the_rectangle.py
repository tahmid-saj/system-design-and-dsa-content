class Solution:
    def constructRectangle(self, area: int) -> List[int]:
        # initialize width and length with square root of target area rounded down and up, respectively
        width = int(math.sqrt(area))
        length = int(math.ceil(area / width))
        
        # loop until width and length multiplied is equal to target area
        while width * length != area:
            # if width * length is less than target area, increment length
            if width * length < area:
                length += 1
            # if width * length is greater than target area, decrement width
            else:
                width -= 1
        
        # return [length, width]
        return [length, width]