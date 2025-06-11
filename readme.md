# API - Parte 1: Autenticação, Registro e Login

Este repositório contém a primeira parte da API, onde implementamos funcionalidades básicas de **autenticação**, **registro de usuários** e **login**, utilizando Django REST Framework (DRF) e o pacote `djangorestframework-simplejwt` para autenticação via JSON Web Tokens (JWT).

---

## Funcionalidades
- Registro de usuários (estabelecimentos)
- Login via JWT com cookies
- Reset e redefinição de senha
- Logout com invalidação de token
- Listagem de estabelecimentos
- [Próximas funcionalidades em desenvolvimento]

---

## Tecnologias utilizadas

- **Python 3.x**
- **Django 4.x**
- **Django REST Framework (DRF)**
- **djangorestframework-simplejwt** — para autenticação JWT e gerenciamento de tokens
- **SQLite** (padrão, para desenvolvimento)

---

## Pré-requisitos
- Python 3.8 ou superior
- Pip instalado
- Ambiente virtual (recomendado)
- Variáveis de ambiente necessárias
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
    - BASE_URL

---

## Estrutura de rotas principais

### Rotas de autenticação (`authentication` app)

| Método | Endpoint                                             | Descrição                                                             |
|--------|------------------------------------------------------|----------------------------------------------------------------------|
| POST   | `/api/v1/authentication/login/`                      | Realiza login, retorna tokens JWT (access + refresh)                |
| POST   | `/api/v1/authentication/logout/`                     | Realiza logout, blacklist do refresh token                           |
| POST   | `/api/v1/authentication/verifyCode/`                 | Verifica código enviado por email                                    |
| POST   | `/api/v1/authentication/reset_password/`             | Envia o link com os dados de reset para o email do usuário          |
| PATCH  | `/api/v1/authentication/reset_confirm_password/`     | Reseta a senha do usuário                                            |
| POST   | `/api/v1/authentication/api/token/refresh/`          | Renova o access token usando o refresh token                         |
### Rotas de usuários (`accounts` app)

| Método | Endpoint                       | Descrição                      |
|--------|-------------------------------|-------------------------------|
| POST   | `/api/v1/accounts/auth/register/` | Registro de novo estabelecimento |
| GET    | `/api/v1/accounts/auth/list/`     | Listar estabelecimentos registrados |


---

## Como rodar a aplicação

1. Dê um fork em nosso repositório:

```bash
    git clone https://github.com/NexTech-Business/rotas-da-ibiapaba-api.git
```

1. Clone o seu repositório:

```bash
    git clone https://github.com/seu-repositorio/rotas-da-ibiapaba-api.git
    cd rotas-da-ibiapaba-api
```

2. Crie o ambiente virtual:

```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
    pip install -r requirements.txt
```

4. Faça as migrações do banco de dados:

```bash
    python manage.py migrate
```

5. Crie um super usuário (para acessar o admin):

```bash
    python manage.py createsuperuser
```

4. Cadastre novas categorias de estabelecimento(necessario para fazer cadastros de estabelecimeto):
```bash
    #rota para criação e listagens de categorias em desenvolvimento
```

6. Rode o servidor de desenvolvimento:
```bash
    python manage.py runserver
```

## Testando a API

- Utilize o Postman, Insomnia ou outra ferramenta para fazer requisições HTTP.

- Para login, envie um POST para /api/v1/authentication/login/ com usuário e senha.
  
- Para validar o token, confira o codigo enviado por email para a conta disponibilizada

- Para renovar o token, envie um POST para /api/v1/authentication/api/token/refresh/ com o refresh token no corpo.

### Arquivo Postman
Para facilitar, disponibilizamos um arquivo Postman com todas as requisições configuradas, incluindo os dados dos corpos (body). Importe esse arquivo na sua ferramenta para começar a testar rapidamente.

## Observações importantes sobre autenticação e logout
- Os tokens JWT são enviados e armazenados via cookies HTTP-only para segurança.  
- Após a validação do código, as rotas serão autenticadas via cookies  
- O access token tem validade curta para proteger o sistema contra acessos não autorizados.  
- O refresh token é usado para renovar o access token sem que o usuário precise logar novamente.  
- No logout, os cookies contendo os tokens são removidos, mas os tokens não são invalidados no servidor e continuam válidos até expirarem.  
- Para implementar invalidação imediata de tokens, seria necessário um mecanismo de blacklist, que não está presente nesta versão da API.
- Este é apenas o começo do projeto, outras funcionalidades como autorização, permissões específicas e testes serão implementadas em breve.

