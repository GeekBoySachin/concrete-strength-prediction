from flask import Flask,request,send_file,render_template
from flask_cors import CORS,cross_origin
from concrete.pipeline.batch_prediction import BatchPrediction
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template("prediction_home.html")

@app.route('/uploadfile',methods=['POST'])
@cross_origin()
def uploadfile():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        if fname[-3:].lower() == "csv":
            input_file_path = os.path.join(os.getcwd(),"prediction",fname)
            f.save(input_file_path)
            batch_prediction = BatchPrediction(input_file_path)
            try:
                output_file_path = batch_prediction.start_batch_prediction() 
                return send_file(output_file_path)
            except:
                return "Some error occured please check the file"
        else:
            return "Please upload file in csv format."


if __name__ == "__main__":
	app.run(debug=True)