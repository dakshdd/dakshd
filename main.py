from flask import Flask, render_template, request, redirect
import webbrowser, threading

from actions import registration, admission, exit

app = Flask(__name__)
app.register_blueprint(registration.bp)
app.register_blueprint(admission.bp)
app.register_blueprint(exit.bp)

@app.route('/')
def home():
    return render_template('front_page.html')

@app.route('/handle_action', methods=['POST'])
def handle_action():
    action = request.form['action']
    if action == 'registration':
        return redirect('/registration')
    elif action == 'new_admission':
        return redirect('/admission')
    elif action == 'fee_entry':
        return "Fee Entry Page (Coming Soon)"
    elif action == 'defaulter_report':
        return "Defaulter Report Page (Coming Soon)"
    elif action == 'printing_report':
        return "Printing Report Page (Coming Soon)"
    elif action == 'utils':
        return "Utils Page (Coming Soon)"
    elif action == 'exit':
        return render_template('exit.html')
    else:
        return "Unknown action"

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
