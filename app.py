import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from imageai.Prediction.Custom import CustomImagePrediction
from tinydb import TinyDB, Query

UPLOAD_FOLDER = r"C:\Users\Kunal Jindal\PycharmProjects\agricure.tech\static\upload"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def agricheck():
    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath(r"C:\Users\Kunal Jindal\PycharmProjects\agricure.tech\Files\model_ex-022_acc-0.966484.h5")
    prediction.setJsonPath(r"C:\Users\Kunal Jindal\PycharmProjects\agricure.tech\Files\model_class.json")
    prediction.loadModel(num_objects=18)
    for a, b, c in os.walk(r"C:\Users\Kunal Jindal\PycharmProjects\agricure.tech\static\upload"):
        imglist = a + r"\\" + c[0]
    predictions, probabilities = prediction.predictImage(imglist, result_count=1)
    os.remove(imglist)
    db = TinyDB(r"C:\Users\Kunal Jindal\PycharmProjects\agricure.tech\Files\db.json")
    User = Query()
    val = (db.search(User.code == predictions[0]))[0]
    outlist = {'code': predictions[0], 'plant': val["plant"], 'treatment': val["treatment"], 'disease': val["disease"]}
    return outlist


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/output', methods=['GET', 'POST'])
def filey():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            outputval = agricheck()
            print(outputval)
            return render_template('output.html',
                                   plant=outputval["plant"],
                                   disease=outputval["disease"],
                                   treatment=outputval["treatment"])
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
