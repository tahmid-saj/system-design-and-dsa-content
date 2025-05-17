class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> ivec;

        for (int i = 0; i < numRows; i++) {
            ivec.push_back(vector<int>());

            for (int j = 0; j < i + 1; j++) {
                if (j == 0 || j == i) {
                    ivec[i].push_back(1);
                }
                else if (j != 0 && j != i) {
                    int num = ivec[i - 1][j - 1] + ivec[i - 1][j];

                    ivec[i].push_back(num);
                }
            }
        }

        return ivec;
    }
};