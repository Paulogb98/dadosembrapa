from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from extract_data import script_comercializacao, script_exportacao, script_importacao, script_processamento, \
    script_producao
from users import USERS

app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'viticultura69'  # Alterar para uma chave secreta segura
jwt = JWTManager(app)
USERS = USERS

# ROTA HOMEPAGE - INSTRUÇÕES GERAIS
@app.route('/')
def index():
    info = {
        "message": "Bem-vindo à API de Dados de Viticultura",
        "description": "Esta API fornece dados sobre comercialização, exportação, importação, processamento e produção "
                       "de produtos vitícolas no Brasil entre os anos de 1970 a 2023.",
        "routes": {
            "/comercializacao": {
                "description": "Retorna dados de comercialização de produtos vitícolas.",
                "example": "/comercializacao?ano=2022"
            },
            "/exportacao": {
                "description": "Retorna dados de exportação de produtos vitícolas.",
                "example": "/exportacao?ano=2022"
            },
            "/importacao": {
                "description": "Retorna dados de importação de produtos vitícolas.",
                "example": "/importacao?ano=2022"
            },
            "/processamento": {
                "description": "Retorna dados de processamento de uvas.",
                "example": "/processamento?ano=2022"
            },
            "/producao": {
                "description": "Retorna dados de produção de uvas.",
                "example": "/producao?ano=2022"
            },
            "/login": {
                "description": "Rota para obter um token JWT. Este token deve ser incluído em cada requisição "
                               "subsequente para rotas protegidas.",
                "example": {
                    "method": "POST",
                    "body": {
                        "username": "seu_username",
                        "password": "sua_senha"
                    },
                    "response": {
                        "access_token": "seu_token_jwt"
                    }
                }
            }
        },
        "usage": (
            "Para acessar os dados, faça uma requisição GET para uma das rotas acima. "
            "Você pode opcionalmente especificar um ano como um parâmetro de consulta na URL, por exemplo: "
            "/comercializacao?ano=2022. Se nenhum ano for especificado, dados de todos os anos disponíveis (de 1970 a 2023) "
            "serão retornados. Para obter um token JWT, faça uma requisição POST para /login com seu nome de usuário e senha. "
            "Inclua o token JWT no cabeçalho Authorization das requisições para acessar rotas protegidas, "
            "no formato: 'Bearer <seu_token_jwt>'."
        ),
        "security": (
            "A API utiliza autenticação baseada em JWT (JSON Web Token). Após obter o token através da rota /login, "
            "o token deve ser incluído no cabeçalho Authorization das requisições para acessar rotas protegidas. "
            "Utilize o formato: 'Bearer <seu_token_jwt>'. Assegure-se de manter o token seguro e não o compartilhe "
            "com terceiros."
        ),
        "contact": "https://www.linkedin.com/in/paulo-goiss/"
    }
    return jsonify(info)

# -----------------------------------------------------
# ROTA DE LOGIN - ACESSO JWT
@app.route('/login', methods=['POST'])
def login():
    # Obtém o nome de usuário e a senha do corpo da requisição JSON
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Verifica se o usuário existe e se a senha está correta
    if username not in USERS or USERS[username] != password:
        return jsonify({"msg": "Usuário ou senha inválidos"}), 401

    # Cria um token JWT com o nome de usuário como identidade
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# -----------------------------------------------------
# PRINCIPAIS ROTAS DA API - ACESSO AOS DADOS
@app.route('/comercializacao')
@jwt_required()
def get_items_comercializacao():
    ano = request.args.get('ano', None)
    return script_comercializacao(ano)

@app.route('/exportacao')
@jwt_required()
def get_items_exportacao():
    ano = request.args.get('ano', None)
    return script_exportacao(ano)

@app.route('/importacao')
@jwt_required()
def get_items_importacao():
    ano = request.args.get('ano', None)
    return script_importacao(ano)

@app.route('/processamento')
@jwt_required()
def get_items_processamento():
    ano = request.args.get('ano', None)
    return script_processamento(ano)

@app.route('/producao')
@jwt_required()
def get_items_producao():
    ano = request.args.get('ano', None)
    return script_producao(ano)

if __name__ == '__main__':
    app.run(debug=True)
