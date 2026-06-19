from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
# Chave secreta para manter as sessões dos usuários seguras
app.secret_key = "guara_secret_2026"

# Lista de usuários permitidos
usuarios = {
    "loja": "Gerencial@Guara2026",
    "abner": "Guara@vendas2026",
    "samuel": "Guara@vendas2026",
    "thiago": "Guara@vendas2026",
    "eduardo": "Guara@vendas2026",
    "ana": "Guara@vendas2026"
}

# --- VISUAL DA PÁGINA DE LOGIN (HTML integrado) ---
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Guará</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        h2 { color: #333; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .error { color: red; margin-top: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Acesso ao Painel</h2>
        <form action="/login" method="POST">
            <input type="text" name="usuario" placeholder="Usuário" required>
            <input type="password" name="senha" placeholder="Senha" required>
            <button type="submit">Entrar</button>
        </form>
        {% if erro %}
            <p class="error">{{ erro }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

# --- ROTAS DO SISTEMA ---

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template_string(LOGIN_HTML)


@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("usuario")
    senha = request.form.get("senha")

    if user in usuarios and usuarios[user] == senha:
        session["user"] = user
        return redirect("/dashboard")

    return render_template_string(LOGIN_HTML, erro="Usuário ou senha inválidos")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    # Banco de links do Power BI (Links da Ana e Eduardo atualizados)
    dashboards = {
        "loja": "https://app.powerbi.com/reportEmbed?reportId=c39f0524-5134-44b1-8ba5-9599b3f1cdc2&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",
        
        "ana": "https://app.powerbi.com/reportEmbed?reportId=80e15aa9-77d0-4d5b-b688-81d37f9b7766&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",
        
        "eduardo": "https://app.powerbi.com/reportEmbed?reportId=a07dc1bf-7609-4ec8-97cd-a0e4c7c819e0&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b"
    }

    if user in dashboards:
        return f"""
        <html>
        <head>
            <title>Dashboard - {user.capitalize()}</title>
            <style>
                .btn-sair {{ position: fixed; top: 10px; right: 10px; z-index: 9999; background: #dc3545; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; font-family: Arial; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
                .btn-sair:hover {{ background: #bd2130; }}
            </style>
        </head>
        <body>
            <a href="/logout" class="btn-sair">Sair</a>
            <iframe
                src="{dashboards[user]}"
                style="position:fixed; top:0; left:0; width:100%; height:100%; border:none;"
                allowFullScreen="true">
            </iframe>
        </body>
        </html>
        """

    # Caso o usuário exista mas ainda não tenha um link cadastrado acima
    return f"""
    <div style="text-align:center; margin-top:100px; font-family: Arial, sans-serif;">
        <h3>Olá {user.capitalize()}, seu relatório ainda está sendo preparado.</h3>
        <p>Por favor, solicite a liberação ao administrador.</p>
        <a href="/logout" style="color: #007bff; text-decoration: none; font-weight: bold; border: 1px solid #007bff; padding: 5px 10px; border-radius: 4px;">Voltar para o Login</a>
    </div>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)