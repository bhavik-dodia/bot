from flask import Flask, jsonify, request
from chat import chat

app = Flask(__name__)
@app.route("/bot", methods=["POST"])
def response():
    query = dict(request.form)['query']
    print(query)
    res = chat(query)
    return jsonify({"response" : res})

if __name__=="__main__":
    app.debug = True
    app.run()