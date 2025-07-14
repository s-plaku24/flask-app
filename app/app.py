from flask import Flask, render_template
import os
import redis
import pandas as pd

app = Flask(__name__, template_folder='template')  # Note: using 'template' folder instead of default 'templates'

# Redis connection
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_password = os.environ.get('REDIS_PASSWORD', '')
redis_conn = redis.Redis(host=redis_host, port=6379, password=redis_password)

def get_hit_count():
    """Increment and return the visitor count"""
    try:
        return int(redis_conn.incr('hits'))
    except redis.exceptions.ConnectionError:
        return 0  # Return 0 instead of a string

@app.route('/')
def hello():
    count = get_hit_count()
    if isinstance(count, str):  # If it's an error string
        return f"Redis connection error: {count}"
    return render_template('hello.html', count=count, name='BIPM')

@app.route('/titanic')
def titanic():
    count = get_hit_count()
    df = pd.read_csv('titanic.csv')
    
    # Calculate survival counts by sex
    survival_counts = df.groupby(['Sex', 'Survived']).size().unstack()
    survival_counts = survival_counts.rename(columns={0: 'Died', 1: 'Survived'})
    
    # Prepare data for chart
    chart_data = {
        'labels': list(survival_counts.index),
        'datasets': [{
            'label': 'Died',
            'data': list(survival_counts['Died']),
            'backgroundColor': 'rgba(255, 99, 132, 0.5)'
        }, {
            'label': 'Survived',
            'data': list(survival_counts['Survived']),
            'backgroundColor': 'rgba(54, 162, 235, 0.5)'
        }]
    }
    
    table_html = df.head().to_html(classes='data', header="true")
    return render_template('titanic.html', 
                         table_html=table_html, 
                         count=count,
                         chart_data=chart_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)