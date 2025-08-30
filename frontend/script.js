let token = null;
let currentUser = null;

// ========== Authentication Functions ==========
function toggleSignup() {
  document.getElementById("login-container").classList.add("hidden");
  document.getElementById("signup-container").classList.remove("hidden");
}

function toggleLogin() {
  document.getElementById("signup-container").classList.add("hidden");
  document.getElementById("login-container").classList.remove("hidden");
}

async function handleLogin() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    showNotification("Please fill in all fields", "error");
    return;
  }

  const loginBtn = document.querySelector('#login-container .btn-primary');
  const originalText = loginBtn.innerHTML;
  
  try {
    // Show loading state
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
    loginBtn.disabled = true;

    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }

    const data = await response.json();
    token = data.token;
    currentUser = username;
    
    // Store user info
    localStorage.setItem('queryfarmer_user', username);
    
    // Transition to chat
    document.getElementById("login-container").classList.add("hidden");
    document.getElementById("chat-container").classList.remove("hidden");
    
    showNotification(`Welcome back, ${username}!`, "success");
    
  } catch (err) {
    showNotification(err.message, "error");
  } finally {
    // Reset button state
    loginBtn.innerHTML = originalText;
    loginBtn.disabled = false;
  }
}

async function handleSignup() {
  const username = document.getElementById("new-username").value.trim();
  const password = document.getElementById("new-password").value.trim();

  if (!username || !password) {
    showNotification("Please fill in all fields", "error");
    return;
  }

  if (password.length < 6) {
    showNotification("Password must be at least 6 characters", "error");
    return;
  }

  const signupBtn = document.querySelector('#signup-container .btn-primary');
  const originalText = signupBtn.innerHTML;
  
  try {
    // Show loading state
    signupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
    signupBtn.disabled = true;

    const response = await fetch("http://127.0.0.1:8000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Signup failed");
    }

    showNotification("Account created successfully! Please log in.", "success");
    toggleLogin();
    
  } catch (err) {
    showNotification(err.message, "error");
  } finally {
    // Reset button state
    signupBtn.innerHTML = originalText;
    signupBtn.disabled = false;
  }
}

function logout() {
  token = null;
  currentUser = null;
  localStorage.removeItem('queryfarmer_user');
  
  // Clear chat
  document.getElementById("chat-box").innerHTML = `
    <div class="welcome-message">
      <div class="welcome-icon">
        <i class="fas fa-seedling"></i>
      </div>
      <h2>Welcome to QueryFARMER!</h2>
      <p>I'm here to help you with farming questions, crop advice, pest management, and agricultural policies. Ask me anything!</p>
    </div>
  `;
  
  // Show login
  document.getElementById("chat-container").classList.add("hidden");
  document.getElementById("login-container").classList.remove("hidden");
  
  showNotification("Logged out successfully", "info");
}

// ========== Chat Functions ==========
async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value.trim();
  const chatBox = document.getElementById("chat-box");
  const sendBtn = document.getElementById("send-btn");

  if (!question) return;

  // Add user message
  addMessage("user", question);
  input.value = "";

  // Disable input and show loading
  input.disabled = true;
  sendBtn.disabled = true;
  sendBtn.classList.add("loading");

  // Add temporary bot "thinking..." message
  const thinkingMsg = addMessage("bot", "Thinking... 🤔", true);

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error("Failed to get response from server");
    }

    const data = await response.json();

    // Replace thinking message with actual response
    thinkingMsg.querySelector('.message-content').innerText = data.answer || "No answer received.";
    
  } catch (err) {
    thinkingMsg.querySelector('.message-content').innerText = "Sorry, I'm having trouble connecting right now. Please try again later.";
    console.error("Chat error:", err);
  } finally {
    // Re-enable input
    input.disabled = false;
    sendBtn.disabled = false;
    sendBtn.classList.remove("loading");
    input.focus();
  }
}

function addMessage(sender, text, returnNode = false) {
  const chatBox = document.getElementById("chat-box");
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  
  message.innerHTML = `
    <div class="message-content">
      ${text}
    </div>
  `;
  
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;

  return returnNode ? message : null;
}

function handleKeyPress(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    askQuestion();
  }
}

// ========== Utility Functions ==========
function showNotification(message, type = "info") {
  // Remove existing notifications
  const existing = document.querySelector('.notification');
  if (existing) existing.remove();

  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <i class="fas fa-${getNotificationIcon(type)}"></i>
      <span>${message}</span>
    </div>
  `;

  // Add styles
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${getNotificationColor(type)};
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    animation: slideInRight 0.3s ease-out;
    max-width: 300px;
    font-size: 14px;
  `;

  document.body.appendChild(notification);

  // Auto-remove after 4 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.animation = 'slideOutRight 0.3s ease-out';
      setTimeout(() => notification.remove(), 300);
    }
  }, 4000);
}

