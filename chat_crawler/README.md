@# Enhanced Chatbot Detection Script

## Overview

The `detectchat.py` script has been significantly enhanced to detect a comprehensive range of chatbot and voice chat services, including the specifically requested **Vapi** and **ElevenLabs** services.

## Enhanced Capabilities

### 🎤 Voice AI Services (6 services)
- **Vapi** - Voice AI platform for conversational interfaces
- **ElevenLabs** - Text-to-speech and voice AI service  
- **Voiceflow** - Conversational AI platform with voice capabilities
- **AssemblyAI** - Speech recognition and audio intelligence API
- **Deepgram** - Speech recognition API
- **Azure Speech** - Microsoft Azure Speech Services

### 🤖 AI Chatbots (6 services)
- **OpenAI ChatGPT Widget** - OpenAI ChatGPT integration
- **Anthropic Claude** - Anthropic Claude AI assistant
- **Google Dialogflow** - Google Dialogflow conversational AI
- **Microsoft Bot Framework** - Microsoft Bot Framework
- **Rasa** - Open source conversational AI
- **Botpress** - Open source chatbot platform

### 💬 Customer Support Chatbots (17 services)
- **Intercom** - Customer messaging platform
- **Drift** - Conversational marketing platform
- **Zendesk Chat** - Customer support chat
- **Tidio** - Live chat and chatbots
- **Crisp** - Customer messaging platform
- **LiveChat** - Live chat software
- **HubSpot** - Customer support chat
- **Freshchat** - Customer messaging software
- **Olark** - Live chat software
- **Tawk.to** - Free live chat software
- **Chatra** - Live chat messenger
- **Smartsupp** - Live chat and video recording
- **Pure Chat** - Live chat software
- **Acquire** - Customer engagement platform
- **Userlike** - Live chat messenger
- **Chaport** - Live chat messenger
- **JivoChat** - Live chat for websites

## Detection Methods

The enhanced script uses multiple detection techniques:

1. **Script Source URL Pattern Matching** - Detects chatbot services by their CDN URLs
2. **Script Content Analysis** - Searches script content for service identifiers
3. **JavaScript Variable Detection** - Checks for initialization variables in the global scope
4. **Environment Variable Detection** - Detects references to environment variables (NEW)
5. **Text Pattern Matching** - Searches page content for service-related text patterns (NEW)
6. **Console Log Analysis** - Captures and analyzes console messages for service indicators (NEW)
7. **DOM Element Detection** - Looks for specific element IDs and CSS classes
8. **Voice Capability Detection** - Detects WebRTC, Audio Context, and Speech Recognition APIs
9. **Confidence Scoring** - Assigns confidence levels (high/medium/low) based on detection methods

## Specific Service Declarations

### ✅ Vapi (Voice AI): **CAN BE DETECTED** (ENHANCED)
- **Detection patterns**: `vapi.ai`, `vapi.dev`, `vapi.com`
- **JavaScript variables**: `Vapi`, `vapi`, `VAPI_PUBLIC_KEY`, `VAPI_PUBLIK_KEY`
- **Environment variables**: `VITE_VAPI_PUBLIK_KEY`, `VITE_VAPI_PUBLIC_KEY`, `REACT_APP_VAPI_PUBLIC_KEY`, `NEXT_PUBLIC_VAPI_PUBLIC_KEY`
- **Text patterns**: `vapi`, `voice assistant`, `AI voice assistant`, `web-based AI voice assistant`
- **Console log detection**: Captures Vapi-related error messages and environment variable references
- **Description**: Voice AI platform for conversational interfaces

### ✅ ElevenLabs (Voice AI): **CAN BE DETECTED**  
- **Detection patterns**: `elevenlabs.io`, `elevenlabs.ai`
- **JavaScript variables**: `ElevenLabs`, `elevenlabs`
- **Description**: Text-to-speech and voice AI service

### Voice Chat Services
The script can detect **6 different voice AI services** including the requested Vapi and ElevenLabs.

### Text Chat Services  
The script can detect **23 different text chat services** including modern AI chatbots and traditional customer support widgets.

## Installation

