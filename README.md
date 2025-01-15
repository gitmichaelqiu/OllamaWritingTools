# Ollama Writing Tools

<div align="center">

![Ollama Writing Tools Logo](resources/icon.png)

A Windows application that enhances your writing with AI-powered assistance through Ollama. Simply select text anywhere, and get instant writing improvements with a single click.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitmichaelqiu/OllamaWritingTools/blob/main/LICENSE)
[![Powered by Ollama](https://img.shields.io/badge/Powered%20by-Ollama-orange)](https://ollama.com)
[![Release](https://img.shields.io/github/v/release/gitmichaelqiu/OllamaWritingTools?color=green)](https://github.com/gitmichaelqiu/OllamaWritingTools/releases/)

</div>

## 🎯 Overview

Ollama Writing Tools is a lightweight Windows application that seamlessly integrates with your workflow to provide instant writing assistance. Using the power of Ollama's AI models, it helps improve your writing with just a few clicks.

## ✨ Key Features

- **Instant Access**: Select text anywhere and press Ctrl+C to activate
- **Smart UI**: Floating button appears near your cursor for quick access
- **System Integration**: 
  - Runs quietly in the system tray
  - Proper taskbar integration with application icon
  - Windows native look and feel
- **Writing Tools**:
  - Proofreading and grammar checking
  - Style improvements
  - More features coming soon
- **Customizable**:
  - Choose your preferred Ollama model
  - Configure API settings
  - Adjust font size

- **System Tray Integration**: Seamlessly runs in the background
- **Text Selection Monitoring**: Activates upon text selection
- **Customizable Writing Tools Options**: Configure in `functions.json`
- **Configurable API Settings**: Customize your Ollama API URL and model selection

## 🚀 Getting Started

### Prerequisites

1. **Ollama**: Install [Ollama](https://ollama.com) on your system
2. **AI Model**: Pull your preferred model (recommended: qwen2.5:3b)
=======
1. Install [Ollama](https://ollama.com)
2. Pull at least one Ollama model (e.g., qwen2.5:3b):
   ```bash
   ollama pull qwen2.5:3b
   ```

### Installation

#### Option 1: Download Executable (Recommended)
1. Download the latest release from the [releases page](https://github.com/gitmichaelqiu/OllamaWritingTools/releases)
2. Extract the zip file
3. Run `OllamaWritingTools.exe`

#### Option 2: Run from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/gitmichaelqiu/OllamaWritingTools.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## 📖 How to Use

1. **Start the App**: 
   - Run `OllamaWritingTools.exe`
   - Look for the icon in your system tray

2. **Using the Writing Tools**:
   - Select any text in any application
   - Press Ctrl+C
   - Click the floating button that appears
   - Choose your desired writing enhancement
   - View the improved text
   - Copy or replace the original text with one click

3. **Configuration**:
   - Right-click the system tray icon
   - Select "Settings"
   - Configure:
     - Ollama API URL (default: 127.0.0.1:11434)
     - AI Model selection
     - Font size
   - Click "Refresh Models" to update the model list

## 📁 Project Structure

```
OllamaWritingTools/
├── resources/
│   ├── icon.png          # Application icon
│   ├── functions.json    # Writing tool definitions
│   └── settings.json     # User settings
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Customize Writing Tools Grammar

```json
{
   "name": "NAME",
   "description": "DESCRIPTION",
   "prompt": "use placeholder {selection} for the selected text",
   "temperature": 0.2,
   "icon": "ADD AN EMOJI HERE"
},
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.
