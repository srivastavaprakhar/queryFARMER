"""
Configuration file for QueryFARMER Translation Service
Set environment variables to configure the service
"""

import os
from typing import Optional

# Translation Provider Configuration
TRANSLATION_PROVIDER = os.getenv("TRANSLATION_PROVIDER", "mock")  # mock, google, deepl, local
TRANSLATION_API_KEY = os.getenv("TRANSLATION_API_KEY", "")

# Service Configuration
HOST = os.getenv("TRANSLATION_HOST", "127.0.0.1")
PORT = int(os.getenv("TRANSLATION_PORT", "8001"))
DEBUG = os.getenv("TRANSLATION_DEBUG", "false").lower() == "true"

# Cache Configuration
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "86400"))  # 24 hours in seconds
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "10000"))  # Maximum cache entries

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "100"))

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi", 
    "gu": "Gujarati",
    "mr": "Marathi",
    "bn": "Bengali"
}

# Language Pairs (which languages can translate to which)
LANGUAGE_PAIRS = {
    "hi": ["en"],
    "gu": ["en"], 
    "mr": ["en"],
    "bn": ["en"],
    "en": ["hi", "gu", "mr", "bn"]
}

# Mock Translation Data (for testing without API keys)
MOCK_TRANSLATIONS = {
    "hi": {
        "en": {
            "नमस्ते": "Hello",
            "कैसे": "How",
            "हैं": "are",
            "आप": "you",
            "मैं": "I",
            "हूं": "am",
            "किसान": "farmer",
            "फसल": "crop",
            "कीट": "pest",
            "रोग": "disease",
            "मेरी": "my",
            "गेहूं": "wheat",
            "में": "in",
            "पीले": "yellow",
            "रंग": "color",
            "के": "of",
            "धब्बे": "spots",
            "दिख": "showing",
            "रहे": "appearing",
            "क्या": "what",
            "यह": "this",
            "रोग": "disease"
        }
    },
    "gu": {
        "en": {
            "નમસ્તે": "Hello",
            "કેમ": "How",
            "છો": "are",
            "તમે": "you",
            "હું": "I",
            "છું": "am",
            "ખેડૂત": "farmer",
            "પાક": "crop",
            "કીટક": "pest",
            "રોગ": "disease"
        }
    },
    "mr": {
        "en": {
            "नमस्कार": "Hello",
            "कसे": "How",
            "आहात": "are",
            "तुम्ही": "you",
            "मी": "I",
            "आहो": "am",
            "शेतकरी": "farmer",
            "पीक": "crop",
            "कीटक": "pest",
            "रोग": "disease"
        }
    },
    "bn": {
        "en": {
            "নমস্কার": "Hello",
            "কেমন": "How",
            "আছেন": "are",
            "আপনি": "you",
            "আমি": "I",
            "আছি": "am",
            "কৃষক": "farmer",
            "ফসল": "crop",
            "কীটপতঙ্গ": "pest",
            "রোগ": "disease"
        }
    }
}

def get_config_summary() -> dict:
    """Get a summary of current configuration"""
    return {
        "provider": TRANSLATION_PROVIDER,
        "host": HOST,
        "port": PORT,
        "debug": DEBUG,
        "cache_duration_hours": CACHE_DURATION // 3600,
        "max_cache_size": MAX_CACHE_SIZE,
        "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
        "api_key_configured": bool(TRANSLATION_API_KEY)
    }

if __name__ == "__main__":
    print("Translation Service Configuration:")
    print("=" * 40)
    for key, value in get_config_summary().items():
        print(f"{key}: {value}")

