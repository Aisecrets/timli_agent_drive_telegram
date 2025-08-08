# Timli – Leap Agent with Google Drive + Telegram

Tools to power an AI agent (Leap.new):
- Create client folders in **Google Drive** and store metadata as JSON
- Upload PDFs into client folders
- Generate simple offers/appointments (stored as JSON files)
- Send outbound **Telegram** messages

## ✅ Requirements

- **Google Service Account JSON** with **Drive API** enabled  
  Set env: `GOOGLE_SERVICE_ACCOUNT_JSON=/absolute/path/to/service_account.json`  
  (Share your Drive root folder with the service account email as **Editor**)  
- (Optional) Root Drive folder for all clients  
  Set env: `TIMLI_DRIVE_ROOT_FOLDER_ID=<drive_folder_id>`
- **Telegram Bot Token** (via @BotFather)  
  Set env: `TELEGRAM_BOT_TOKEN=<token>`

## 🔧 Key Tools

- `clients.create_client(name, email)` → makes client folder + `info.json`  
- `drive_tools.upload_pdf_from_base64(b64, client, filename)` → uploads a PDF (returns web link)  
- `offers.generate_offer(client, amount)` → writes `offers.json`  
- `appointments.create_appointment(date, client)` → writes `appointments.json`  
- `telegram.send_telegram_message(chat_id, text)` → outbound notification

## 🚀 Quick Start (GitHub)

```bash
# 1) Create an empty repo on GitHub: https://github.com/<YOU>/timli_agent_drive_telegram
git init
git remote add origin https://github.com/<YOU>/timli_agent_drive_telegram.git

# 2) Add files (unzip this package in the repo folder)
git add .
git commit -m "Initial commit - Timli Leap Agent (Drive + Telegram)"
git branch -M main
git push -u origin main
```

## 🧩 Leap.new Setup

1. Go to **https://leap.new** → *Create Agent*
2. Use your GitHub repo URL (e.g. `https://github.com/<YOU>/timli_agent_drive_telegram`)
3. **Role/Prompt** example:

> Je bent Timli, een AI‑assistent die klantenbeheer, documentbeheer, offertes en afspraken uitvoert. Gebruik de tools in `tools/`. Vraag ontbrekende info proactief. Bevestig acties met duidelijke feedback en Drive‑links waar mogelijk.

4. **Environment variables** (in Leap):
   - `GOOGLE_SERVICE_ACCOUNT_JSON=/mnt/data/service_account.json` *(upload your JSON or use secrets)*
   - `TIMLI_DRIVE_ROOT_FOLDER_ID=<optional-root-folder-id>`
   - `TELEGRAM_BOT_TOKEN=<telegram-bot-token>`

**Important:** share your Drive **root folder** with the service account **email** (Editor).

## 💬 Telegram – Outbound

- Create a bot via **@BotFather**
- Set `TELEGRAM_BOT_TOKEN`  
- Use `send_telegram_message(chat_id, text)` to notify your user

**Inbound** (user → Timli): use **Make/Zapier/custom webhook** to call your Leap Agent, then send the response back to Telegram.

## 🧪 Local sanity check

```bash
python - << 'PY'
import importlib
mods = [
  'tools.clients','tools.drive_api','tools.drive_tools',
  'tools.offers','tools.appointments','tools.telegram','tools.inbox'
]
for m in mods:
    importlib.import_module(m)
print('✅ All imports ok')
PY
```

## 🛠 GitHub Actions (CI)

A small workflow to ensure imports work on each push:

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install
        run: pip install -r requirements.txt
      - name: Import smoke test
        run: |
          python - << 'PY'
          import importlib
          mods = [
            'tools.clients','tools.drive_api','tools.drive_tools',
            'tools.offers','tools.appointments','tools.telegram','tools.inbox'
          ]
          for m in mods:
              importlib.import_module(m)
          print('✅ All imports ok')
          PY
```

## 🧭 Tips
- Keep tools **pure** (clear params, string outputs).
- Let the agent **ask for missing info** (email, date, etc.).
- Use Drive as a lightweight “database” with JSON files per client folder.
