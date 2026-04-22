# 💬 AI Chatbot

A simple AI chatbot powered by the OpenAI API. Available as both a **command-line tool** and a **Streamlit web app**.

## Features

- Chat with OpenAI models (GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo)
- Conversation memory within a session
- Streaming responses (typewriter effect)
- Customizable system prompt (web app)
- Clear conversation history any time

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key (get one at https://platform.openai.com/api-keys):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## Run the Web App (Streamlit)

```bash
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Run the CLI Version

```bash
python chatbot.py
```

CLI commands:
- `/clear` — clear conversation history
- `/quit` or `/exit` — exit the chatbot

## Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, pick your repo, and set the main file to `streamlit_app.py`.
4. In **Advanced settings → Secrets**, add:
   ```
   OPENAI_API_KEY = "sk-..."
   ```
   *(or let users paste their own key in the sidebar)*
5. Click **Deploy**. Share the URL with your friends and interviewers!

## License

MIT
