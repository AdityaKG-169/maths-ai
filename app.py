from flask import Flask, redirect, render_template, request, jsonify
import os
import gensim


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


app = Flask(__name__)
saved_model_path = 'savedmodel/maths-ai-model'
model = gensim.models.Word2Vec.load(saved_model_path)

def predict(a, b, c):
    try:
        return '', model.wv.most_similar_cosmul(positive=[a, c], negative=[b])[0][0]
    except:
        return 'Word not in my dictionary, sorry.', ''



@app.route('/', methods=['GET'])
def home():
    return render_template('sample.html', error=None, pred=None, last_updated=dir_last_updated('./static'))

@app.route('/infer/', methods=['POST'])
def pred():
    error = ''
    try:
        a = lower(request.form['a'])
        b = lower(request.form['b'])
        c = lower(request.form['c'])
    except:
        error = 'Invalid action!'
    
    if a == '' or b == '' or c == '':
        error = 'Fill out all the fields!'
    
    error, inference = predict(a, b, c)

    if error == '':
        return jsonify({'error': '', 'pred': inference})
    else:
        return jsonify({'error': error, 'pred': ''})



if __name__ == '__main__':
    app.run(debug=True)

