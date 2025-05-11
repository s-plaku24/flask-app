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