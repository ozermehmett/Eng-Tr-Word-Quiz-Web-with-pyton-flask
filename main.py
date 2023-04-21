from flask import Flask, render_template, request, flash, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "ben-bir-insanim"

with open("words.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

data = {}
for line in lines:
    key, value = line.strip().split("= ", maxsplit=1)
    data[key] = value


@app.route('/')
def home():
    session['visited'] = True
    return render_template('home.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'visited' not in session:
        session['visited'] = False

    if request.method == 'POST':
        selected_keys = request.form.getlist('options')
        question = selected_keys[0]
        answer = request.form.get('answer')
        if answer == question:
            flash(f"Doğru! {question} = {data[question]}")
            # Rasgele seçim yapmak için
            keys = list(data.keys())
            selected_keys = random.sample(keys, 4)
            question = selected_keys[0]
            ans1 = selected_keys[1]
            ans2 = selected_keys[2]
            ans3 = selected_keys[3]
        else:
            flash(f"Yanlış! Cevap: {answer} = {data[answer]}", 'error')

        session['visited'] = True
        return redirect(url_for('quiz'))

    else:
        keys = list(data.keys())
        selected_keys = random.sample(keys, 4)
        question = selected_keys[0]
        ans1 = selected_keys[1]
        ans2 = selected_keys[2]
        ans3 = selected_keys[3]

        options = [question, ans1, ans2, ans3]
        random.shuffle(options)

        return render_template('quiz.html', options=options, question=question, ans1=ans1, ans2=ans2, ans3=ans3, data=data, visited=session['visited'])


if __name__ == '__main__':
    app.run(debug=True)
