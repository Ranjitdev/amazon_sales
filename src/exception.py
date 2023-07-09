import sys
from src.logger import logging

def error_message_details(error, error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "error occured script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        print(self.error_message)
        logging.error(self.error_message)
        return self.error_message


if __name__=='__main__':
    try:
        print(1/0)
    except Exception as e:
        raise CustomException(e, sys)