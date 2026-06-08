# 📡 WiFi da Cidade

Site para compartilhar senhas WiFi com amigos, com login protegido por senha.

## Estrutura do projeto

```
wifimap/
├── main.py              # Backend FastAPI
├── requirements.txt     # Dependências Python
├── Procfile             # Comando de start (Render)
├── templates/
│   ├── login.html       # Página de login
│   ├── redes.html       # Página com as redes (amigos)
│   └── admin.html       # Painel admin
└── data/
    └── redes.json       # Redes salvas (criado automaticamente)
```

---

## 🚀 Como subir no Render (grátis)

### 1. Crie uma conta no GitHub e suba o projeto
- Acesse https://github.com e crie uma conta
- Crie um repositório novo (ex: `wifimap`)
- Faça upload de todos os arquivos desta pasta

### 2. Crie uma conta no Render
- Acesse https://render.com e crie uma conta gratuita

### 3. Crie um novo Web Service
- Clique em **New → Web Service**
- Conecte seu repositório do GitHub
- Configure assim:
  - **Runtime:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4. Configure as senhas (variáveis de ambiente)
No painel do Render, vá em **Environment** e adicione:

| Variável       | Valor          | Para quê?                        |
|----------------|----------------|----------------------------------|
| `SENHA_ACESSO` | (sua senha)    | Senha que você passa para amigos |
| `SENHA_ADMIN`  | (senha secreta)| Senha para gerenciar redes       |

> ⚠️ Nunca use as senhas padrão do código em produção!

### 5. Deploy!
- Clique em **Create Web Service**
- Aguarde alguns minutos
- Seu site estará no ar em `https://seu-app.onrender.com`

---

## 🔑 Como usar

| Quem        | Senha           | O que pode fazer                  |
|-------------|-----------------|-----------------------------------|
| Amigos      | `SENHA_ACESSO`  | Ver e copiar senhas WiFi          |
| Admin (você)| `SENHA_ADMIN`   | Adicionar e remover redes         |

---

## ⚠️ Observação sobre dados

O Render no plano gratuito **não persiste arquivos** entre deploys. Isso significa que as redes cadastradas podem ser apagadas quando o serviço reiniciar.

**Solução recomendada:** Use o [Supabase](https://supabase.com) (PostgreSQL gratuito) para salvar os dados de forma permanente. Avise se quiser que eu adapte o código para isso!
