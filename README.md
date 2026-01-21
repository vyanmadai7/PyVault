# PyVault

A  Python project that demonstrates how real password managers handle authentication logic.

## What it does
- Creates a vault.json file automatically
- Stores a bcrypt hashed master password
- Verifies master password before any action
- Saves account credentials locally
- Provides CLI menu for operations

## Learn before making this
- File I/O with JSON
- Password hashing with bcrypt
- Secure input handling
- Basic authentication flow

## Installation
pip install bcrypt

## Run
python main.py

## Roadmap
- Encrypt stored credentials (Fernet / AES)
- Password generator
- Export / import vault
