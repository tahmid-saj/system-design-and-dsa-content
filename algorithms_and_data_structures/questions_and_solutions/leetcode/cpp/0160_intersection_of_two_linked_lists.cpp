/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
            set<ListNode*> setA, setB;

        for (auto tmpA = headA, tmpB = headB; tmpA != NULL || tmpB != NULL;) {
            if (setA.find(tmpB) == setA.end()) {
                setA.insert(tmpA);
            }
            else if (setA.find(tmpB) != setA.end()) {
                return tmpB;
            }

            if (setB.find(tmpA) == setB.end()) {
                setB.insert(tmpB);
            }
            else if (setB.find(tmpA) != setB.end()) {
                return tmpA;
            }
            
            if (tmpA == tmpB) {
                return tmpA;
            }

            if (tmpA != NULL) {
                tmpA = tmpA->next;
            }

            if (tmpB != NULL) {
                tmpB = tmpB->next;
            }
        }

        return NULL;
    }
};