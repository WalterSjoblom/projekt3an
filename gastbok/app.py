from flask import Flask, request, render_template, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
JSON_FILE = 'data.json'


def load_posts():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_posts(posts):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


@app.route('/')
def gastbok():
    posts = load_posts()
    posts_senaste_forst = list(reversed(posts))
    return render_template('gastbok.html', posts=posts_senaste_forst)


@app.route('/skicka', methods=['POST'])
def skicka():
    namn = request.form.get('namn', '').strip()
    meddelande = request.form.get('meddelande', '').strip()

    if namn and meddelande:
        posts = load_posts()
        posts.append({
            'namn': namn,
            'meddelande': meddelande,
            'tid': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        save_posts(posts)

    return redirect(url_for('gastbok'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')