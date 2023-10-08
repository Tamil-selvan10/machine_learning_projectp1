from flask import Flask


app=Flask(__name__) # Name of module
                    # By default, main

@app.route('/',methods=['GET','POST'])
def index():
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