from flask import Flask, request, render_template, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
JSON_FILE = 'data.json'


def load_posts():
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_posts(posts):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


@app.route('/')
def gastbok():
    return render_template('gastbok.html', posts=load_posts()[::-1])


@app.route('/skicka', methods=['POST'])
def skicka():
    namn = request.form.get('namn', '').strip()
    email = request.form.get('email', '').strip()
    meddelande = request.form.get('meddelande', '').strip()

    if namn and email and meddelande:
        posts = load_posts()
        posts.append({
            'namn': namn,
            'email': email,
            'meddelande': meddelande,
            'tid': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        save_posts(posts)

    return redirect(url_for('gastbok'))


if __name__ == '__main__':
    app.run(debug=True)