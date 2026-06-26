MAIN_STYLE = """
QMainWindow {
    background-color: #1e1e24;
}

QFrame#sidebar {
    background-color: #141416;
    border-right: 1px solid #2a2a30;
    min-width: 220px;
    max-width: 280px;
}

QLabel#sidebar_title {
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    padding: 15px 10px;
}

QPushButton#sidebar_btn {
    color: #a0a0aa;
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 10px;
    text-align: left;
    font-size: 13px;
}

QPushButton#sidebar_btn:hover {
    background-color: #2a2a30;
    color: #ffffff;
}

QPushButton#sidebar_btn:checked {
    background-color: #2ecc71;
    color: #141416;
    font-weight: bold;
}

QWidget#history_item_widget {
    background-color: transparent;
    border-radius: 6px;
}
QWidget#history_item_widget:hover {
    background-color: #2a2a30;
}

QPushButton#history_select_btn {
    color: #e4e4e7;
    background-color: transparent;
    border: none;
    text-align: left;
    font-size: 12px;
    padding: 6px;
}

QPushButton#history_delete_btn {
    background-color: transparent;
    border: none;
    color: #71717a;
    font-size: 12px;
    padding: 6px;
}
QPushButton#history_delete_btn:hover {
    color: #ef4444;
}

QFrame#chat_container {
    background-color: #1e1e24;
}

QTextEdit#chat_history {
    background-color: #1e1e24;
    border: none;
    color: #e4e4e7;
    font-size: 14px;
    padding: 10px;
}

QFrame#input_container {
    background-color: #141416;
    border: 1px solid #2a2a30;
    border-radius: 8px;
    padding: 4px;
}

QTextEdit#message_input {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 14px;
}

QPushButton#attach_btn {
    background-color: transparent;
    color: #a0a0aa;
    border: none;
    border-radius: 6px;
    padding: 8px;
    font-size: 16px;
}
QPushButton#attach_btn:hover {
    background-color: #2a2a30;
    color: #ffffff;
}

QPushButton#send_btn {
    background-color: #2ecc71;
    color: #141416;
    border: none;
    border-radius: 6px;
    padding: 8px 15px;
    font-weight: bold;
}
QPushButton#send_btn:hover {
    background-color: #27ae60;
}
"""