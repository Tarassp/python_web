class UnknownAssistentCommand(Exception):
    def __init__(self, message = "You entered the wrong command."):
        self.message = message
        super().__init__(self.message)
        
class UnknownAssistentValue(Exception):
    def __init__(self, message = "You entered the wrong value."):
        self.message = message
        super().__init__(self.message)
        
class IncorrectDataFormat(Exception):
    def __init__(self, message = "Incorrect data format."):
        self.message = message
        super().__init__(self.message)
        
class IncorrectDateFormat(Exception):
    def __init__(self, message = "Incorrect date format, should be 'dd/mm/yyyy'"):
        self.message = message
        super().__init__(self.message)
        
class IncorrectEmailFormat(Exception):
    def __init__(self, message = "Incorrect email format, should be"):
        self.message = message
        super().__init__(self.message)
        
class IncorrectPhoneFormat(Exception):
    def __init__(self, message = "Incorrect phone number format, should be '(+)(38)0xxxxxxxxx'"):
        self.message = message
        super().__init__(self.message)

class IncorrectFileName(Exception):
    def __init__(self, message = "Incorrect file name, should be <filename> + extension"):
        self.message = message
        super().__init__(self.message)