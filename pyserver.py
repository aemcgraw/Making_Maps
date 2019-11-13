import traceback

from flask import Flask, render_template, url_for, jsonify

import MapBuilder
#from Making_Maps import MapBuilder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generatemap')
def generate_map():
    result = {}
    result['meta'] = {}
    try:
        image_path = MapBuilder.generate_random_map()
        image_path = url_for("static", filename=image_path)
    except Exception as e:
        result['meta']['status'] = 'fail'
        result['meta']['reason'] = str(e)
        traceback.print_exc()
    else:
        result['meta']['status'] = 'ok'
        result['content'] = image_path
        print(str(result['content']))
    return jsonify(result) 
