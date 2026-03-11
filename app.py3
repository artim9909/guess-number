from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

secret_number = random.randint(1,100)
attempts = 0
game_over = False
leaderboard = []

HTML = """

<!DOCTYPE html>
<html>
<head>
<title>Colorful Prediction Game</title>

<style>

body{
font-family:Arial;
background:linear-gradient(120deg,#ff9a9e,#fad0c4,#fbc2eb,#a6c1ee);
background-size:400% 400%;
animation:gradient 10s ease infinite;
height:100vh;
display:flex;
justify-content:center;
align-items:center;
}

@keyframes gradient{
0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}
}

.box{
background:white;
padding:40px;
border-radius:20px;
width:420px;
text-align:center;
box-shadow:0 15px 40px rgba(0,0,0,0.25);
}

h1{
color:#444;
}

input{
padding:12px;
font-size:18px;
width:140px;
border-radius:8px;
border:2px solid #ddd;
}

button{
padding:12px 25px;
margin:10px;
border:none;
background:linear-gradient(45deg,#ff512f,#dd2476);
color:white;
font-size:16px;
border-radius:10px;
cursor:pointer;
transition:0.3s;
}

button:hover{
transform:scale(1.1);
}

.result{
font-size:20px;
margin-top:10px;
font-weight:bold;
}

.hint{
margin-top:8px;
color:#333;
}

table{
width:100%;
margin-top:15px;
border-collapse:collapse;
}

th{
background:#ff512f;
color:white;
padding:6px;
}

td{
padding:6px;
border-bottom:1px solid #ddd;
}

.good{
color:green;
font-size:22px;
}

.bad{
color:red;
font-size:20px;
}

</style>

</head>

<body>

<div class="box">

<h1>🎮 Number Prediction Game</h1>
<p>Guess number between <b>1 - 100</b></p>

{% if not game_over %}

<form method="POST">
<input type="number" name="guess" min="1" max="100" required>
<br>
<button type="submit">Guess</button>
</form>

{% endif %}

<div class="result">{{message}}</div>
<div class="result">{{distance}}</div>
<div class="hint">{{ai_hint}}</div>

<p><b>Attempts:</b> {{attempts}}</p>

{% if game_over %}

<h2 class="good">👏 Good Job! You Won!</h2>

<form method="POST">
<button name="restart" value="1">🔄 Restart Game</button>
</form>

{% endif %}

<h3>🏆 Leaderboard</h3>

<table>
<tr>
<th>Rank</th>
<th>Attempts</th>
</tr>

{% for score in leaderboard %}

<tr>
<td>{{loop.index}}</td>
<td>{{score}}</td>
</tr>

{% endfor %}

</table>

</div>

</body>
</html>

"""

@app.route("/", methods=["GET","POST"])
def home():
    global secret_number, attempts, game_over, leaderboard

    message=""
    distance=""
    ai_hint=""

    if request.method=="POST":

        if "restart" in request.form:
            secret_number=random.randint(1,100)
            attempts=0
            game_over=False

        elif not game_over:

            guess=int(request.form["guess"])
            attempts+=1

            diff=abs(secret_number-guess)

            if guess==secret_number:

                message=f"🎉 Correct! Number was {secret_number}"
                distance=f"You solved it in {attempts} attempts"

                leaderboard.append(attempts)
                leaderboard=sorted(leaderboard)[:5]

                game_over=True

            else:

                message="😄 Demag chala beta!"

                if guess>secret_number:
                    ai_hint=f"🤖 AI Hint: Try LOWER than {guess}"
                else:
                    ai_hint=f"🤖 AI Hint: Try HIGHER than {guess}"

                if diff<=5:
                    distance=f"🔥 HOT! Only {diff} away"
                elif diff<=15:
                    distance=f"🙂 Warm! {diff} away"
                else:
                    distance=f"❄️ Cold! {diff} away"

    return render_template_string(
        HTML,
        message=message,
        distance=distance,
        ai_hint=ai_hint,
        attempts=attempts,
        leaderboard=leaderboard,
        game_over=game_over
    )


if __name__=="__main__":
    app.run(debug=True)