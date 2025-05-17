# from segment_tree import SegmentTree

class OrderedSet:
    def __init__(self):
        self.set = []
    
    def add(self, val):
        self.set.append(val)
        self.set.sort(reversed=False)
    
    def findByOrder(self, k):
        if k < 0 or k >= len(self.set): return None
        return self.set[k]
    
    def orderOfKey(self, val):
        return sum(1 for x in self.set if x < val)

class SegmentTree:
    def __init__(self, nums):
        self.st = [0 for _ in range(4 * len(nums))]
        self.list = nums

    def build(self, node, l, r):
        if l == r: self.st[node] = self.list[l]
        else:
            middle = (l + r) // 2
            self.build(2 * node, l, middle)
            self.build(2 * node + 1, middle + 1, r)
            self.st[node] = self.st[2 * node] + self.st[2 * node + 1]
    
    def update(self, node, l, r, i, val):
        if l == r:
            self.list[i] += val
            self.st[node] += val
        else:
            middle = (l + r) // 2
            if (l <= i and i <= middle): self.update(2 * node, l, middle, i, val)
            else: self.update(2 * node + 1, middle + 1, r, i, val)
        
            self.st[node] = self.st[2 * node] + self.st[2 * node + 1]
    
    def query(self, node, start, end, l, r):
        if r < start or end < l: return 0
        if l <= start and end <= r: return self.st[node]
        middle = (start + end) // 2
        return self.query(2 * node, start, middle, l, r) + self.query(2 * node + 1, middle + 1, end, l, r)

# https://leetcode.com/discuss/interview-question/787180/segment-tree-implementation-python-range-query-min-max-sum-and-update-segment-tree
class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.min = float("inf")
        self.max = float("-inf")
        self.sum = float("inf")
        self.leftEdge = None
        self.rightEdge = None


