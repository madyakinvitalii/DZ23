import os
from flask import Flask, request, jsonify
from constants import DATA_DIR
from marshmallow import ValidationError
from schema import RequestJsonSchema
from functions import get_query

app = Flask(__name__)


@app.route("/perform_query/", methods=["POST"])
def perform_query():
    try:
        data = RequestJsonSchema().load(request.json)
    except ValidationError as e:
        return jsonify(error=str(e)), 400

    valid_commands = {'sort', 'filter', 'limit', 'map', 'unique'}
    if not (data['cmd1'] in valid_commands and data['cmd2'] in valid_commands):
        return jsonify(error='Invalid command'), 400

    file_path = os.path.abspath(os.path.join(DATA_DIR, data['file_name']))
    if not os.path.exists(file_path):
        return jsonify(error='File does not exist'), 400

    with open(file_path) as f:
        try:
            result = get_query(data['cmd1'], data['value1'], f)
            result = get_query(data['cmd2'], data['value2'], result)
        except ValueError as e:
            return jsonify(error=str(e)), 400

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)

