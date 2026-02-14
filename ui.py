import sys
import threading
import requests
import json
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Try importing markdown for rich text
try:
    import markdown
except ImportError:
    markdown = None

# ==========================================
# OLLAMA BACKEND (Llama 3.1 Integration)
# ==========================================
class OllamaBackend:
    def __init__(self):
        self.history = []
        self.api_url = "http://localhost:11434/api/chat"
        self.model = "llama3.1"

    def stream_jarvis(self, prompt):
        """Streams response from Ollama Llama 3.1"""
        # 1. Append User Message to History
        self.history.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": True
        }

        full_response = ""
        try:
            # 2. Connect to Ollama
            with requests.post(self.api_url, json=payload, stream=True) as response:
                if response.status_code != 200:
                    yield f"**Error:** Ollama returned status {response.status_code}."
                    return

                # 3. Stream the chunks
                for line in response.iter_lines():
                    if line:
                        try:
                            json_response = json.loads(line)
                            if 'message' in json_response:
                                token = json_response['message']['content']
                                full_response += token
                                yield token
                        except json.JSONDecodeError:
                            continue
            
            # 4. Append AI Response to History (so it remembers next time)
            self.history.append({"role": "assistant", "content": full_response})

        except requests.exceptions.ConnectionError:
            yield "**System Failure:** Unable to connect to Neural Core (Ollama is not running at localhost:11434)."
        except Exception as e:
            yield f"**Critical Error:** {str(e)}"

    def reset_chat(self):
        self.history = []
        print("Memory Core Wiped.")

# Initialize the Backend
backend = OllamaBackend()

# ==========================================
# 3D CYBER BUTTON
# ==========================================
class CyberButton(QPushButton):
    def __init__(self, text, color="#00f3ff", parent=None):
        super().__init__(text, parent)
        self.color = color
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(50)
        
        self.default_style = f"""
            QPushButton {{
                background-color: rgba(0, 20, 30, 0.8);
                color: {color};
                border: 1px solid {color};
                border-bottom: 4px solid {color};
                border-radius: 4px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding-bottom: 2px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 243, 255, 0.15);
                border: 1px solid #fff;
                border-bottom: 4px solid #fff;
                color: #fff;
            }}
        """
        self.pressed_style = f"""
            QPushButton {{
                background-color: rgba(0, 243, 255, 0.2);
                border: 1px solid {color};
                border-bottom: 0px solid {color};
                border-radius: 4px;
                color: {color};
                margin-top: 4px;
            }}
        """
        self.setStyleSheet(self.default_style)
        
        self.glow = QGraphicsDropShadowEffect()
        self.glow.setBlurRadius(15)
        self.glow.setColor(QColor(color))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)

    def mousePressEvent(self, e):
        self.setStyleSheet(self.pressed_style)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.setStyleSheet(self.default_style)
        super().mouseReleaseEvent(e)

# ==========================================
# HOLOGRAPHIC BACKGROUND
# ==========================================
class TechFrame(QFrame):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Grid
        painter.setPen(QPen(QColor(0, 243, 255, 15), 1))
        grid_size = 40
        for x in range(0, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)
            
        # Corner Brackets
        painter.setPen(QPen(QColor(0, 243, 255, 180), 2))
        w, h = self.width(), self.height()
        bracket_len = 20
        
        painter.drawLine(0, 0, bracket_len, 0) # Top Left
        painter.drawLine(0, 0, 0, bracket_len)
        painter.drawLine(w, 0, w-bracket_len, 0) # Top Right
        painter.drawLine(w, 0, w, bracket_len)
        painter.drawLine(0, h, bracket_len, h) # Bottom Left
        painter.drawLine(0, h, 0, h-bracket_len)
        painter.drawLine(w, h, w-bracket_len, h) # Bottom Right
        painter.drawLine(w, h, w, h-bracket_len)
        
        super().paintEvent(event)

