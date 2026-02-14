# JARVIS // Neural Interface 🤖✨

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![GUI](https://img.shields.io/badge/PySide6-Qt-green)
![AI](https://img.shields.io/badge/Ollama-Llama%203.1-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**A high-fidelity, sci-fi inspired desktop client for local Large Language Models.**

The **Jarvis Neural Interface** is a fully custom graphical user interface (GUI) built with **Python** and **PySide6**. It connects directly to a local **Ollama** instance (running Llama 3.1) to provide a private, offline AI assistant experience.

Unlike standard chatbots, this project focuses on **immersion**: featuring a frameless glassmorphism design, holographic HUD elements, real-time text streaming, and tactile 3D interactive buttons.

---

## 📸 Interface

*(Replace this line with a screenshot of your application running, e.g., `![Main UI](screenshots/jarvis_ui.png)`)*

---

## ✨ Key Features

* **🖥️ Holographic UI:** Custom-painted background grids, corner brackets, and semi-transparent "glass" frames for a true cyberpunk aesthetic.
* **🧠 Local Intelligence:** Powered by **Llama 3.1** via Ollama. Your data never leaves your machine.
* **⚡ Real-Time Streaming:** AI responses are streamed character-by-character with a typewriter effect, mimicking a retro-futuristic terminal.
* **🎨 Rich Text Support:** Full Markdown rendering for code blocks, bold text, and lists.
* **🖱️ Tactile 3D Buttons:** Custom `CyberButton` widgets that physically depress and glow when clicked.
* **🔧 Frameless Window:** A custom title bar allows for dragging and window management without standard OS borders.
* **📊 Live Status HUD:** Simulated system metrics (CPU, RAM, Network) for visual immersion.

---

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.10+**
2.  **Ollama** (Running locally)
    * Download from [ollama.com](https://ollama.com)
    * Pull the default model:
        ```bash
        ollama pull llama3.1
        ```

---

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/jarvis-neural-interface.git](https://github.com/yourusername/jarvis-neural-interface.git)
    cd jarvis-neural-interface
    ```

2.  **Install Python dependencies**
    ```bash
    pip install PySide6 requests markdown
    ```

3.  **Start Ollama**
    Ensure the Ollama server is running in the background (usually on `localhost:11434`).

---

## 🚀 Usage

Run the main application entry point:

```bash
python main.py
