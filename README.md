# 🎙️ Nova Mini: AI Voice & Text Assistant

A fully local, multi-modal AI assistant built from scratch using Python, Machine Learning, and OpenAI's Whisper. 

Unlike standard cloud-dependent voice assistants, **Siri Mini** processes NLP and speech-to-text entirely on your local machine. It features a custom glassmorphism UI built with Streamlit, seamless Voice and Text input tabs, and a hybrid backend that balances heavy NLP predictions with lightning-fast OS-level hardware triggers.

## ✨ Features
* **True Multi-Modal UX:** Seamlessly switch between Voice 🎤 and Text ⌨️ modes depending on your environment.
* **100% Local Processing:** Core NLP and Whisper transcription run locally. No cloud APIs, no subscription fees, total privacy.
* **Hybrid ML Architecture:** Uses a trained Scikit-Learn TF-IDF + MLP model for intent classification, paired with a keyword-override engine for instant hardware execution.
* **"Glass Box" AI:** The UI displays real-time, color-coded intent tags (e.g., `⚡ set_timer`, `⚡ open_maps`) so you can see the ML classification happen live.
* **OS Integration:** Uses background threading and subprocesses to set silent alarms, open local apps (Notepad, Calculator), and scrape Wikipedia without freezing the UI.

## 🛠️ Tech Stack
* **Language:** Python
* **Machine Learning:** Scikit-Learn (TF-IDF Vectorizer, MLP Classifier), joblib
* **Speech-to-Text:** OpenAI Whisper, `sounddevice`, `scipy`
* **Text-to-Speech:** `pyttsx3`
* **Frontend:** Streamlit with Custom CSS injection

📂 Project Structure
app.py: The main Streamlit frontend and UI configuration.

engine.py: Handles microphone hardware hooks, Whisper transcription, and Text-to-Speech.

actions.py: The hybrid execution engine (ML intents + hardware overrides).

model.py: Training script for the Scikit-Learn NLP intent classifier.
