import logging
import sys


class HousingException(Exception):

    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail)  

    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys) -> str:
        '''
        error_message:Exception Object
        error_detail:object of sys module
        '''
        _,_,exec_tb=error_detail.exc_info()
        filename=exec_tb.tb_frame.f_code.co_filename
        functionname=exec_tb.tb_frame.f_code.co_name
        try_block_line_number=exec_tb.tb_lineno
        exception_block_line_number=exec_tb.tb_frame.f_lineno
        error_message=f"""Error occured in filename: {filename} 
                          at function name:{functionname}
                          at try block line number:{try_block_line_number}
                          at exception block line number:{exception_block_line_number}
                          and error message:{error_message}"""
        return error_message
    
    def __str__(self)->str:
        return self.error_message
    
    def __repr__(self)->str:
        return HousingException.__name__.str()


