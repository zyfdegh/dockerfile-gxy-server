class Transaction:
    def __init__(self, transactionID=None, orderID=None):
        self._transactionID = transactionID
        self._orderID = orderID

    def getTransactionID(self):
        return self._transactionID

    def setTransactionID(self, transactionID):
        self._transactionID = transactionID

    def getOrderID(self):
        return self._orderID

    def setOrderID(self, orderID):
        self._orderID = orderID
