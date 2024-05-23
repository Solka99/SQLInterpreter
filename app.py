from flask import Flask, request, render_template, jsonify
from functions import execute_query
import grammar  # Import parsera SQL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/execute-query', methods=['POST'])
def execute_query_route():
    data = request.get_json()
    sql_query = data.get('query', '')
    try:
        parsed_query = grammar.parser.parse(sql_query)
        result = execute_query(parsed_query)
    except SyntaxError as e:
        result = {"error": str(e)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
