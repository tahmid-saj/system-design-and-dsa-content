class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> res = new ArrayList<List<Integer>>(List.of(List.of(1), List.of(1, 1)));

        if (numRows == 1) return new ArrayList<List<Integer>>(List.of(List.of(1)));
        else if (numRows == 2) return res;
        else {
            for (int i = 2; i < numRows; i++) {
                List<Integer> subRes = new ArrayList<Integer>();
                for (int j = 0; j <= i; j++) {
                    if (j == 0 || j == i) subRes.add(1);
                    else subRes.add(res.get(i - 1).get(j - 1) + res.get(i - 1).get(j));
                }
                res.add(subRes);
            }
        }

        return res;
    }
}