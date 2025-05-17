/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        if (head == nullptr) {
            return head;
        }
        
        for (ListNode* tmpI = head, *tmpJ = head->next; tmpJ != nullptr; tmpJ = tmpJ->next) {
            if (tmpI->val != tmpJ->val) {
                tmpI = tmpI->next;
            }
            else if (tmpI->val == tmpJ->val) {
                tmpI->next = tmpJ->next;
            }
        }
        
        return head;
    }
};