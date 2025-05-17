class Solution:
    def defangIPaddr(self, address: str) -> str:
        address = address.split(".")
        return "[.]".join(address)