class MyStack {
    Queue<Integer> q = new LinkedList<>();

    public MyStack() {
    
    }
    
    public void push(int x) {
        if (q.size() == 0) {
            q.add(x);
            return;
        }
        q.add(x);
        for (int i = 0; i < q.size() - 1; i++) {
            int tmp = q.remove();
            q.add(tmp);
        }
    }
    
    public int pop() {
        return q.remove();
    }
    
    public int top() {
        return q.peek();
    }
    
    public boolean empty() {
        return q.isEmpty();
    }
}

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack obj = new MyStack();
 * obj.push(x);
 * int param_2 = obj.pop();
 * int param_3 = obj.top();
 * boolean param_4 = obj.empty();
 */