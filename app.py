from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'Lois',
    'password': 'loisgantenzzz',
    'host': 'localhost',
    'database': 'currency_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM currency')
    currencies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', currencies=currencies)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        symbol = request.form['symbol']
        rate = request.form['rate']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO currency (name, symbol, rate) VALUES (%s, %s, %s)', (name, symbol, rate))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        symbol = request.form['symbol']
        rate = request.form['rate']
        
        cursor.execute('UPDATE currency SET name=%s, symbol=%s, rate=%s WHERE id=%s', (name, symbol, rate, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM currency WHERE id = %s', (id,))
    currency = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update.html', currency=currency)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM currency WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)