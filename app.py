from flask import Flask, request, redirect, session

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

link_loja = "https://app.powerbi.com/reportEmbed?reportId=f2ee6213-1533-410c-8ceb-f30bbafad857&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b"
link_vendedores = "https://app.powerbi.com/links/PsAlAMGCDf?ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b&pbi_source=linkShare"

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
    user = request.form.get("usuario")
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
    url_painel = link_loja if user == "loja" else link_vendedores
    nome_perfil = "Gerencial (Loja)" if user == "loja" else user.capitalize()

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head><meta charset="UTF-8"><title>Painel - Guará</title></head>
    <body style="background:#121212; color:white; font-family:sans-serif; margin:0; display:flex; flex-direction:column; height:100vh;">
        <div style="background:#1e1e1e; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333;">
            <span style="font-weight:bold; color:#4CAF50;">👤 Usuário: {nome_perfil}</span>
            <a href="/logout" style="background:#dc3545; color:white; padding:8px 16px; border-radius:4px; text-decoration:none; font-weight:bold;">Sair</a>
        </div>
        <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:20px;">
            <div style="background:#1e1e1e; padding:40px; border-radius:10px; max-width:450px; width:100%; border:1px solid #333;">
                <h2 style="color:#f2c811; margin-bottom:15px;">Painel Disponível</h2>
                <p style="color:#ccc; margin-bottom:25px; font-size:14px;">Clique no botão abaixo para abrir o seu painel de controle com segurança no Power BI.</p>
                <a href="{url_painel}" target="_blank" style="background:#f2c811; color:black; padding:16px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:16px; display:block;">
                    🚀 ABRIR PAINEL NO POWER BI
                </a>
            </div>
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