class SegmentTree:
    def __init__(self):
        """
        Initializer method to initialize the class level objects
        :rtype: object
        """
        self.partial_overlap = "Partial overlap"
        self.no_overlap = "No overlap"
        self.complete_overlap = "Complete overlap"

    def get_overlap(self, x1, y1, x2, y2):
        """
        Method to get the overlapping type for a given ranges
        X1, Y1 -> Given node's range
        X2, Y2 -> Query range
        :return: type of overlap
        """
        if (x1 == x2 and y1 == y2) or (x1 >= x2 and y1 <= y2):
            overlap = self.complete_overlap
        elif (y1 < x2) or (x1 > y2):
            overlap = self.no_overlap
        else:
            overlap = self.partial_overlap
        return overlap

    def construct_segment_tree(self, array, start, end):
        """
        Method to construct a Segment tree using a given array elements
        :param end:
        :param start:
        :param array: Array elements
        :return: Root node of a segment tree
        """
        if end - start <= 0 or len(array) == 0:
            return None
        if end - start == 1:
            node = Node()
            node.min = array[start]
            node.max = array[start]
            node.sum = array[start]
            node.leftEdge = start
            node.rightEdge = end - 1
            return node
        else:
            node = Node()
            mid = start + (end - start) // 2
            node.left = self.construct_segment_tree(array, start=start, end=mid)
            node.right = self.construct_segment_tree(array, start=mid, end=end)
            if node.left is None and node.right is None:
                node.sum = 0
                node.leftEdge = start
                node.rightEdge = start
                node.min = float("inf")
                node.max = float("-inf")
            elif node.left is None:
                node.sum = node.right.sum
                node.leftEdge = node.right.leftEdge
                node.rightEdge = node.right.rightEdge
                node.min = node.right.min
                node.max = node.right.max
            elif node.right is None:
                node.sum = node.left.sum
                node.leftEdge = node.left.leftEdge
                node.rightEdge = node.left.rightEdge
                node.min = node.left.min
                node.max = node.left.max
            else:
                node.min = min(node.left.min, node.right.min)
                node.max = max(node.left.max, node.right.max)
                node.sum = node.left.sum + node.right.sum
                node.leftEdge = node.left.leftEdge
                node.rightEdge = node.right.rightEdge
            return node

    def update_segment_tree(self, head, index, new_value, array):
        """
        Method to update the segment tree node value
        :return: Head node of a segment tree
        :rtype: object
        """
        if index == head.leftEdge == head.rightEdge:
            head.max = new_value
            head.min = new_value
            head.sum = new_value
            array[index] = new_value
            return head
        elif (head.leftEdge <= index <= head.rightEdge) and (head.rightEdge > head.leftEdge):
            left_node = self.update_segment_tree(head=head.left, index=index, new_value=new_value, array=array)
            right_node = self.update_segment_tree(head=head.right, index=index, new_value=new_value, array=array)
            head.sum = right_node.sum + left_node.sum
            head.min = min(left_node.min, right_node.min)
            head.max = max(left_node.max, right_node.max)
            return head
        else:
            return head

    def get_minimum(self, head, left, right):
        """
        Method to get the minimum in a given range query
        :return: Minimum value for a given range query
        """
        overlap = self.get_overlap(head.leftEdge, head.rightEdge, left, right)
        if overlap == self.complete_overlap:
            return head.min
        elif overlap == self.no_overlap:
            return float("inf")
        elif overlap == self.partial_overlap:
            left_min = self.get_minimum(head=head.left, left=left, right=right)
            right_min = self.get_minimum(head=head.right, left=left, right=right)
            return min(left_min, right_min)

    def get_maximum(self, head, left, right):
        """
        Method to get the maximum value for a given range query
        :return Maximum value for a given range query
        """
        overlap = self.get_overlap(head.leftEdge, head.rightEdge, left, right)
        if overlap == self.complete_overlap:
            return head.max
        elif overlap == self.no_overlap:
            return float("-inf")
        elif overlap == self.partial_overlap:
            left_max = self.get_maximum(head=head.left, left=left, right=right)
            right_max = self.get_maximum(head=head.right, left=left, right=right)
            return max(left_max, right_max)

    def get_sum(self, head, left, right):
        """
        Method to return the sum of an array elements for a given range query
        :return: Returns the sum of an array elements for a given range query
        """
        overlap = self.get_overlap(head.leftEdge, head.rightEdge, left, right)
        if overlap == self.complete_overlap:
            return head.sum
        elif overlap == self.no_overlap:
            return 0
        elif overlap == self.partial_overlap:
            left_sum = self.get_sum(head=head.left, left=left, right=right)
            right_sum = self.get_sum(head=head.right, left=left, right=right)
            return left_sum + right_sum

    def preorder_traversal(self, head, array):
        if head is None:
            return
        print("Array = {} Min = {}, Max = {}, Sum = {}".format(array[head.leftEdge:head.rightEdge + 1], head.min,
                                                               head.max, head.sum))
        self.preorder_traversal(head=head.left, array=array)
        self.preorder_traversal(head=head.right, array=array)

class NumArray:
    def __init__(self, nums: List[int]):
        # self.prefix = []
        # for num in nums: self.prefix.append((self.prefix[-1] if self.prefix else 0) + num)

        self.st = SegmentTree()
        self.root = self.st.construct_segment_tree(array=nums, start=0, end=len(nums))
        self.nums = nums

        # self.st = SegmentTree(nums)

    def update(self, index: int, val: int) -> None:
        # num = self.prefix[index] - (self.prefix[index - 1] if index > 0 else 0)
        # val = val - num
        # for i in range(index, len(self.prefix)): self.prefix[i] += val

        self.st.update_segment_tree(head=self.root, index=index, new_value=val, array=self.nums)

        # self.st.update(index, val)

    def sumRange(self, left: int, right: int) -> int:
        # l = self.prefix[left - 1] if left > 0 else 0
        # r = self.prefix[right]
        # return r - l

        return self.st.get_sum(head=self.root, left=left, right=right)

        # return self.st.query(left, right, "sum")

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)