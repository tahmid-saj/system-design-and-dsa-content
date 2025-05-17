class Solution:
    def simplifyPath(self, path: str) -> str:
        pathList, stk = path.split("/"), []

        for p in pathList:
            if not p or p == ".": continue
            elif p == "..": 
                if stk: stk.pop()
            else: stk.append(p)
        
        return "/" + "/".join(stk)