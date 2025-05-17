class Solution {
    public String[] findWords(String[] words) {
        Map<Character, Integer> rows = new HashMap<Character, Integer>();
        rows.put('q', 1);
        rows.put('w', 1);
        rows.put('e', 1);
        rows.put('r', 1);
        rows.put('t', 1);
        rows.put('y', 1);
        rows.put('u', 1);
        rows.put('i', 1);
        rows.put('o', 1);
        rows.put('p', 1);
        rows.put('a', 2);
        rows.put('s', 2);
        rows.put('d', 2);
        rows.put('f', 2);
        rows.put('g', 2);
        rows.put('h', 2);
        rows.put('j', 2);
        rows.put('k', 2);
        rows.put('l', 2);
        rows.put('z', 3);
        rows.put('x', 3);
        rows.put('c', 3);
        rows.put('v', 3);
        rows.put('b', 3);
        rows.put('n', 3);
        rows.put('m', 3);

        String[] res = new String[words.length];
        int resI = 0;
        for (int i = 0; i < words.length; i++) {
            int row = rows.get(words[i].toLowerCase().charAt(0));
            for (int j = 0; j < words[i].length(); j++) {
                if (row != rows.get(words[i].toLowerCase().charAt(j))) break;
                else if (j + 1 == words[i].length()) {
                    res[resI] = words[i];
                    resI++;
                }
            }
        }

        return Arrays.copyOfRange(res, 0, resI);
    }
}