class CustomError(Exception):
    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 400

    def to_dict(self):
        return_value = dict()
        return_value['error'] = self.message
        return return_value