/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int sizeToErase(int val) {
        int size = 0;
        
        if (val < 0) {
            size++;
            val *= -1;
        }
        
        if (val < 10) {
            size += 1;
        }
        else if (val < 100) {
            size += 2;
        }
        else {
            size += 3;
        }
        
        return size;
    }
    
    void binaryTreePathsHelper(TreeNode* root, string &path, vector<string> &ret) {
        if (root != nullptr) {
            if (root->left == nullptr && root->right == nullptr) {
                path += to_string(root->val);
            }
            else {
                path += to_string(root->val) + "->";
            }
            
            binaryTreePathsHelper(root->left, path, ret);
            if (root->left != nullptr) {
                //path.pop_back();
                //path.erase(path.size() - 1, path.size());
                int sizeErase = sizeToErase(root->left->val);
                
                if (root->left->left == nullptr && root->left->right == nullptr) {
                    
                    path.erase(path.size() - sizeErase, path.size());
                }
                else {
                    path.erase(path.size() - (sizeErase + 2), path.size());
                }
            }
            //path.erase(path.size() - 1, path.size());
            
            binaryTreePathsHelper(root->right, path, ret);
            if (root->right != nullptr) {
                //path.pop_back();
                //path.erase(path.size() - 1, path.size());
                int sizeErase = sizeToErase(root->right->val);
                
                if (root->right->left == nullptr && root->right->right == nullptr) {
                    path.erase(path.size() - sizeErase, path.size());
                }
                else {
                    path.erase(path.size() - (sizeErase + 2), path.size());
                }
            }
            //path.erase(path.size() - 1, path.size());
            
            if (root->left == nullptr && root->right == nullptr) {
                ret.push_back(path);
            }
        }
    }
    
    vector<string> binaryTreePaths(TreeNode* root) {
        vector<string> ret;
        string path = "";
        
        binaryTreePathsHelper(root, path, ret);
        
        return ret;
    }
};