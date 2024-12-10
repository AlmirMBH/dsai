class NumberRangeError(Exception):
    def __init__(self, message):
        self.message=message
        super().__init__(self.message)

try:
    x = int(input("input number: "))
    if x < 0:
        raise NumberRangeError("x must be positive")
except NumberRangeError as NE:
    print(NE)
except:
    print("Error")