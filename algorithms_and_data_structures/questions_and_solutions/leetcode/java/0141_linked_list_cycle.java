/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        if (head == null || head.next == null) return false;

        ListNode hare = head;
        do {
            if (hare == null) return false;
            head = head.next;
            hare = hare.next;
            if (hare == null) {
                return false;
            } else {
                hare = hare.next;
            }
        } while (head != hare);

        if (hare == null || head == null) return false;

        return true;
    }
}