function getNotificationIcon(type) {
  const icons = {
    success: 'check-circle',
    error: 'exclamation-circle',
    warning: 'exclamation-triangle',
    info: 'info-circle'
  };
  return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
  const colors = {
    success: '#10b981',
    error: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6'
  };
  return colors[type] || '#3b82f6';
}

// ========== i18n & Translation Variables ==========
let currentLanguage = 'en';
let translations = {};
let translationCache = {};

// ========== Language Management ==========
function showLanguageSelector() {
  if (!localStorage.getItem('selected_language')) {
    document.getElementById('language-modal').classList.remove('hidden');
    // Block all other interactions until language selected
    document.body.style.overflow = 'hidden';
  }
}

function selectLanguage(langCode) {
  currentLanguage = langCode;
  localStorage.setItem('selected_language', langCode);
  
  // Update HTML lang attribute for accessibility
  document.documentElement.lang = langCode;
  
  // Initialize i18n
  initializeI18n(langCode);
  
  // Hide language modal
  hideLanguageModal();
  
  // Show main app
  showMainApp();
  
  showNotification(`Language changed to ${getLanguageName(langCode)}`, 'success');
}

function hideLanguageModal() {
  document.getElementById('language-modal').classList.add('hidden');
  document.body.style.overflow = 'auto';
}

function getLanguageName(langCode) {
  const languageNames = {
    'en': 'English',
    'hi': 'हिंदी',
    'gu': 'ગુજરાતી',
    'mr': 'मराठी',
    'bn': 'বাংলা'
  };
  return languageNames[langCode] || langCode;
}

// ========== i18n Initialization ==========
async function initializeI18n(langCode) {
  try {
    const response = await fetch(`/frontend/locales/${langCode}.json`);
    if (!response.ok) {
      throw new Error(`Failed to load language resources: ${response.status}`);
    }
    
    translations = await response.json();
    window.i18n = {
      t: (key) => translations[key] || key,
      currentLang: langCode
    };
    
    // Update all UI text
    updateAllUIText();
    
    console.log(`i18n initialized for ${langCode}`);
  } catch (error) {
    console.error('Failed to load language resources:', error);
    fallbackToEnglish();
  }
}

function fallbackToEnglish() {
  currentLanguage = 'en';
  localStorage.setItem('selected_language', 'en');
  showNotification('Language resources failed to load, using English', 'warning');
  
  // Load English as fallback
  fetch('/frontend/locales/en.json')
    .then(response => response.json())
    .then(data => {
      translations = data;
      window.i18n = {
        t: (key) => translations[key] || key,
        currentLang: 'en'
      };
      updateAllUIText();
    })
    .catch(err => {
      console.error('Even English fallback failed:', err);
    });
}

function updateAllUIText() {
  // Update all translatable elements
  const elements = document.querySelectorAll('[data-i18n]');
  elements.forEach(element => {
    const key = element.getAttribute('data-i18n');
    if (translations[key]) {
      element.textContent = translations[key];
    }
  });
  
  // Update placeholders
  const inputs = document.querySelectorAll('input[data-i18n-placeholder]');
  inputs.forEach(input => {
    const key = input.getAttribute('data-i18n-placeholder');
    if (translations[key]) {
      input.placeholder = translations[key];
    }
  });
  
  // Update specific elements
  updateSpecificElements();
}

function updateSpecificElements() {
  // Update welcome message
  const welcomeTitle = document.querySelector('.welcome-message h2');
  if (welcomeTitle && translations.welcome) {
    welcomeTitle.textContent = translations.welcome;
  }
  
  const welcomeSubtitle = document.querySelector('.welcome-message p');
  if (welcomeSubtitle && translations.welcome_subtitle) {
    welcomeSubtitle.textContent = translations.welcome_subtitle;
  }
  
  // Update input placeholder
  const questionInput = document.getElementById('question');
  if (questionInput && translations.ask_question) {
    questionInput.placeholder = translations.ask_question;
  }
  
  // Update language selector text
  const languageTitle = document.getElementById('language-title');
  if (languageTitle && translations.language_selector) {
    languageTitle.textContent = translations.language_selector;
  }
  
  const languageSubtitle = document.getElementById('language-subtitle');
  if (languageSubtitle && translations.select_language) {
    languageSubtitle.textContent = translations.select_language;
  }
}

