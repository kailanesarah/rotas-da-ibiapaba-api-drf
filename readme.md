# API - Parte 1: Autenticação, Registro e Login

Este repositório contém a primeira parte da API, onde implementamos funcionalidades básicas de **autenticação**, **registro de usuários** e **login**, utilizando Django REST Framework (DRF) e o pacote `djangorestframework-simplejwt` para autenticação via JSON Web Tokens (JWT).

---

## Funcionalidades implementadas até agora

- Registro de usuários (estabelecimentos)
- Login via cookies JWT 
- Reset para que o usuario consiga um novo acesso

---

## Tecnologias utilizadas

- **Python 3.x**
- **Django 4.x**
- **Django REST Framework (DRF)**
- **djangorestframework-simplejwt** — para autenticação JWT e gerenciamento de tokens
- **SQLite** (padrão, para desenvolvimento)

---

## Estrutura de rotas principais

### Rotas de autenticação (`authentication` app)

| Método | Endpoint                                | Descrição                                             |
|--------|----------------------------------------|-------------------------------------------------------|
| POST   | `/api/v1/authentication/login/`        | Realiza login, retorna tokens JWT (access + refresh)  |
| POST   | `/api/v1/authentication/logout/`       | Realiza logout, blacklist do refresh token            |
| POST   | `/api/v1/authentication/verifyCode/` | Verifica codigo enviado por email         |
| POST   | `/api/v1/authentication/api/token/refresh/` | Renova o access token usando o refresh token     |
| POST   | `/api/v1/authentication/verifyCode`    | Faz a validação do código enviado por email

### Rotas de usuários (`accounts` app)

| Método | Endpoint                       | Descrição                      |
|--------|-------------------------------|-------------------------------|
| POST   | `/api/v1/accounts/auth/register/` | Registro de novo estabelecimento |
| GET    | `/api/v1/accounts/auth/list/`     | Listar estabelecimentos registrados |


---

## Como rodar a aplicação

1. Clone o repositório:

```bash
    git clone https://github.com/NexTech-Business/rotas-da-ibiapaba-api.git
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

5. Crie um usuário (opcional, para acessar o admin):

```bash
    python manage.py createsuperuser
```

6. Rode o servidor de desenvolvimento:
```bash
    python manage.py runserver
```
---
## Testando a API

- Utilize o Postman, Insomnia ou outra ferramenta para fazer requisições HTTP.

- Para login, envie um POST para /api/v1/authentication/login/ com usuário e senha.
  
- Para validar o token, confira o codigo enviado por email para a conta disponibilizada

- Para renovar o token, envie um POST para /api/v1/authentication/api/token/refresh/ com o refresh token no corpo.

- Para logout, envie um POST para /api/v1/authentication/logout/ com o refresh token para invalidar.

- Para registrar um estabelecimento, envie um POST para /api/v1/accounts/auth/register/ com os dados necessários.

## Observações importantes
- A blacklist para refresh tokens deve estar habilitada no SimpleJWT para que o logout funcione corretamente.

- O access token possui validade curta para garantir maior segurança.

- O refresh token é utilizado para gerar novos access tokens sem que o usuário precise realizar login novamente.

- Este é apenas o começo do projeto, outras funcionalidades como autorização, permissões específicas e testes serão implementadas em breve.
