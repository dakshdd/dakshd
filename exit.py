from flask import Blueprint, render_template
import datetime

bp = Blueprint('exit', __name__)

@bp.route('/exit')
def exit():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("exit_log.txt", "a") as f:
        f.write(f"User exited at {timestamp}\n")
    return render_template('exit.html')
