from flask import Flask, render_template, request
from engine import perform_duckduckgo_search, perform_github_search

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    results = []

    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            results += perform_duckduckgo_search(query)
            results += perform_github_search(query)

    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
