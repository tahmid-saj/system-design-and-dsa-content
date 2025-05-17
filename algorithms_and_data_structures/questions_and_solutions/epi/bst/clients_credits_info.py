import bintrees
class ClientsCreditsInfo:
    def __init__(self):
        self.offset = 0
        self.clientToCredit = {}
        self.creditToClient = bintrees.RBTree()
    
    def insert(self, client_id, credit):
        self.remove(client_id)
        self.clientToCredit[client_id] = credit - self.offset
        self.creditToClient.setDefault(credit - self.offset, set()).add(client_id)
    
    def remove(self, client_id):
        if client_id in self.clientToCredit:
            credit = self.clientToCredit[client_id]
            del self.clientToCredit[client_id]
            self.creditToClient[credit].remove(client_id)
            if not self.creditToClient[credit]: del self.creditToClient[credit]
            return True
        return False
    
    def lookup(self, client_id):
        if client_id in self.clientToCredit: return self.clientToCredit[client_id]
        return False
    
    def add_all(self, credit):
        self.offset += credit
    
    def max(self):
        res = self.creditToClient.max_item()[1]
        if res: return next(iter(res))
        return False