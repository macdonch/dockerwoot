import subprocess
from subprocess import check_output
from flask import Flask, render_template

def get_ip_from_shell():
    stdout = check_output(['./scripts/getnodeip.sh']).decode('utf-8')
    return stdout

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("hello.html")

if __name__ == '__main__':
    get_ip_from_shell()
    app.run(debug=True, host='0.0.0.0')
