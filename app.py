from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
import numpy as np
import sklearn
import pandas as pd

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def Home():
    return render_template('index.html')



@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def predict():
    
    if request.method == 'POST':
        
        Designation = float(request.form['Designation'])
        
        MentalFatigueScore=float(request.form['Mental Fatigue Score'])
        
        Gender=request.form['Gender']
        if(Gender=='Female'):
                Female=1
                Male=0
        else:
            Female=0
            Male=1
    
        WFHSetupAvailable=request.form['WFH Setup Available']
        if(WFHSetupAvailable=='Yes'):
                Yes=1
                No=0
        else:
            Yes=0
            No=1
        
        date_joining = request.form["Date of Joining"]    
        
        day = int(pd.to_datetime(date_joining, format="%Y-%m-%dT%H:%M").day)
        
        year = int(pd.to_datetime(date_joining, format ="%Y-%m-%dT%H:%M").year)
        
        prediction=model.predict([[Designation,MentalFatigueScore,Female,Male,No,Yes,day,year]])
        
        output=round(prediction[0],2)
        if output>0.4:
            return render_template('index.html',prediction_texts="Attention! You are highly prone of getting a burnout phase, Kindly consult the councillor")
        else:
            return render_template('index.html',prediction_text="You are currently on the safe side with less signs of burnout".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)