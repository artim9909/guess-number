from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

secret_number = random.randint(1, 100)
attempts = 0
game_over = False

HTML = """

<!DOCTYPE html>
<html>
<head>
<title>Number Prediction Game</title>

<style>

body{
font-family: Arial;
background: linear-gradient(135deg,#4facfe,#00f2fe);
height:100vh;
display:flex;
justify-content:center;
align-items:center;
}

.container{
background:white;
padding:40px;
border-radius:15px;
text-align:center;
width:380px;
box-shadow:0 15px 30px rgba(0,0,0,0.2);
}

h1{
color:#333;
}

input{
padding:10px;
font-size:18px;
width:120px;
border-radius:6px;
border:1px solid #ccc;
}

button{
padding:10px 20px;
margin-top:10px;
border:none;
background:#4facfe;
color:white;
font-size:16px;
border-radius:8px;
cursor:pointer;
}

button:hover{
background:#0077ff;
}

.result{
margin-top:15px;
font-size:18px;
}

.attempt{
margin-top:10px;
font-weight:bold;
}

</style>

</head>

<body>

<div class="container">

<h1>🎮 Number Prediction Game</h1>

<p>Guess a number between <b>1 and 100</b></p>

{% if not game_over %}

<form method="POST">

<input type="number" name="guess" min="1" max="100" required>
<br><br>
<button type="submit">Predict</button>

</form>

{% endif %}

<div class="result">

<p>{{ message }}</p>
<p>{{ distance }}</p>

</div>

<div class="attempt">

Attempts: {{ attempts }}

</div>

{% if game_over %}

<h2>🏆 Correct! Game Finished</h2>

{% endif %}

</div>

</body>
</html>

"""

@app.route("/", methods=["GET", "POST"])
def home():
    global secret_number, attempts, game_over

    message = ""
    distance = ""

    if request.method == "POST" and not game_over:
        guess = int(request.form["guess"])
        attempts += 1

        diff = abs(secret_number - guess)

        if guess == secret_number:
            message = f"🎉 Correct! The number was {secret_number}"
            distance = f"You found it in {attempts} attempts!"
            game_over = True

        else:

            if diff <= 5:
                distance = f"🔥 Very Close! Only {diff} away"
            elif diff <= 15:
                distance = f"🙂 Close! {diff} away"
            else:
                distance = f"❄️ Far! {diff} away"

            if guess > secret_number:
                message = "📉 Your guess is HIGH"
            else:
                message = "📈 Your guess is LOW"

    return render_template_string(
        HTML,
        message=message,
        distance=distance,
        attempts=attempts,
        game_over=game_over
    )


if __name__ == "__main__":
    app.run(debug=True)