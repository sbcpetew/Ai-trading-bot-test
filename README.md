# AlphaFive

This repository contains a work-in-progress implementation of the AlphaFive trading system as described in the specification. The goal is to build an autonomous futures trading bot with strict risk controls.

This project currently provides a minimal skeleton including CLI entry points and a simple web-based interface built with Flask.

## Running the Web UI

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the interface and open `http://localhost:8000` in a browser:
   ```bash
   python ui_app.py
   ```
3. Build a Windows executable:
   ```bash
   pyinstaller ui_app.spec
   ```
   The output `AITradingBot.exe` will appear in the `dist/` directory.
