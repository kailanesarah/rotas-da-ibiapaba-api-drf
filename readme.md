# API Rotas da Ibiapaba - Módulo 1: Autenticação, Registro e Gerenciamento de Usuários

Este repositório contém a primeira etapa do desenvolvimento da API, focada na implementação das funcionalidades essenciais de **autenticação**, **registro de usuários** e **login**.  
Utilizamos o **Django REST Framework (DRF)** em conjunto com o pacote `djangorestframework-simplejwt` para autenticação segura via **JSON Web Tokens (JWT)**, garantindo proteção e controle de acesso robustos.

---

## ✅ Funcionalidades

- **Cadastro de Usuários**  
  Permite o registro de estabelecimentos e administradores.

- **Autenticação via JWT com Cookies Seguros**  
  Login utilizando tokens JWT armazenados em cookies HTTPOnly para maior segurança.

- **Recuperação de Senha**  
  Envio de e-mail para redefinição de senha com token de verificação.

- **Logout Seguro**  
  Invalida os tokens armazenados ao realizar logout.

- **Listagem de Estabelecimentos**  
  Exibe todos os estabelecimentos cadastrados no sistema.

- **Criação de Estabelecimentos com Categorias**  
  Permite o cadastro de novos estabelecimentos e associação com categorias específicas.

- **Reenvio de Código de Verificação**  
  Possibilidade de reenviar o código necessário para login ou confirmação de e-mail.

- **Renovação de Tokens JWT (Access e Refresh)**  
  Geração de novos tokens JWT e atualização automática nos cookies do usuário.


---

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Django 4.x**
- **Django REST Framework (DRF)**
- **djangorestframework-simplejwt** — autenticação via JWT e gerenciamento de tokens
- **PostgreSQL** — banco de dados relacional usado em ambiente de produção
- **SQLite** — banco de dados leve usado em ambiente de desenvolvimento local
- **Docker & Docker Compose** — conteinerização da aplicação e orquestração de serviços

---

## ⚙️ Pré-requisitos

Antes de iniciar o projeto, certifique-se de ter os seguintes itens instalados e configurados:

- **Python 3.8 ou superior**
- **pip** — gerenciador de pacotes do Python
- **Ambiente virtual** (recomendado) — para isolamento das dependências

### 🔐 Variáveis de Ambiente Necessárias

Certifique-se de configurar as seguintes variáveis de ambiente:

- `EMAIL_HOST_USER` — e-mail remetente (usado para envio de mensagens automáticas)
- `EMAIL_HOST_PASSWORD` — senha ou token de acesso do e-mail remetente
- `BASE_URL` — URL base da API (ex: `http://localhost:8000`)
- `URL_FRONT` — URL do front-end que receberá os links de redefinição de senha e outros fluxos


---

## 🔀 Estrutura de Rotas Principais

### Rotas de autenticação (`authentication` app)

## 🔐 Rotas de Autenticação

| Método | Endpoint                                              | Descrição                                                                 |
|--------|-------------------------------------------------------|---------------------------------------------------------------------------|
| POST   | `/api/v1/authentication/login/`                       | Realiza login e retorna tokens JWT (access e refresh)                    |
| POST   | `/api/v1/authentication/logout/`                      | Realiza logout e adiciona o refresh token à blacklist                    |
| POST   | `/api/v1/authentication/verifyCode/`                  | Verifica o código enviado por e-mail para completar o login              |
| POST   | `/api/v1/authentication/resend_code/`                 | Reenvia o código de verificação para o e-mail                            |
| POST   | `/api/v1/authentication/reset_password/`              | Envia um link de redefinição de senha para o e-mail do usuário           |
| POST   | `/api/v1/authentication/token/refresh/`               | Renova tokens de acesso e refresh                                        |
| PATCH  | `/api/v1/authentication/reset_confirm_password/`      | Redefine a senha do usuário a partir do token de recuperação             |



### Rotas de Usuários (`accounts` app)

| Método | Endpoint                           | Descrição                            |
|--------|-----------------------------------|------------------------------------|
| POST   | `/api/v1/accounts/establishment/` | Registrar novo estabelecimento     |
| GET    | `/api/v1/accounts/establishment/` | Listar estabelecimentos registrados|
| POST   | `/api/v1/accounts/admin/`         | Criar novo administrador           |

---
### Rotas de categorias (`categories` app)

| Método | Endpoint                       | Descrição                      |
|--------|-------------------------------|-------------------------------|
| POST   | `/api/v1/categories/categorie/` | Registro de nova categoria |
| GET    | `/api/v1/categories/categorie/`     | Listar categorias registradas |

---


## 🚀 Como rodar a aplicação

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
    python manage.py makemigrations
    python manage.py migrate
```

5. Cadastre novas categorias de estabelecimento(necessario para fazer cadastros de estabelecimeto):
```bash
    /api/v1/categories/categorie/
```

6. Rode o servidor de desenvolvimento:
```bash
    python manage.py runserver
```

---
## 🧪 Testando a API

- Utilize ferramentas como **Postman**, **Insomnia**, **API Dog** ou similares para realizar requisições HTTP.

- **Login**  
  Envie uma requisição `POST` para `/api/v1/authentication/login/` com os dados do usuário (usuário e senha) no corpo da requisição, você receberá um código no email cadastrado.

- **Validação de Token**  
  Após o login, verifique o código enviado por e-mail para confirmar e ativar a conta ou validar o token recebido.

- **Renovação de Token**  
  Envie uma requisição `POST` para `/api/v1/authentication/api/token/refresh/` com o **refresh token** no corpo da requisição para obter um novo token de acesso.

💡 Dica: Nos clientes API (Postman, API Dog), salve os tokens em variáveis de ambiente para facilitar testes sequenciais e automáticos.

---

### 📂 Arquivo Postman

Para facilitar os testes, disponibilizamos um arquivo **Postman** com todas as requisições pré-configuradas, incluindo exemplos dos corpos (body).  
Importe esse arquivo na sua ferramenta favorita (Postman, API Dog, Insomnia) para começar a testar rapidamente a API.

---

## ⚠️ Observações Importantes sobre Autenticação e Logout

- Os tokens JWT são enviados e armazenados via **cookies HTTP-only** para garantir maior segurança contra ataques XSS.
- Após a validação do código enviado por e-mail, todas as rotas protegidas passam a ser autenticadas utilizando esses cookies.
- O **access token** possui validade curta para proteger o sistema contra acessos não autorizados.
- O **refresh token** é utilizado para renovar o access token sem que o usuário precise fazer login novamente.
- No logout, os cookies contendo os tokens são removidos do cliente, porém os tokens em si **não são invalidados no servidor** e permanecem válidos até expirarem.
- A implementação de uma **blacklist para invalidação imediata** dos tokens não está presente nesta versão da API, mas é uma melhoria planejada.
- Este é apenas o início do projeto; funcionalidades adicionais, como controle de autorização, permissões específicas e testes automatizados, serão implementadas em breve.
  
---

## 📄 Licença

Este software é propriedade exclusiva da NexTech - Soluções em software.  
Todo o código-fonte, documentação e materiais relacionados são confidenciais e protegidos por leis de direitos autorais.  
Nenhuma parte deste software pode ser reproduzida, distribuída ou utilizada sem a autorização expressa e por escrito da NexTech - Soluções em software.  

Para mais informações ou solicitações de uso, entre em contato com a equipe responsável.


