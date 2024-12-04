from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost', dbname='publications', user='postgres', password='manu123')
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query'].lower()  # Convert query to lowercase
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM papers WHERE LOWER(author) LIKE %s OR LOWER(title) LIKE %s', (f'%{query}%', f'%{query}%'))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('results.html', results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
