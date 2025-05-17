class Solution {
    public List<Integer> getRow(int rowIndex) {
        List<Integer> prev = new ArrayList<Integer>(List.of(1, 1));
        List<Integer> curr = new ArrayList<Integer>();

        if (rowIndex == 0) return new ArrayList<Integer>(List.of(1));
        else if (rowIndex == 1) return prev;
        else {
            for (int i = 0; i <= rowIndex; i++) {
                curr = new ArrayList<Integer>();
                for (int j = 0; j <= i; j++) {
                    if (j == 0 || j == i) curr.add(1);
                    else curr.add(prev.get(j - 1) + prev.get(j));
                }
                prev = curr;
            }
        }

        return curr;
    }
}