// ========== Translation Service ==========
async function translateText(text, sourceLang, targetLang) {
  try {
    // Check cache first
    const cacheKey = `${text}:${sourceLang}:${targetLang}`;
    if (translationCache[cacheKey]) {
      return translationCache[cacheKey];
    }
    
    // Call translation microservice
    const response = await fetch('http://127.0.0.1:8001/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text,
        source_lang: sourceLang,
        target_lang: targetLang,
        preserve_tokens: true
      })
    });
    
    if (!response.ok) {
      throw new Error(`Translation failed: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.success) {
      // Cache the result
      translationCache[cacheKey] = data.translated_text;
      return data.translated_text;
    } else {
      throw new Error('Translation service returned error');
    }
    
  } catch (error) {
    console.error('Translation error:', error);
    // Return original text with fallback indicator
    return `[${targetLang.toUpperCase()}] ${text}`;
  }
}

// ========== Enhanced Chat Functions with Translation ==========
async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value.trim();
  const chatBox = document.getElementById("chat-box");
  const sendBtn = document.getElementById("send-btn");

  if (!question) return;

  // Add user message
  addMessage("user", question);
  input.value = "";

  // Disable input and show loading
  input.disabled = true;
  sendBtn.disabled = true;
  sendBtn.classList.add("loading");

  // Add temporary bot "thinking..." message
  const thinkingText = translations.thinking || "Thinking... 🤔";
  const thinkingMsg = addMessage("bot", thinkingText, true);

  try {
    let backendQuestion = question;
    let backendResponse;
    
    // Translate user question to English if needed
    if (currentLanguage !== 'en') {
      try {
        // Show translation loading
        thinkingMsg.querySelector('.message-content').innerText = 
          translations.loading_translation || "Translating...";
        
        backendQuestion = await translateText(question, currentLanguage, 'en');
        
        // Show thinking message
        thinkingMsg.querySelector('.message-content').innerText = thinkingText;
      } catch (translationError) {
        console.error('Translation failed:', translationError);
        // Continue with original question
        backendQuestion = question;
      }
    }
    
    // Send to backend
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ question: backendQuestion })
    });

    if (!response.ok) {
      throw new Error("Failed to get response from server");
    }

    const data = await response.json();
    backendResponse = data.answer || "No answer received.";
    
    // Translate response back to user language if needed
    let finalResponse = backendResponse;
    if (currentLanguage !== 'en') {
      try {
        thinkingMsg.querySelector('.message-content').innerText = 
          translations.loading_translation || "Translating...";
        
        finalResponse = await translateText(backendResponse, 'en', currentLanguage);
      } catch (translationError) {
        console.error('Response translation failed:', translationError);
        // Show fallback message
        finalResponse = translations.translation_unavailable || 
                       "Translation temporarily unavailable, showing in English";
        finalResponse += "\n\n" + backendResponse;
      }
    }
    
    // Replace thinking message with actual response
    thinkingMsg.querySelector('.message-content').innerText = finalResponse;
    
  } catch (err) {
    const errorMessage = translations.connection_error || 
                         "Sorry, I'm having trouble connecting right now. Please try again later.";
    thinkingMsg.querySelector('.message-content').innerText = errorMessage;
    console.error("Chat error:", err);
  } finally {
    // Re-enable input
    input.disabled = false;
    sendBtn.disabled = false;
    sendBtn.classList.remove("loading");
    input.focus();
  }
}

// ========== Auto-login Check ==========
function checkAutoLogin() {
  const savedUser = localStorage.getItem('queryfarmer_user');
  if (savedUser) {
    currentUser = savedUser;
    // Auto-login logic could be added here
    // For now, just show the user was previously logged in
    console.log(`Previous user: ${savedUser}`);
  }
}

// ========== Initialize ==========
document.addEventListener('DOMContentLoaded', function() {
  checkAutoLogin();
  
  // Add notification animations to CSS
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInRight {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(100%); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
  
  // Check for language selection
  const selectedLanguage = localStorage.getItem('selected_language');
  if (!selectedLanguage) {
    // Show language selector on first visit
    showLanguageSelector();
  } else {
    // Initialize with saved language
    currentLanguage = selectedLanguage;
    document.documentElement.lang = selectedLanguage;
    initializeI18n(selectedLanguage);
    showMainApp();
  }
  
  // Focus on first input
  const firstInput = document.querySelector('input');
  if (firstInput) firstInput.focus();
});

// ========== App Display Functions ==========
function showMainApp() {
  // Show the main application
  document.getElementById('login-container').classList.remove('hidden');
  document.getElementById('signup-container').classList.add('hidden');
  document.getElementById('chat-container').classList.add('hidden');
}

// ========== Error Handling ==========
window.addEventListener('error', function(e) {
  console.error('Global error:', e.error);
  showNotification('Something went wrong. Please refresh the page.', 'error');
});

// ========== Network Status ==========
window.addEventListener('online', function() {
  showNotification('Connection restored', 'success');
});

window.addEventListener('offline', function() {
  showNotification('You are offline. Some features may not work.', 'warning');
});
