from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Hardcoded users
users = {
    "admin": "admin123",
    "teacher": "teach123",
    "parent": "parent123"
}

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return render_template('dashboard.html', username=username)
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
