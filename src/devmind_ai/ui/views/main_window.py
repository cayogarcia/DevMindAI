from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QFrame, QPushButton, QLabel, QTextEdit, QSplitter, QFileDialog)
from PySide6.QtCore import Qt
from devmind_ai.ui.views.styles import MAIN_STYLE
from devmind_ai.services.gemini import GeminiService

class DevMindMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevMind AI")
        self.resize(1024, 680)
        
        self.setStyleSheet(MAIN_STYLE)
        self.has_active_session_in_sidebar = False
        
        # Inicializa o serviço do Gemini corrigido
        self.ai_service = GeminiService()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        sidebar = self._create_sidebar()
        chat_area = self._create_chat_area()
        
        splitter.addWidget(sidebar)
        splitter.addWidget(chat_area)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        main_layout.addWidget(splitter)

    def _create_sidebar(self):
        """Cria a barra lateral esquerda com navegação, novo chat e histórico"""
        frame = QFrame()
        frame.setObjectName("sidebar")
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        title = QLabel("🧠 DevMind AI")
        title.setObjectName("sidebar_title")
        layout.addWidget(title)
        
        # Botão para criar nova conversa limpa
        self.btn_new_chat = QPushButton("➕ Novo Chat")
        self.btn_new_chat.setObjectName("sidebar_btn")
        self.btn_new_chat.setStyleSheet("background-color: #2a2a30; color: #ffffff; font-weight: bold; margin-bottom: 10px;")
        self.btn_new_chat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_chat.clicked.connect(self._clear_to_new_chat)
        layout.addWidget(self.btn_new_chat)
        
        btn_chat = QPushButton("💬 Chat Principal")
        btn_chat.setObjectName("sidebar_btn")
        btn_chat.setCheckable(True)
        btn_chat.setChecked(True)
        
        btn_rag = QPushButton("📂 Arquivos e Contexto")
        btn_rag.setObjectName("sidebar_btn")
        btn_rag.setCheckable(True)
        
        layout.addWidget(btn_chat)
        layout.addWidget(btn_rag)
        
        history_title = QLabel("🕒 Conversas Recentes")
        history_title.setStyleSheet("color: #71717a; font-size: 11px; font-weight: bold; margin-top: 20px; padding-left: 10px;")
        layout.addWidget(history_title)
        
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(4)
        layout.addLayout(self.history_layout)
        
        layout.addStretch()
        return frame

    def _create_chat_area(self):
        """Cria a área de conversação centralizada"""
        frame = QFrame()
        frame.setObjectName("chat_container")
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.chat_history = QTextEdit()
        self.chat_history.setObjectName("chat_history")
        self.chat_history.setReadOnly(True)
        self.chat_history.setHtml(
            "<p style='color: #71717a;'><i>Bem-vindo ao DevMind AI! Como posso ajudar no seu código hoje?</i></p>"
        )
        layout.addWidget(self.chat_history)
        
        input_frame = QFrame()
        input_frame.setObjectName("input_container")
        input_frame.setMaximumHeight(80)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 5, 10, 5)
        
        self.attach_btn = QPushButton("📎")
        self.attach_btn.setObjectName("attach_btn")
        self.attach_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.attach_btn.setToolTip("Anexar arquivo de código ou contexto")
        self.attach_btn.clicked.connect(self._open_file_dialog)
        
        self.message_input = QTextEdit()
        self.message_input.setObjectName("message_input")
        self.message_input.setPlaceholderText("Pergunte algo sobre o projeto ou cole um log de erro...")
        self.message_input.installEventFilter(self)
        
        self.send_btn = QPushButton("Enviar")
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self._send_message)
        
        input_layout.addWidget(self.attach_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        
        layout.addWidget(input_frame)
        return frame

    def _add_history_item(self, title_text):
        """Injeta um registro de histórico composto por Seleção + Lixeira"""
        item_widget = QWidget()
        item_widget.setObjectName("history_item_widget")
        
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(4, 2, 4, 2)
        item_layout.setSpacing(0)
        
        clean_title = title_text.replace("\n", " ")
        
        select_btn = QPushButton(f"📄 {clean_title}")
        select_btn.setObjectName("history_select_btn")
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_btn.clicked.connect(lambda: self._select_history_item(clean_title))
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setObjectName("history_delete_btn")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setToolTip("Excluir esta conversa")
        delete_btn.clicked.connect(lambda: self._delete_history_item(item_widget))
        
        item_layout.addWidget(select_btn, stretch=1)
        item_layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        self.history_layout.addWidget(item_widget)

    def _select_history_item(self, title):
        """Simula a troca de contexto ao clicar no registro de histórico"""
        self.chat_history.setHtml(
            f"<p style='color: #71717a;'><i>[Histórico] Carregada a conversa: <b>{title}</b></i></p>"
        )

    def _delete_history_item(self, widget):
        """Remove o registro da barra lateral e restaura a tela inicial do chat"""
        widget.deleteLater()
        self.history_layout.removeWidget(widget)
        self._clear_to_new_chat()

    def _clear_to_new_chat(self):
        """Reseta o painel de mensagens e permite abrir uma nova sessão"""
        self.has_active_session_in_sidebar = False
        self.ai_service.reset_chat()
        self.chat_history.setHtml(
            "<p style='color: #71717a;'><i>Iniciando um novo chat limpo. Como posso ajudar no seu código?</i></p>"
        )
        self.message_input.clear()

    def _open_file_dialog(self):
        """Abre a caixa de diálogo nativa do sistema para anexar arquivos"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo de Contexto", "", "Todos os Arquivos (*.*)"
        )
        if file_path:
            filename = file_path.split("/")[-1]
            self.chat_history.append(
                f"<p style='color: #3498db; margin: 5px 0;'>📎 <b>Arquivo anexado:</b> {filename}</p>"
            )

    def _send_message(self):
        """Captura o texto digitado e aciona o fluxo dinâmico conectado ao Gemini"""
        text = self.message_input.toPlainText().strip()
        
        if not text:
            return
            
        if not self.has_active_session_in_sidebar:
            session_title = text if len(text) < 18 else f"{text[:15]}..."
            self._add_history_item(session_title)
            self.has_active_session_in_sidebar = True
            
        formatted_user_text = text.replace("\n", "<br/>")
        user_html = f"<p style='margin: 15px 0;'><b>Você:</b><br/>{formatted_user_text}</p>"
        self.chat_history.append(user_html)
        self.message_input.clear()
        
        ai_html_response = self.ai_service.send_message(text)
        
        ai_html = f"<p style='color: #ffffff; margin: 15px 0;'><b>DevMind AI:</b><br/>{ai_html_response}</p>"
        self.chat_history.append(ai_html)

    def eventFilter(self, obj, event):
        """Intercepta as teclas pressionadas no campo de texto"""
        from PySide6.QtGui import QKeyEvent
        from PySide6.QtCore import QEvent
        
        if obj is self.message_input and event.type() == QEvent.Type.KeyPress:
            key_event = QKeyEvent(event)
            if key_event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if key_event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    self._send_message()
                    return True
        return super().eventFilter(obj, event)