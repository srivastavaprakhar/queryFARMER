"""
Translation Microservice for QueryFARMER
Handles translation between supported languages while preserving tokens and formatting.
"""

import os
import json
import logging
import hashlib
import time
from typing import Dict, List, Tuple, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="QueryFARMER Translation Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
TRANSLATION_PROVIDER = os.getenv("TRANSLATION_PROVIDER", "google")  # google, deepl, local
API_KEY = os.getenv("TRANSLATION_API_KEY", "")
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "86400"))  # 24 hours in seconds
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "10000"))  # Maximum cache entries

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati", 
    "mr": "Marathi",
    "bn": "Bengali"
}

# Translation cache
translation_cache = {}
cache_timestamps = {}

# Request/Response models
class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    preserve_tokens: bool = True

class TranslationResponse(BaseModel):
    translated_text: str
    confidence: float
    preserved_tokens: Dict[str, List[str]]
    source_lang: str
    target_lang: str
    success: bool

class HealthResponse(BaseModel):
    status: str
    supported_languages: Dict[str, str]
    cache_stats: Dict[str, int]

class TranslationService:
    """Handles translation logic with token preservation"""
    
    def __init__(self):
        self.provider = TRANSLATION_PROVIDER
        self.api_key = API_KEY
    
    def translate_text(self, text: str, source_lang: str, target_lang: str, preserve_tokens: bool = True) -> Tuple[str, float]:
        """
        Translate text while preserving tokens if requested
        """
        if source_lang == target_lang:
            return text, 1.0
        
        if preserve_tokens:
            # Extract and preserve tokens
            preserved_tokens = self._extract_tokens(text)
            # Replace tokens with placeholders
            processed_text = self._replace_tokens_with_placeholders(text, preserved_tokens)
            
            # Translate the processed text
            translated_text, confidence = self._call_translation_provider(processed_text, source_lang, target_lang)
            
            # Restore tokens in translated text
            final_text = self._restore_tokens(translated_text, preserved_tokens)
            
            return final_text, confidence
        else:
            # Direct translation without token preservation
            return self._call_translation_provider(text, source_lang, target_lang)
    
    def _extract_tokens(self, text: str) -> Dict[str, List[str]]:
        """Extract various types of tokens from text"""
        tokens = {
            "placeholders": [],  # {{variable_name}}
            "markdown": [],      # **bold**, *italic*
            "code": [],          # <code>...</code>
            "urls": [],          # http://...
            "numbers": []        # Preserve numbers
        }
        
        import re
        
        # Extract placeholders
        tokens["placeholders"] = re.findall(r'\{\{[^}]+\}\}', text)
        
        # Extract markdown
        tokens["markdown"] = re.findall(r'\*\*[^*]+\*\*|\*[^*]+\*', text)
        
        # Extract code blocks
        tokens["code"] = re.findall(r'<code>[^<]+</code>', text)
        
        # Extract URLs
        tokens["urls"] = re.findall(r'https?://[^\s]+', text)
        
        # Extract numbers (basic preservation)
        tokens["numbers"] = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        
        return tokens
    
    def _replace_tokens_with_placeholders(self, text: str, tokens: Dict[str, List[str]]) -> str:
        """Replace tokens with unique placeholders"""
        processed_text = text
        
        # Replace placeholders
        for i, token in enumerate(tokens["placeholders"]):
            processed_text = processed_text.replace(token, f"__PLACEHOLDER_{i}__")
        
        # Replace markdown
        for i, token in enumerate(tokens["markdown"]):
            processed_text = processed_text.replace(token, f"__MARKDOWN_{i}__")
        
        # Replace code blocks
        for i, token in enumerate(tokens["code"]):
            processed_text = processed_text.replace(token, f"__CODE_{i}__")
        
        # Replace URLs
        for i, token in enumerate(tokens["urls"]):
            processed_text = processed_text.replace(token, f"__URL_{i}__")
        
        # Replace numbers
        for i, token in enumerate(tokens["numbers"]):
            processed_text = processed_text.replace(token, f"__NUMBER_{i}__")
        
        return processed_text
    
    def _restore_tokens(self, translated_text: str, tokens: Dict[str, List[str]]) -> str:
        """Restore tokens in translated text"""
        restored_text = translated_text
        
        # Restore placeholders
        for i, token in enumerate(tokens["placeholders"]):
            restored_text = restored_text.replace(f"__PLACEHOLDER_{i}__", token)
        
        # Restore markdown
        for i, token in enumerate(tokens["markdown"]):
            restored_text = restored_text.replace(f"__MARKDOWN_{i}__", token)
        
        # Restore code blocks
        for i, token in enumerate(tokens["code"]):
            restored_text = restored_text.replace(f"__CODE_{i}__", token)
        
        # Restore URLs
        for i, token in enumerate(tokens["urls"]):
            restored_text = restored_text.replace(f"__URL_{i}__", token)
        
        # Restore numbers
        for i, token in enumerate(tokens["numbers"]):
            restored_text = restored_text.replace(f"__NUMBER_{i}__", token)
        
        return restored_text
    
    def _call_translation_provider(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Call the configured translation provider"""
        if self.provider == "google":
            return self._call_google_translate(text, source_lang, target_lang)
        elif self.provider == "deepl":
            return self._call_deepl_translate(text, source_lang, target_lang)
        elif self.provider == "local":
            return self._call_local_translate(text, source_lang, target_lang)
        else:
            # Fallback to mock translation for testing
            return self._mock_translate(text, source_lang, target_lang)
    
    def _call_google_translate(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Call Google Translate API"""
        try:
            if not self.api_key:
                raise Exception("Google Translate API key not configured")
            
            url = "https://translation.googleapis.com/language/translate/v2"
            params = {
                "q": text,
                "source": source_lang,
                "target": target_lang,
                "key": self.api_key
            }
            
            response = requests.post(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            translated_text = data["data"]["translations"][0]["translatedText"]
            confidence = data["data"]["translations"][0].get("detectedSourceConfidence", 0.9)
            
            return translated_text, confidence
            
        except Exception as e:
            logger.error(f"Google Translate error: {e}")
            return self._fallback_translation(text, source_lang, target_lang)
    
    def _call_deepl_translate(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Call DeepL API"""
        try:
            if not self.api_key:
                raise Exception("DeepL API key not configured")
            
            url = "https://api-free.deepl.com/v2/translate"
            headers = {"Authorization": f"DeepL-Auth-Key {self.api_key}"}
            data = {
                "text": [text],
                "source_lang": source_lang.upper(),
                "target_lang": target_lang.upper()
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            translated_text = data["translations"][0]["text"]
            
            return translated_text, 0.95
            
        except Exception as e:
            logger.error(f"DeepL error: {e}")
            return self._fallback_translation(text, source_lang, target_lang)
    
    def _call_local_translate(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Call local translation model (placeholder for future implementation)"""
        logger.info("Local translation not yet implemented")
        return self._fallback_translation(text, source_lang, target_lang)
    
    def _mock_translate(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Mock translation for testing purposes"""
        # Simple word replacement for demonstration
        mock_translations = {
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
            }
        }
        
        if source_lang in mock_translations and target_lang == "en":
            translated = text
            for word, translation in mock_translations[source_lang]["en"].items():
                translated = translated.replace(word, translation)
            return translated, 0.8
        
        return f"[{target_lang.upper()}] {text}", 0.5
    
    def _fallback_translation(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Fallback translation when provider fails"""
        return f"[{target_lang.upper()}] {text}", 0.3

# Initialize translation service
translation_service = TranslationService()

def get_cache_key(text: str, source_lang: str, target_lang: str) -> str:
    """Generate cache key for translation"""
    content = f"{text}:{source_lang}:{target_lang}"
    return hashlib.md5(content.encode()).hexdigest()

def cleanup_cache():
    """Remove expired cache entries and limit cache size"""
    current_time = time.time()
    expired_keys = []
    
    for key, timestamp in cache_timestamps.items():
        if current_time - timestamp > CACHE_DURATION:
            expired_keys.append(key)
    
    for key in expired_keys:
        del translation_cache[key]
        del cache_timestamps[key]
    
    # Limit cache size
    if len(translation_cache) > MAX_CACHE_SIZE:
        sorted_items = sorted(cache_timestamps.items(), key=lambda x: x[1])
        keys_to_remove = [key for key, _ in sorted_items[:len(sorted_items) - MAX_CACHE_SIZE]]
        for key in keys_to_remove:
            del translation_cache[key]
            del cache_timestamps[key]

# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    cleanup_cache()
    return HealthResponse(
        status="healthy",
        supported_languages=SUPPORTED_LANGUAGES,
        cache_stats={
            "cache_size": len(translation_cache),
            "max_cache_size": MAX_CACHE_SIZE,
            "cache_duration_hours": CACHE_DURATION // 3600
        }
    )

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate text between supported languages"""
    try:
        # Validate languages
        if request.source_lang not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported source language: {request.source_lang}")
        if request.target_lang not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported target language: {request.target_lang}")
        
        # Check cache first
        cache_key = get_cache_key(request.text, request.source_lang, request.target_lang)
        if cache_key in translation_cache:
            cached_result = translation_cache[cache_key]
            logger.info(f"Cache hit for translation: {request.source_lang} -> {request.target_lang}")
            return cached_result
        
        # Perform translation
        translated_text, confidence = translation_service.translate_text(
            request.text, 
            request.source_lang, 
            request.target_lang, 
            request.preserve_tokens
        )
        
        # Extract preserved tokens for response
        preserved_tokens = {}
        if request.preserve_tokens:
            preserved_tokens = translation_service._extract_tokens(request.text)
        
        # Create response
        response = TranslationResponse(
            translated_text=translated_text,
            confidence=confidence,
            preserved_tokens=preserved_tokens,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            success=True
        )
        
        # Cache the result
        translation_cache[cache_key] = response
        cache_timestamps[cache_key] = time.time()
        
        logger.info(f"Translation completed: {request.source_lang} -> {request.target_lang} (confidence: {confidence})")
        return response
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {"languages": SUPPORTED_LANGUAGES}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

