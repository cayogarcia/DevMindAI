import re
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from devmind_ai.config.settings import settings

class GeminiService:
    def __init__(self):
        """Inicializa as configurações e o cliente oficial da API Gemini."""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada no arquivo .env!")
        
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"
        self.chat_session = None
        self.reset_chat()

    def reset_chat(self):
        system_instruction = (
            "1. Você é o DevMind AI, um assistente especialista e direto em engenharia de software.\n"
            "2. Você é especialista em Python (ecossistema PySide6, Django, FastAPI), React.js, TypeScript e bancos de dados SQL.\n"
            "3. Responda APENAS sobre o contexto solicitado de forma concisa e objetiva.\n"
            "4. O projeto utiliza PySide6 e Python 3.14+. NUNCA mencione ou use PyQt5 ou PyQt6.\n"
            "5. Evite explicações longas e comentários redundantes no código.\n"
            "6. Quando enviar blocos de código, use sempre a marcação padrão de Markdown (```python, ```tsx, ```sql, etc.)."
        )
        
        self.chat_session = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
            )
        )

    def send_message(self, message: str) -> str:
        """
        Envia a mensagem do usuário para o Gemini com mecanismo de re-tentativas automáticas 
        (Exponential Backoff) para evitar falhas temporárias como erros 503 (Serviço Indisponível).
        """
        max_retries = 5
        backoff_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                response = self.chat_session.send_message(message)
                return self.format_markdown_to_html(response.text)
            except APIError as e:
                if e.code in (503, 429) and attempt < max_retries - 1:
                    time.sleep(backoff_delay)
                    backoff_delay *= 2 
                    continue
                
                return (
                    f'<div style="border: 1px solid #ef4444; background-color: #2a1414; '
                    f'padding: 12px; border-radius: 6px; color: #fca5a5; margin: 10px 0;">'
                    f'⚠️ <b>O servidor do Gemini está temporariamente indisponível ou sobrecarregado (Erro {e.code}).</b><br/>'
                    f'<small>O DevMind AI tentou re-estabelecer a conexão {max_retries} vezes sem sucesso. '
                    f'Por favor, aguarde alguns segundos e clique em Enviar novamente.</small></div>'
                )
            except Exception as e:
                return f'<span style="color: #ff5555;"><b>Erro inesperado:</b> {str(e)}</span>'

    def format_markdown_to_html(self, text: str) -> str:
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # 2. Regex para blocos de código (captura a linguagem opcional no grupo 1 e o código no grupo 2)
        code_block_pattern = r'```([a-zA-Z0-9_-]*)\s*\n(.*?)\s*```'
        
        def replace_code_block(match):
            code_content = match.group(2)
            formatted_code = code_content.replace('\n', '<br/>').replace(' ', '&nbsp;')
            return (
                f'<div style="background-color: #141416; border: 1px solid #2a2a30; '
                f'border-radius: 6px; padding: 12px; font-family: Consolas, Monaco, monospace; '
                f'color: #a6e22e; margin: 10px 0; line-height: 1.4;">{formatted_code}</div>'
            )
        
        text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)

        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

        text = re.sub(
            r'`(.*?)`', 
            r'<code style="background-color: #2a2a30; color: #f8f8f2; padding: 2px 4px; border-radius: 4px; font-family: Consolas, monospace;">\1</code>', 
            text
        )

        text = text.replace('\n', '<br/>')
        
        return text