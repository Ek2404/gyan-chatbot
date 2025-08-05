[README.md](https://github.com/user-attachments/files/21603442/README.md)
# G.Y.A.N. – Guiding Youth with Artificial Network

An AI-powered chatbot designed for **B.K. Birla Public School’s Creativity Conclave**, helping users with:
- Event queries (from `conclave_data.json`)
- School information (from `school_data.json`)
- General AI questions (via OpenRouter API)

## 🚀 Features
- 🎯 Dual-source answer system (JSON + AI)
- 🗣️ Voice input & output (TTS + STT)
- 📁 Clean Flask-based backend
- 🌐 Responsive frontend with chat UI

## 🛠️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/ekansh-garg/gyan-chatbot.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your environment variable:**
   ```bash
   # In .env or your system env
   OPENROUTER_API_KEY=your-api-key-here
   ```

4. **Run locally:**
   ```bash
   python app.py
   ```

## 🧩 Project Structure

```
├── static/              # CSS & JS files
├── templates/           # HTML file (index.html)
├── app.py               # Flask server
├── ai_response.py       # AI API handler
├── conclave_response.py # Answers from conclave_data.json
├── automation.py        # Answers from school_data.json
├── requirements.txt     # All Python dependencies
```

## 🧠 Tech Stack
- Python 3.11+
- Flask
- JavaScript (frontend interactivity)
- OpenRouter AI API

## 👨‍💻 Developer
Created with 💙 by **Ekansh Garg** – BK Birla Public School, Kalyan
