from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data for demonstration
    data = [
        {'name': 'Alice', 'age': 28, 'city': 'New York'},
        {'name': 'Bob', 'age': 35, 'city': 'San Francisco'},
        {'name': 'Charlie', 'age': 22, 'city': 'Los Angeles'},
        # Add more data as needed
    ]

    return render_template('indexx.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
