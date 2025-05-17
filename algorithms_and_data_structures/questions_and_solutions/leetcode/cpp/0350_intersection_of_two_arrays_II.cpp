class Solution {
public:
    vector<int> intersect(vector<int>& nums1, vector<int>& nums2) {
        if(nums1.size() > nums2.size()){
            swap(nums1, nums2);
        }
        
        unordered_map<int, int> m;
        for(auto val : nums1){
            m[val]++;
        }
        
        int k = 0;
        
        for(auto val : nums2){
            if(m[val] > 0){
                nums1[k++] = val;
                --m[val];
            }
        }
        
        return vector<int>(nums1.begin(), nums1.begin() + k);
    }
};