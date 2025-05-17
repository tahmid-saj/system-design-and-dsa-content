class NumArray {
private:
    vector<int> numbers;
public:
    NumArray(vector<int>& nums) {
        numbers.push_back(0);
        for (int num : nums) {
            numbers.push_back(numbers.back() + num);
        }
    }
    
    int sumRange(int left, int right) {
        return numbers[right + 1] - numbers[left];
    }
};

/**
 * Your NumArray object will be instantiated and called as such:
 * NumArray* obj = new NumArray(nums);
 * int param_1 = obj->sumRange(left,right);
 */