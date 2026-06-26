# DevMind AI 🧠

O **DevMind AI** é um assistente de engenharia de software sênior, direto e de alta performance desenvolvido em Python com **PySide6**. Ele utiliza a API do Gemini (`gemini-2.5-flash`) para fornecer suporte especializado, conciso e focado em desenvolvimento de código para múltiplos ecossistemas.

---

## 🚀 Tecnologias e Ecossistemas Suportados

O assistente foi moldado para atuar com maestria nas seguintes stacks:
* 🐍 **Python**: Especialista no ecossistema PySide6, Django e FastAPI (rodando em Python 3.14+).
* ⚛️ **React.js & TypeScript**: Suporte completo a componentes, hooks e tipagem estrita.
* 🗄️ **Bancos de Dados SQL**: Otimização de queries, criação de índices e estruturas relacionais.

---

## 🛠️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
* Python 3.14+
* [Poetry](https://python-poetry.org/) (Gerenciador de dependências)

---

## 📦 Instalação e Execução

1. **Instale as dependências via Poetry:**
   ```powershell
   poetry install
Configure as Variáveis de Ambiente:
Crie um arquivo .env na raiz do projeto e adicione sua chave da API do Gemini:

Snippet de código
GEMINI_API_KEY=sua_chave_da_api_aqui
Execute a aplicação:

PowerShell
$env:PYTHONPATH="src"
poetry run python src/devmind_ai/main.py
🪟 Atalho de Inicialização Rápida (Windows)
Para rodar a aplicação em segundo plano de forma 100%

VBScript
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\Projects\DevMindAI"
WshShell.Run "cmd /c set PYTHONPATH=src && C:\Users\cayog\AppData\Roaming\Python\Python314\Scripts\poetry.exe run python src/devmind_ai/main.py", 0, False