# from client_test_api.config.ws import EXCHANGE
from config.ws import EXCHANGE


class Check:

    def __init__(self, ex_name):
        if ex_name not in EXCHANGE:
            raise Exception(f"{ex_name} is not supported")
        else:
            self.ex_name = ex_name
        self.ltp = None
        self.exchange = None

    def _parse_data(self):
        self.ltp_asks = self.ltp["asks"]
        self.ltp_bids = self.ltp["bids"]

        if self.ex_name == "OKX":
            self.ex_asks = self.exchange[0]["asks"]
            self.ex_bids = self.exchange[0]["bids"]
        elif self.ex_name == "BN":
            self.ex_asks = self.exchange["a"]
            self.ex_bids = self.exchange["b"]

    def _diff(self, n1, n2):
        size1, size2 = len(n1), len(n2)
        p1, p2 = 0, 0
        if size1 != size2:
            return False
        else:
            while p1 < size1:
                if not self._check_detail(n1[p1], n2[p2]):
                    return False
                p1 += 1
                p2 += 1
            return True

    def _check_detail(self, n1, n2):
        if self.ex_name == "OKX":
            n2 = n2[:2]

            for i in range(2):
                if n1[i] != n2[i]:
                    return False
        return True


    def is_equals(self, ltp, exchange):
        self.ltp = ltp.get("data")
        if self.ex_name == "BN":
            self.exchange = exchange
        else:
            self.exchange = exchange.get("data")
        self._parse_data()

        res1 = self._diff(self.ltp_asks, self.ex_asks)
        res2 = self._diff(self.ltp_bids, self.ex_bids)
        return res1 and res2