# ==========================================
# CHAT BUBBLES
# ==========================================
class MessageBubble(QFrame):
    def __init__(self, text, is_user=False):
        super().__init__()
        self.is_user = is_user
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        
        time_lbl = QLabel(QTime.currentTime().toString("HH:mm"))
        time_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; margin-bottom: 5px;")
        
        self.content = QLabel()
        self.content.setWordWrap(True)
        self.content.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.content.setOpenExternalLinks(True)
        
        # Initial Text Set
        self.update_text(text)
            
        if is_user:
            layout.addStretch()
            layout.addWidget(self.content)
            self.content.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d4, stop:1 #005a9e);
                color: white;
                padding: 12px 16px;
                border-radius: 12px;
                border-bottom-right-radius: 2px;
                border: 1px solid rgba(255,255,255,0.2);
            """)
        else:
            layout.addWidget(self.content)
            layout.addWidget(time_lbl, alignment=Qt.AlignBottom)
            layout.addStretch()
            self.content.setStyleSheet("""
                background: rgba(5, 15, 25, 0.85);
                color: #e0f2fe;
                padding: 12px 16px;
                border-radius: 12px;
                border-bottom-left-radius: 2px;
                border: 1px solid rgba(0, 243, 255, 0.3);
                border-left: 3px solid #00f3ff;
            """)

        self.content.setMaximumWidth(650)
        self.setGraphicsEffect(self.get_glow(is_user))

    def update_text(self, text):
        if markdown and not self.is_user:
            html = markdown.markdown(text, extensions=['fenced_code'])
            style = """
            <style>
                code { background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 3px; }
                pre { background: rgba(0,0,0,0.5); padding: 10px; border: 1px solid #00f3ff; border-radius: 5px;}
                p { color: #e0f2fe; margin: 0; }
                strong { color: #00f3ff; }
                ul, ol { margin-left: 15px; }
            </style>
            """
            self.content.setText(style + html)
        else:
            self.content.setText(text)

    def get_glow(self, is_user):
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(0, 120, 212, 100) if is_user else QColor(0, 243, 255, 60))
        glow.setOffset(0, 4)
        return glow

# ==========================================
# MAIN CLASS (Renamed to JarvisUI)
# ==========================================
class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.moving = False
        self.offset = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1200, 850)
        
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.frame = TechFrame()
        self.frame.setStyleSheet("""
            TechFrame {
                background: rgba(5, 8, 15, 0.95);
                border: 1px solid rgba(0, 243, 255, 0.3);
                border-radius: 8px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 243, 255, 150))
        shadow.setOffset(0, 0)
        self.frame.setGraphicsEffect(shadow)
        
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        
        self.layout.addWidget(self.frame)
        
        self.init_header()
        self.init_chat()
        self.init_footer()

    def init_header(self):
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet("background: rgba(0,0,0,0.2); border-bottom: 1px solid rgba(0,243,255,0.2);")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(15, 0, 15, 0)
        
        icon = QLabel("●")
        icon.setStyleSheet("color: #00ff00; font-size: 10px;")
        title = QLabel(" JARVIS // LLAMA 3.1 CORE")
        title.setStyleSheet("color: #00f3ff; font-weight: bold; letter-spacing: 2px; font-size: 12px;")
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("background:none; color: #555; border:none; font-weight:bold;")
        btn_close.setCursor(Qt.PointingHandCursor)
        
        h_layout.addWidget(icon)
        h_layout.addWidget(title)
        h_layout.addStretch()
        h_layout.addWidget(btn_close)
        
        self.frame_layout.addWidget(header)
        header.mousePressEvent = self.header_press
        header.mouseMoveEvent = self.header_move
        header.mouseReleaseEvent = self.header_release

    def init_chat(self):
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.scroll.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical { background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: rgba(0,243,255,0.2); border-radius: 3px; }
            QScrollBar::handle:vertical:hover { background: #00f3ff; }
        """)
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        self.chat_layout = QVBoxLayout(container)
        self.chat_layout.addStretch()
        
        self.scroll.setWidget(container)
        self.frame_layout.addWidget(self.scroll)

    def init_footer(self):
        footer = QFrame()
        footer.setFixedHeight(120)
        footer.setStyleSheet("background: rgba(0, 15, 25, 0.6); border-top: 1px solid rgba(0, 243, 255, 0.3);")
        f_layout = QVBoxLayout(footer)
        f_layout.setContentsMargins(20, 15, 20, 15)
        
        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("ENTER COMMAND SEQUENCE...")
        self.input.returnPressed.connect(self.send)
        self.input.setStyleSheet("""
            QLineEdit {
                background: rgba(0,0,0,0.5);
                border: 1px solid rgba(0,243,255,0.3);
                border-radius: 4px;
                color: #00f3ff;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #00f3ff; }
        """)
        
        self.btn_send = CyberButton("EXECUTE", color="#00f3ff")
        self.btn_send.setFixedWidth(120)
        self.btn_send.clicked.connect(self.send)
        
        self.btn_clear = CyberButton("WIPE", color="#ff3366")
        self.btn_clear.setFixedWidth(80)
        self.btn_clear.clicked.connect(self.reset)

        input_row.addWidget(self.input)
        input_row.addSpacing(10)
        input_row.addWidget(self.btn_send)
        input_row.addWidget(self.btn_clear)
        f_layout.addLayout(input_row)
        
        status_row = QHBoxLayout()
        labels = ["SYS: ONLINE", "LLM: LLAMA-3.1", "NET: LOCALHOST", "SECURE"]
        for txt in labels:
            lbl = QLabel(txt)
            lbl.setStyleSheet("color: rgba(0,243,255,0.5); font-size: 10px; font-family: 'Arial';")
            status_row.addWidget(lbl)
        status_row.addStretch()
        f_layout.addLayout(status_row)
        self.frame_layout.addWidget(footer)

    def send(self):
        text = self.input.text().strip()
        if not text: return
        self.input.clear()
        
        self.add_bubble(MessageBubble(text, is_user=True))
        
        self.current_ai_msg = MessageBubble("Processing...", is_user=False)
        self.add_bubble(self.current_ai_msg)
        self.current_ai_text = ""
        
        self.worker = StreamThread(text)
        self.worker.token_signal.connect(self.update_ai)
        self.worker.start()
        
    def update_ai(self, token):
        self.current_ai_text += token
        self.current_ai_msg.update_text(self.current_ai_text)
        QTimer.singleShot(10, self.scroll_to_bottom)
            
    def add_bubble(self, widget):
        self.chat_layout.addWidget(widget)
        QTimer.singleShot(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def reset(self):
        backend.reset_chat()
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.add_bubble(MessageBubble("**SYSTEM RESET COMPLETE**", is_user=False))

    # Drag Logic
    def header_press(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.globalPosition().toPoint() - self.pos()
    def header_move(self, event):
        if self.moving:
            self.move(event.globalPosition().toPoint() - self.offset)
    def header_release(self, event):
        self.moving = False

# ==========================================
# THREAD
# ==========================================
class StreamThread(QThread):
    token_signal = Signal(str)
    def __init__(self, text):
        super().__init__()
        self.text = text
    def run(self):
        for token in backend.stream_jarvis(self.text):
            self.token_signal.emit(token)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisUI()
    window.show()
    sys.exit(app.exec())