1. Install dependencies:
```bash
pip install -r chat_crawler/requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Usage

```bash
python chat_crawler/detectchat.py <URL>
```

### Examples:
```bash
python chat_crawler/detectchat.py https://example.com
python chat_crawler/detectchat.py intercom.com
python chat_crawler/detectchat.py https://vapi.ai
```

## Sample Output

```
================================================================================
🔍 CHATBOT & VOICE CHAT DETECTION REPORT
================================================================================
URL: https://example.com
Total Services Detected: 2

🎤 VOICE CAPABILITIES DETECTED:
   WebRTC Support: ✅ Yes
   Audio Context: ✅ Yes  
   Speech Recognition: ❌ No

📊 CATEGORIES DETECTED: Voice AI, Customer Support

🤖 VOICE AI SERVICES:
--------------------------------------------------
   🟢 Vapi (high confidence)
      Description: Voice AI platform for conversational interfaces
      Detection methods:
        • Script sources: ['https://cdn.vapi.ai/vapi.js']
        • JavaScript variable 'Vapi' found

💬 CUSTOMER SUPPORT SERVICES:
--------------------------------------------------
   🟡 Intercom (medium confidence)
      Description: Customer messaging platform
      Detection methods:
        • Script content contains 'intercom.io'

🎯 SPECIFIC SERVICE DECLARATIONS:
--------------------------------------------------
   Vapi (Voice AI): ✅ DETECTED
   ElevenLabs (Voice AI): ❌ NOT DETECTED
   Voice Chat Services: ✅ 1 DETECTED
   Text Chat Services: ✅ 1 DETECTED
================================================================================
```

## Clear Declarations

When **NO** chatbot or voice chat services are detected, the script will clearly state:

```
❌ NO CHATBOT OR VOICE CHAT SERVICES DETECTED
   This website does not appear to have:
   • Vapi or other voice AI integrations
   • ElevenLabs or text-to-speech services
   • Traditional customer support chatbots  
   • Modern AI chatbot widgets
```

## Key Improvements

1. **Comprehensive Coverage**: Expanded from 7 to 29 different chatbot services
2. **Voice AI Focus**: Added specific detection for voice chat services like Vapi and ElevenLabs
3. **Modern AI Chatbots**: Added detection for ChatGPT, Claude, and other AI assistants
4. **Enhanced Detection**: Multiple detection methods with confidence scoring
5. **Environment Variable Detection**: Detects build-time environment variable references (FIXED VAPI DETECTION)
6. **Console Log Analysis**: Captures runtime errors and messages for additional detection clues
7. **Text Pattern Matching**: Searches page content for service-related descriptions and keywords
8. **Clear Reporting**: Categorized results with specific declarations
9. **Voice Capabilities**: Detects underlying voice/audio technologies
10. **Better Error Handling**: Robust error handling and timeout management

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: Playwright (for browser automation)
- **Async Support**: Full async/await implementation
- **Browser**: Chromium (headless mode)
- **Timeout**: 30 seconds per page load
- **Categories**: Voice AI, AI Chatbot, Customer Support

## Bug Fix for Vapi Detection

**ISSUE RESOLVED**: The original script failed to detect Vapi on cyberplanet.tech despite the site having Vapi-enabled voice chat.

**ROOT CAUSE**: The detection patterns were too narrow and missed modern implementation patterns:
- Environment variable references in build tools (Vite, React, Next.js)
- Console error messages indicating missing API keys
- Text content describing voice assistant functionality

**SOLUTION IMPLEMENTED**:
1. **Enhanced Environment Variable Detection**: Added patterns for `VITE_VAPI_PUBLIK_KEY`, `REACT_APP_VAPI_PUBLIC_KEY`, etc.
2. **Console Log Analysis**: Captures console messages like "VITE_VAPI_PUBLIK_KEY is not set in environment variables"
3. **Text Pattern Matching**: Detects descriptions like "AI voice assistant", "web-based AI voice assistant"
4. **Improved Confidence Scoring**: Multiple detection methods increase confidence levels

**VERIFICATION**: The enhanced script now successfully detects Vapi implementations that use:
- Modern build tools (Vite, Webpack, etc.)
- Environment variable configuration
- Descriptive content about voice assistant functionality
- Console error messages indicating Vapi integration

The enhanced script provides comprehensive chatbot detection with specific focus on the requested Vapi and ElevenLabs services, clearly declaring their presence or absence on any given website.
