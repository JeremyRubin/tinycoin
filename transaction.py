
from base import *
class TX(object):
    def __init__(self, parent_tx, _from, to_amounts, sig=""):
        self.parent_tx = parent_tx
        self._from = _from
        self.to_amounts = to_amounts
        self.sig = sig
        self.tx = (self.parent_tx, self._from, self.to_amounts)
    def amount_spent(self):
        return sum(a for (_, a) in self.to_amounts)
    def sign(self, sk):
        return TX(self.parent_tx, self._from, self.to_amounts, sk.sign_deterministic(str(self.tx)))
    def verifySig(self):
        vk = VerifyingKey.from_string(self._from)
        try:
            return vk.verify(self.sig, str(self.tx))
        except:
            raise ValueError("Sig Bad")
    def hash(self):
        sha(self.serialize())
    def serialize(self):
        return str( (self.sig, self.tx))
    @staticmethod
    def deserialize(s):
        v = ast.literal_eval(s)
        if isinstance(v, tuple) and isinstance(v[1], tuple) and len(v) == 2 and len(v[1]) == 3:
            t = TX(v[1][0], v[1][1], v[1][2],  v[0])
            t.verifySig()
            if any(amount < 0 for (to, amount) in t.to_amounts):
                raise ValueError("No Negative Values legal")
            return t
        else:
            raise ValueError("Malformed tx")

