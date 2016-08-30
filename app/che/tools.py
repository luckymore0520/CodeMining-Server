



class SimpleResult:
    result = 1
    message = ""

    def __init__(self, success = 1, message = "success"):
        self.result = success
        self.message = message 

    def json(self):
        return {"result":self.result, "message":self.message}
