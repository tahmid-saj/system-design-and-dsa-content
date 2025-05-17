/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        if (head == null) return null;
        if (head.next == null) return head;

        ListNode res = head, prev = head, curr = head.next;

        while (curr != null) {
            if (prev.val != curr.val) {
                prev.next = curr;
                prev = prev.next;
            }
            curr = curr.next;

            if (curr == null) prev.next = null;
        }

        return res;
    }
}