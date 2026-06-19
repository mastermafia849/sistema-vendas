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

    user = session["user"]

    # O link da Ana foi inserido logo abaixo:
    dashboards = {
        "loja": "https://app.powerbi.com/reportEmbed?reportId=c39f0524-5134-44b1-8ba5-9599b3f1cdc2&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",

        "ana": "https://app.powerbi.com/reportEmbed?reportId=80e15aa9-77d0-4d5b-b688-81d37f9b7766&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b"
    }

    if user in dashboards:
        return f"""
        <iframe
            src="{dashboards[user]}"
            style="position:fixed; top:0; left:0; width:100%; height:100%; border:none;"
            allowFullScreen="true">
        </iframe>
        """

    return """
    <h3 style="text-align:center; margin-top:50px;">
        Acesso negado ou relatório não configurado para este usuário.
    </h3>
    <div style="text-align:center;">
        <a href="/logout">Sair</a>
    </div>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)