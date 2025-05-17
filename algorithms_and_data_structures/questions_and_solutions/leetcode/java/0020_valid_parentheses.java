class Solution {
    public boolean isValid(String s) {
        Stack<Character> stk = new Stack<Character>();

        if (s.length() == 1) return false;

        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stk.push(c);
                continue;
            }
            if ((c == ')' || c == '}' || c == ']') && stk.isEmpty()) {
                return false;
            } else if ((c == ')' && stk.peek() != '(') || (c == '}' && stk.peek() != '{') || (c == ']' && stk.peek() != '[')) {
                return false;
            } else {
                stk.pop();
            }
        }

        return stk.isEmpty();
    }
}