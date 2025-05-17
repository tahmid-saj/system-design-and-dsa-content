class Solution {
    public String[] findRelativeRanks(int[] score) {
        // create a hash map of score[i], i
        // sort score
        // traverse through new score using i:
        // score = [3, 4, 8, 9, 10]
        // socreMap [10 : 0, 3 : 1, 8 : 2, 9 : 3, 4 : 4]
        // if (score.length > 3 && i < score.length - 3) res[scoreMap.get(score[i])] = i.toString()
        // else if (i == score.length - 3) res[scoreMap.get(score[i])] = "Bronze Medal"
        // else if (i == score.length - 2) res[scoreMap.get(score[i])] = "Silver Medal" 
        // else if (i == score.length - 1) res[scoreMap.get(score[i])] = "Gold Medal"
        // return res
        Map<Integer, Integer> scoreMap = new HashMap<Integer, Integer>();
        for (int i = 0; i < score.length; i++) scoreMap.put(score[i], i);
        Arrays.sort(score);

        String[] res = new String[score.length];
        for (int i = 0; i < score.length; i++) {
            if (score.length > 3 && i < score.length - 3) res[scoreMap.get(score[i])] = String.valueOf(score.length - i);
            else if (i == score.length - 3) res[scoreMap.get(score[i])] = "Bronze Medal";
            else if (i == score.length - 2) res[scoreMap.get(score[i])] = "Silver Medal";
            else if (i == score.length - 1) res[scoreMap.get(score[i])] = "Gold Medal";
        }
        
        return res;
    }
}