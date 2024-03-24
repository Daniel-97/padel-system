class ResponseDTO:
    message: str
    data: any

    def __init__(self, message: str, data: any = None) -> None:
        self.message = message
        self.data = data

        