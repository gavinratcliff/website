import sys
from flask import Flask, request, abort
import os
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Fetch the latest changes from the repo
        subprocess.run(['git', 'fetch', 'origin', 'main'], cwd='/root/website/')
        subprocess.run(['git', 'pull'], cwd='/root/website/')

        # Run your script
        subprocess.run(['./deploy.sh'], cwd='/root/website/')

        return 'Success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

