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
        parsed_queries = grammar.parser.parse(sql_query)
        results = []
        for query in parsed_queries:
            result = execute_query(query)
            results.append(result)
    except NameError as e:
        results = [{"error": str(e)}]
    except SyntaxError as e:
        results = [{"error": str(e)}]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
