import sys
from PySide6.QtWidgets import QApplication
from devmind_ai.config.settings import settings
from devmind_ai.ui.views.main_window import DevMindMainWindow

def main():
    app = QApplication(sys.argv)
    
    if not settings.GEMINI_API_KEY:
        print("\n[AVISO]: GEMINI_API_KEY não foi encontrada no arquivo .env!")
        
    window = DevMindMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()