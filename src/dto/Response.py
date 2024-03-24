class ResponseDTO:
    message: str
    data: any

    def __init__(self, message: str = None, data: any = None) -> None:
        self.message = message
        self.data = data

        