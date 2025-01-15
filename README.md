# Ollama Writing Tools

<div align="center">

![Ollama Writing Tools Logo](./icon.png)

An AI-powered Windows application that provides writing assistance through Ollama AI. This tool activates when you select text, offering various writing enhancement features such as proofreading.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitmichaelqiu/OllamaWritingTools/blob/main/LICENSE)
[![Powered by Ollama](https://img.shields.io/badge/Powered%20by-Ollama-orange)](https://ollama.com)
[![Release](https://img.shields.io/github/v/release/gitmichaelqiu/OllamaWritingTools?color=green)](https://github.com/gitmichaelqiu/OllamaWritingTools/releases/)

</div>

## 🎯 Overview

Ollama Writing Tools enhances your writing experience by providing real-time assistance powered by advanced AI models. It simplifies the process of improving your text with just a few clicks.

## ✨ Key Features

- **System Tray Integration**: Seamlessly runs in the background
- **Text Selection Monitoring**: Activates upon text selection
- **Proofreading Functionality**: Offers grammar and spelling corrections
- **Configurable API Settings**: Customize your Ollama API URL and model selection

## 🚀 Quick Start

### Prerequisites

1. Install [Ollama](https://ollama.com) and ensure it is running on `127.0.0.1:11434`
2. Pull at least one Ollama model (e.g., qwen2.5:3b):
   ```bash
   ollama pull qwen2.5:3b
   ```

### Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage Guide

### Basic Operation

1. Run the application:
   ```bash
   python main.py
   ```
2. The application will run in the system tray (look for the icon in the bottom right corner of your screen).
3. To use the writing tools:
   - Select any text in any application
   - Press Ctrl+C to copy the text
   - A small button will appear near your cursor
   - Click the button to open the writing tools interface
   - Choose the desired writing enhancement option (currently supports proofreading)

### Configuration

Right-click the system tray icon and select "Settings" to:
- Configure the Ollama API URL (default: 127.0.0.1:11434)
- Select which Ollama model to use
- Refresh the list of available models

## ⚠️ Note

Make sure to add an `icon.png` file in the same directory as `main.py` for the system tray icon.
