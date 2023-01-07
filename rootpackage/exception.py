import sys,os


class ConcreteException(Exception):
    def __init__(self,error_message:str,error_details:sys):
        self.error_message = self.error_message_detail(error_message, error_details)

    def error_message_detail(self,error:str,error_details:sys):
        _,_,exc_tab = error_details.exc_info()
        file_name = exc_tab.tb_frame.f_code.co_filename
        error_message = f"Error occurred in python script{file_name} in line{exc_tab.tb_lineno} error message {error}"
        return error_message

    def __str__(self):
        return self.error_message