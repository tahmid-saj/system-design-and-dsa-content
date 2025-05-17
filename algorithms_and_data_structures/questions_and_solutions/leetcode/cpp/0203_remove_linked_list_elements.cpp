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
    ListNode* removeElements(ListNode* head, int val) {
        ListNode* prev, *curr;
        
        if (head == nullptr) {
            return nullptr;
        }


        while (head->val == val && head != nullptr) {
            ListNode* tmp = head;
            head = head->next;
            
            if (head == nullptr) {
                return nullptr;
            }
        }

        prev = head;

        for (curr = head->next; curr != nullptr; ) {
            if (curr->val == val) {
                prev->next = curr->next;
                curr = curr->next;
            }
            else if (curr->val != val) {
                prev = prev->next;
                curr = curr->next;
            }
        }

        return head;
    }
};