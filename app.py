from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'  # Necessário para controlar as sessões de login

# Dicionário de usuários e senhas
usuarios = {
    "loja": "Gerencial@Guara2026",
    "abner": "Guara@vendas2026",
    "samuel": "Guara@vendas2026",
    "thiago": "Guara@vendas2026",
    "eduardo": "Guara@vendas2026",
    "ana": "Guara@vendas2026"
}

# Links do Power BI para cada perfil
LINK_LOJA = "https://app.powerbi.com/reportEmbed?reportId=f2ee6213-1533-410c-8ceb-f30bbafad857&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b"
LINK_VENDEDORES = "https://app.powerbi.com/reportEmbed?reportId=f2ee6213-1533-410c-8ceb-f30bbafad857&autoAuth=true&ctid=425c7c8c-859b-4c1b-9c2a-b609c6a8e14b" # Altere para o link específico de vendedores se houver outro

@app.route('/', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            erro = "Usuário ou senha inválidos!"
            
    return render_template('login.html', erro=erro)

@app.route('/dashboard')
def dashboard():
    # BLINDAGEM: Se não estiver logado, é barrado e volta para a tela de login
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario_atual = session['usuario']
    
    # Define o nome amigável para exibir na tela
    if usuario_atual == "loja":
        nome_exibicao = "Gerencial (Loja)"
        link_painel = LINK_LOJA
    else:
        nome_exibicao = f"Vendedor({usuario_atual.capitalize()})"
        link_painel = LINK_VENDEDORES
        
    return render_template('dashboard.html', usuario=nome_exibicao, link_painel=link_painel)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)