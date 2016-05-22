from flask import render_template
from app import app

@app.route('/')
@app.route('/stats')
def stats():
    return render_template('stats.html')


if __name__ == "__main__":
    app.run(port=port)
