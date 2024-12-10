class NoRunners(Exception):
    def __init__(self, message="There are no runners in the league!"):
        self.message = message
        super().__init__(self.message)