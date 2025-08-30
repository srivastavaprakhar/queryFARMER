# 🌾 QueryFARMER - AI-Powered Multilingual Farming Assistant

> **Your intelligent farming companion that speaks your language** 🌱

QueryFARMER is an advanced AI-powered chatbot designed specifically for farmers, providing expert agricultural advice, disease identification, farming techniques, and equipment recommendations. Built with cutting-edge AI technology and featuring comprehensive multilingual support for Indian farmers.

## ✨ Features

### 🤖 **AI-Powered Farming Intelligence**
- **Expert Agricultural Advice**: Get personalized recommendations for crops, soil, and farming practices
- **Disease Identification**: Identify plant diseases and get treatment solutions
- **Farming Techniques**: Learn modern and traditional farming methods
- **Equipment Recommendations**: Get advice on farming tools and machinery
- **Weather-Aware Suggestions**: Context-aware farming recommendations

### 🌐 **Multilingual Support**
- **5 Indian Languages**: Hindi, Gujarati, Marathi, Bengali, and English
- **Natural Language Processing**: Understands farming terminology in local languages
- **Seamless Translation**: Real-time translation between languages
- **Cultural Context**: Farming advice tailored to regional practices

### 🏗️ **Advanced Architecture**
- **LLM Integration**: Powered by Mistral-7B and LlamaIndex
- **Vector Database**: FAISS-based semantic search for accurate responses
- **Microservices**: Translation service for language processing
- **Real-time Processing**: Fast response times for farming queries

### 🔐 **User Management**
- **Secure Authentication**: User registration and login system
- **Personalized Experience**: Save user preferences and farming history
- **Data Privacy**: Local data storage with encryption

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (for AI models)
- Windows/Linux/macOS

### Installation

1. **Clone the repository**
git clone https://github.com/yourusername/queryFARMER.git
cd queryFARMER

2. **Create virtual environment**
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

3. **Install dependencies**
# Main application
pip install -r requirements.txt

# Translation service
pip install -r translation_requirements.txt

4. **Start the services**
# Terminal 1: Main backend
python api_wrapper.py

# Terminal 2: Translation service
python start_translation_service.py

5. **Open the application**
```bash
# Open frontend/index.html in your browser
# Or start the main application
python main.py

## 🏗️ Architecture

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │ Translation      │    │   Backend       │
│   (Multilingual)│◄──►│   Service        │◄──►│   (AI Engine)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Localization  │    │   Language       │    │   Vector DB     │
│   (5 Languages) │    │   Processing     │    │   (FAISS)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘

## 🌐 Supported Languages

| Language | Code | Native Name | Status |
|----------|------|-------------|---------|
| English | `en` | English | ✅ Complete |
| Hindi | `hi` | हिंदी | ✅ Complete |
| Gujarati | `gu` | ગુજરાતી | ✅ Complete |
| Marathi | `mr` | मराठी | ✅ Complete |
| Bengali | `bn` | বাংলা | ✅ Complete |

## 📁 Project Structure

queryFARMER/
├── 📁 frontend/                 # Web interface
│   ├── index.html              # Main application
│   ├── style.css               # Styling
│   ├── script.js               # Frontend logic
│   └── 📁 locales/             # Language files
│       ├── en.json             # English
│       ├── hi.json             # Hindi
│       ├── gu.json             # Gujarati
│       ├── mr.json             # Marathi
│       └── bn.json             # Bengali
├── 📁 models/                   # AI models
│   └── 📁 Mistral/             # Mistral-7B model
├── 📁 database/                 # Farming knowledge base
│   ├── farming_categories.py    # Crop categories
│   ├── plant_diseases.py        # Disease database
│   ├── farming_techniques.py    # Techniques guide
│   └── farming_equipment.py     # Equipment info
├── 📁 auth/                     # User authentication
├── 📁 logs/                     # Application logs
├── api_wrapper.py               # API server
├── translation_service.py       # Translation microservice
├── main.py                      # Main application
└── requirements.txt             # Dependencies

**Made with ❤️ for Indian Farmers**

*QueryFARMER - Empowering farmers with AI, one question at a time* 🌱🚜
