from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "guara_secret_2026"

# Lista de usuários atualizada com o Manoel
usuarios = {
    "loja": "Gerencial@Guara2026",
    "abner": "Guara@vendas2026",
    "samuel": "Guara@vendas2026",
    "eduardo": "Guara@vendas2026",
    "manoel": "Guara@vendas2026"
}

# Dicionário mapeando o link específico de cada usuário
links_paineis = {
    "loja": "https://app.powerbi.com/reportEmbed?reportId=45722072-420a-401b-a23e-abd3bc2c6f1a&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",
    "abner": "https://app.powerbi.com/reportEmbed?reportId=cfb7cc32-61fd-4422-a0dd-b9cd034276ca&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",
    "eduardo": "https://app.powerbi.com/reportEmbed?reportId=6954fefd-ee4e-499a-8278-299d5d148eca&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",
    "samuel": "https://app.powerbi.com/reportEmbed?reportId=b1ed3c24-a20e-440e-831f-1fb90bada28c&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",
    "manoel": "https://app.powerbi.com/reportEmbed?reportId=3e45810d-d4ed-4b0d-949e-96a61ef8f237&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b",


}

@app.route("/")
def home():
    if "user" in session: 
        return redirect("/dashboard")
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head><meta charset="UTF-8"><title>Login - Guará</title></head>
    <body style="background:#121212; color:white; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <div style="background:#1e1e1e; padding:40px; border-radius:10px; width:350px; text-align:center; border:1px solid #333;">
            <h2 style="color:#4CAF50; margin-bottom:20px;">Sistema Guará</h2>
            <form action='/login' method='POST'>
                <input type='text' name='usuario' placeholder='Usuário' required style="width:100%; padding:12px; margin-bottom:15px; background:#2a2a2a; border:1px solid #444; color:white; box-sizing:border-box;">
                <input type='password' name='senha' placeholder='Senha' required style="width:100%; padding:12px; margin-bottom:20px; background:#2a2a2a; border:1px solid #444; color:white; box-sizing:border-box;">
                <button type='submit' style="width:100%; padding:12px; background:#f2c811; color:black; border:none; font-weight:bold; cursor:pointer;">Entrar</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("usuario").lower().strip()
    senha = request.form.get("senha")
    if user in usuarios and usuarios[user] == senha:
        session["user"] = user
        return redirect("/dashboard")
    return "Dados incorretos. <a href='/'>Voltar</a>"

@app.route("/dashboard")
def dashboard():
    if "user" not in session: 
        return redirect("/")
     
    user = session["user"]
    url_painel = links_paineis.get(user, links_paineis["loja"])
    nome_perfil = "Gerencial (Loja)" if user == "loja" else user.capitalize()

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head><meta charset="UTF-8"><title>Painel - Guará</title></head>
    <body style="background:#121212; color:white; font-family:sans-serif; margin:0; display:flex; flex-direction:column; height:100vh;">
        <div style="background:#1e1e1e; padding:12px 30px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333;">
            <span style="font-weight:bold; color:#4CAF50;">👤 Usuário: {nome_perfil}</span>
            <a href="/logout" style="background:#dc3545; color:white; padding:6px 14px; border-radius:4px; text-decoration:none; font-weight:bold; font-size:14px;">Sair</a>
        </div>
        <div style="flex:1; width:100%; background:#121212;">
            <iframe title="Painel Guara" width="100%" height="100%" src="{url_painel}" frameborder="0" allowFullScreen="true"></iframe>
        </div>
    </body>
    </html>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)