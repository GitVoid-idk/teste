from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic
import json
import os
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ─── CONFIGURAÇÕES ───────────────────────────────────────────────
# Senha de acesso ao site (compartilhe com seus amigos)
SENHA_ACESSO = os.getenv("SENHA_ACESSO", "amigos2024")

# Senha de admin para gerenciar as redes wifi
SENHA_ADMIN = os.getenv("SENHA_ADMIN", "admin123")

# Arquivo onde as redes ficam salvas
DATA_FILE = Path("data/redes.json")
DATA_FILE.parent.mkdir(exist_ok=True)

# ─── HELPERS ─────────────────────────────────────────────────────
def carregar_redes():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def salvar_redes(redes):
    with open(DATA_FILE, "w") as f:
        json.dump(redes, f, ensure_ascii=False, indent=2)

def get_sessao(request: Request):
    return request.cookies.get("sessao")

# ─── ROTAS ───────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    sessao = get_sessao(request)
    if sessao == "amigo":
        return RedirectResponse("/redes")
    if sessao == "admin":
        return RedirectResponse("/admin")
    return templates.TemplateResponse("login.html", {"request": request, "erro": None})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, senha: str = Form(...)):
    if senha == SENHA_ADMIN:
        resp = RedirectResponse("/admin", status_code=302)
        resp.set_cookie("sessao", "admin")
        return resp
    elif senha == SENHA_ACESSO:
        resp = RedirectResponse("/redes", status_code=302)
        resp.set_cookie("sessao", "amigo")
        return resp
    return templates.TemplateResponse("login.html", {"request": request, "erro": "Senha incorreta. Tenta de novo!"})

@app.get("/logout")
async def logout():
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("sessao")
    return resp

@app.get("/redes", response_class=HTMLResponse)
async def redes(request: Request):
    sessao = get_sessao(request)
    if sessao not in ("amigo", "admin"):
        return RedirectResponse("/")
    redes = carregar_redes()
    return templates.TemplateResponse("redes.html", {"request": request, "redes": redes, "admin": sessao == "admin"})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    if get_sessao(request) != "admin":
        return RedirectResponse("/")
    redes = carregar_redes()
    return templates.TemplateResponse("admin.html", {"request": request, "redes": redes})

@app.post("/admin/adicionar")
async def adicionar_rede(
    request: Request,
    local: str = Form(...),
    nome_rede: str = Form(...),
    senha: str = Form(...),
    descricao: str = Form("")
):
    if get_sessao(request) != "admin":
        raise HTTPException(status_code=403)
    redes = carregar_redes()
    redes.append({
        "id": len(redes) + 1,
        "local": local,
        "nome_rede": nome_rede,
        "senha": senha,
        "descricao": descricao
    })
    salvar_redes(redes)
    return RedirectResponse("/admin", status_code=302)

@app.post("/admin/remover/{rede_id}")
async def remover_rede(request: Request, rede_id: int):
    if get_sessao(request) != "admin":
        raise HTTPException(status_code=403)
    redes = carregar_redes()
    redes = [r for r in redes if r["id"] != rede_id]
    salvar_redes(redes)
    return RedirectResponse("/admin", status_code=302)
