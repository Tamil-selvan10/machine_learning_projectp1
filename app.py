from flask import Flask
from housing.logger import logging
from housing.exception import HousingException
import sys


app=Flask(__name__) # Name of module
                    # By default, main

@app.route('/',methods=['GET','POST'])
def index():
    try:
        result=10/0
    except Exception as e:
        Houexec=HousingException(error_message=e,error_detail=sys)
        logging.info(Houexec.error_message)
    return 'Starting Machine Learning Project'

if __name__=='__main__':
    app.run(debug=True)

    #debug =False
    #1.Changes --> saved
    #2.Already running --> stop
    #3.Start

    #debug=True
    #1.Changes --> saved
    #2.Automatica changes detect ---> restart