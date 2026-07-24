from flask import Flask,request
app = Flask(__name__)
@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return f"Hello, {data['name']}"

if __name__=="__main__":
    app.run(debug=True)
