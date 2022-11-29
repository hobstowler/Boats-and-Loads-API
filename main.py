from flask import Flask, request, jsonify
import boats
import loads
import users

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(boats.bp)
app.register_blueprint(users.bp)
app.register_blueprint(loads.bp)


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!', 404


if __name__ == '__main__':
    app.run()
