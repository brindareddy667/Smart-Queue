from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='.')
DB_FILE = 'queue.db'
AVERAGE_WAIT_TIME = 10  # minutes

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_color_by_index(index, total):
    # Define a gradient of 10 colors (green → yellow → orange → red)
    gradient = [
        '#d4edda', '#e2efd6', '#f1f1d1', '#fff3cd',
        '#ffedc4', '#ffe6bb', '#ffe0b2', '#fdddbf',
        '#fadacd', '#f8d7da'
    ]
    if total <= 1:
        return gradient[0]
    step = len(gradient) / max(1, total - 1)
    idx = int(index * step)
    return gradient[min(idx, len(gradient)-1)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT INTO queue_entries (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('status', username=name, joined='true'))
    else:
        # When accessed via QR scan (GET request), just show the join form
        return render_template('index.html')

@app.route('/status/<username>')
def status(username):
    joined = request.args.get('joined')
    conn = get_db_connection()
    queue = conn.execute('SELECT * FROM queue_entries ORDER BY joined_time').fetchall()
    conn.close()

    queue_display = []
    total_time = 0
    position = None
    estimated_time = None
    current_time = datetime.now()

    for idx, row in enumerate(queue):
        wait_time = row['wait_time'] if row['wait_time'] is not None else AVERAGE_WAIT_TIME
        total_time += wait_time
        eta_minutes = total_time
        eta_clock = current_time + timedelta(minutes=eta_minutes)

        queue_display.append({
            'name': row['name'],
            'position': idx + 1,
            'eta': eta_minutes,
            'eta_clock': eta_clock.strftime("%I:%M %p"),
            'color': get_color_by_index(idx, len(queue)),
            'wait_time': wait_time
        })

        if row['name'] == username:
            position = idx + 1
            estimated_time = eta_minutes

    return render_template('status.html',
                           queue=queue_display,
                           username=username,
                           position=position,
                           estimated_time=estimated_time,
                           joined=joined)

@app.route('/exit_queue', methods=['POST'])
def exit_queue():
    username = request.form['username']
    conn = get_db_connection()
    conn.execute('DELETE FROM queue_entries WHERE name = ?', (username,))
    conn.commit()
    conn.close()
    return render_template('thankyou.html', name=username)

@app.route('/admin')
def admin():
    conn = get_db_connection()
    queue = conn.execute('SELECT * FROM queue_entries ORDER BY joined_time').fetchall()
    conn.close()

    current_time = datetime.now()
    display = []
    total_time = 0

    for idx, row in enumerate(queue):
        wait_time = row['wait_time'] if row['wait_time'] is not None else AVERAGE_WAIT_TIME
        total_time += wait_time
        eta_clock = current_time + timedelta(minutes=total_time)

        display.append({
            'id': row['id'],
            'name': row['name'],
            'wait_time': wait_time,
            'eta_clock': eta_clock.strftime("%I:%M %p"),
            'position': idx + 1,
            'color': get_color_by_index(idx, len(queue))
        })

    return render_template('admin.html', queue=display)

@app.route('/update_time', methods=['POST'])
def update_time():
    user_id = request.form['user_id']
    new_time = request.form['wait_time']
    conn = get_db_connection()
    conn.execute('UPDATE queue_entries SET wait_time = ? WHERE id = ?', (new_time, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/next', methods=['POST'])
def next_user():
    conn = get_db_connection()
    first = conn.execute('SELECT * FROM queue_entries ORDER BY joined_time LIMIT 1').fetchone()
    if first:
        conn.execute('INSERT INTO queue_exited (name) VALUES (?)', (first['name'],))
        conn.execute('DELETE FROM queue_entries WHERE id = ?', (first['id'],))
        conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)





