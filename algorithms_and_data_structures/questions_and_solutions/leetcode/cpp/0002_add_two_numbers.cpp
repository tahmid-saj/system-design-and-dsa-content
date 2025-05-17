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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        int size1 = 0, size2 = 0;

        ListNode* tmp1Last, * tmp2Last;

        for (tmp1Last = l1; ; tmp1Last = tmp1Last->next) {
            size1++;
            
            if (tmp1Last->next == nullptr) {
                break;
            }
        }

        for (tmp2Last = l2; ; tmp2Last = tmp2Last->next) {
            size2++;
            
            if (tmp2Last->next == nullptr) {
                break;
            }
        }

        if (size1 > size2) {
            for (int i = 0; i < size1 - size2; i++) {
                tmp2Last->next = new ListNode(0, nullptr);
                tmp2Last = tmp2Last->next;
            }
        }
        else if (size2 > size1) {
            for (int i = 0; i < size2 - size1; i++) {
                tmp1Last->next = new ListNode(0, nullptr);
                tmp1Last = tmp1Last->next;
            }
        }

        ListNode* ret = new ListNode(0);

        ListNode& head = *ret;

        for (ListNode* tmp1 = l1, *tmp2 = l2; tmp1 != nullptr && tmp2 != nullptr; tmp1 = tmp1->next, tmp2 = tmp2->next) {
            if (tmp1->val + tmp2->val + ret->val <= 9) {
                ret->val += tmp1->val + tmp2->val;

                if (tmp1->next == nullptr || tmp2->next == nullptr) {
                    break;
                }

                ret->next = new ListNode(0, nullptr);
                ret = ret->next;
            }
            else if (tmp1->val + tmp2->val + ret->val > 9) {
                ret->val = (tmp1->val + tmp2->val + ret->val) % 10;
                ret->next = new ListNode(1, nullptr);
                ret = ret->next;
            }
        }

        return &head;
    }
};