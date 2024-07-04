from src import config, app
from flask import json

if __name__ == "__main__":
    # create a ping route
    @app.route('/',methods=['GET'])
    def pingServer():
        return json.jsonify({"msg":"we are logically blessed"})
    app.run(host= config.HOST,
            port= config.PORT,
            debug= config.DEBUG)