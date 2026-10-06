# SentinelOT
AI-powered OT/ICS security alert triage copilot (Nebius x NVIDIA Global AI Hackathon).

## Setup
python -m venv .venv
# Windows: .venv\Scripts\activate   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # then fill in the keys
python smoke_test.py
