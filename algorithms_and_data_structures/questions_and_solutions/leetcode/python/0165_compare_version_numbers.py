class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        # return self.splitting(version1, version2)
        return self.withoutSplitting(version1, version2)

    def splitting(self, version1, version2):
        version1Split = version1.split(".")
        version2Split = version2.split(".")
        i, j = 0, 0
        while i < len(version1Split) or j < len(version2Split):
            ver1 = int(version1Split[i]) if i < len(version1Split) else 0
            ver2 = int(version2Split[j]) if j < len(version2Split) else 0
            if ver1 < ver2: return -1
            elif ver1 > ver2: return 1
            i += 1
            j += 1
        return 0

    def withoutSplitting(self, version1, version2):
        i, j = 0, 0
        while i < len(version1) or j < len(version2):
            num1, num2 = 0, 0
            if i < len(version1): i, num1 = self.revision(version1, i)
            if j < len(version2): j, num2 = self.revision(version2, j)

            if num1 < num2: return -1
            if num1 > num2: return 1
        
        return 0
    
    def revision(self, version, i):
        start = i
        while i < len(version) and version[i] != ".": i += 1
        return i + 1, int(version[start:i])