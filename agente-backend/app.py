from flask import Flask, request, jsonify
from  flask_cors import CORS

app= Flask(__name__)
CORS(app)

@app.route('/ping')
def  ping():
    return jsonify({'ping':'pong!'})

@app.route('/load_file', methods=['POST'])
def load_matriz():
    try:
        data = request.get_json()
        file = data.get('file')

        print("file:")
        print(file)

        return jsonify({'message': 'succeful load file'}),200
    
    except Exception as e:
        return jsonify({'error': str(e)}),400
    



if  __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
