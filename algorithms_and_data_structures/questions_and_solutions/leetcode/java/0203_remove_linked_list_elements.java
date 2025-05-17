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
    public ListNode removeElements(ListNode head, int val) {
        ListNode prev = null, curr = head, res = null;

        while (curr != null) {
            if (curr.val == val && res == null) {
                curr = curr.next;
            } else if (curr.val != val && res == null) {
                res = curr;
                prev = curr;
                curr = curr.next;
            } else if (curr.val == val && res != null) {
                prev.next = curr.next;
                curr = curr.next;
            } else if (curr.val != val && res != null) {
                prev = prev.next;
                curr = curr.next;
            }
        }

        return res;
    }
}