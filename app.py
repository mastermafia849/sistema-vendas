from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "guara_secret_2026"

usuarios = {
    "loja": "Gerencial@Guara2026",
    "abner": "Guara@vendas2026",
    "samuel": "Guara@vendas2026",
    "thiago": "Guara@vendas2026",
    "eduardo": "Guara@vendas2026",
    "ana": "Guara@vendas2026"
}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("usuario")
    senha = request.form.get("senha")

    if user in usuarios and usuarios[user] == senha:
        session["user"] = user
        return redirect("/dashboard")

    return "Usuário ou senha inválidos"

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return f"""
    <h1>Bem-vindo ao Sistema Guaralub</h1>
    <p>Usuário: {session['user']}</p>
    <a href="/logout">Sair</a>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)