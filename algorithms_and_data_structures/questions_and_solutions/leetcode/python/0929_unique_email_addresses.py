class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        res = set()

        for email in emails:
            names = email.split("@")
            localName = ""
            for c in names[0]:
                if c == ".": continue
                elif c == "+": break
                localName += c
            res.add(localName + "@" + names[1])
        
        return len(res)