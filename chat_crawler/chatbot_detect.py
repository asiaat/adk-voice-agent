import sys
import asyncio
from playwright.async_api import async_playwright

KNOWN_CHATBOTS = [
    # Traditional Text Chatbots
    {"name": "Intercom", "match": "intercom.com", "initVar": "Intercom", "version": "Intercom.boot"},
    {"name": "Drift", "match": "drift.com", "initVar": "drift", "version": "drift.version"},
    {"name": "Zendesk", "match": "zendesk.com", "elementId": "ze-snippet", "version": "zE.version"},
    {"name": "Tidio", "match": "tidio.com", "initVar": "tidioChatApi", "version": "tidioChatApi.version"},
    {"name": "Crisp", "match": "crisp.com", "initVar": "$crisp", "version": "$crisp.version"},
    {"name": "LiveChat", "match": "livechat.com", "initVar": "livechat", "envVar": "CHATBOT_URL", "textPatterns": ["chat configuration", "chat API"], "elementId": "live-chat", "version": "livechat.version"},
    {"name": "HubSpot", "match": "hubspot.com", "initVar": "hubspot", "envVar": "CHATBOT_TOKEN", "textPatterns": ["chat initialization"], "elementId": "customer-support", "version": "hubspot.version"},
    {"name": "Tawk.to", "match": "tawk.to", "initVar": "Tawk_API", "version": "Tawk_API.version"},
    {"name": "Olark", "match": "olark.com", "initVar": "Olark", "version": "Olark.version"},
    {"name": "Smooch", "match": "smooch.io", "initVar": "Smooch", "version": "Smooch.version"},
    {"name": "PureChat", "match": "purechat.com", "initVar": "PureChat", "version": "PureChat.version"},
    {"name": "Zoho", "match": "zoho.com", "initVar": "zoho", "version": "zoho.version"},
    {"name": "Helpshift", "match": "helpshift.com", "initVar": "Helpshift", "version": "Helpshift.version"},
    {"name": "Userlike", "match": "userlike.com", "initVar": "Userlike", "version": "Userlike.version"},
    {"name": "LivePerson", "match": "liveperson.net", "initVar": "LivePerson", "version": "LivePerson.version"},
    {"name": "SnapEngage", "match": "snapengage.com", "initVar": "SnapEngage", "version": "SnapEngage.version"},
    {"name": "Chatra", "match": "chatra.io", "initVar": "Chatra", "version": "Chatra.version"},
    {"name": "Smartsupp", "match": "smartsupp.com", "initVar": "Smartsupp", "version": "Smartsupp.version"},
    {"name": "Comm100", "match": "comm100.com", "initVar": "Comm100", "version": "Comm100.version"},
    {"name": "Zopim", "match": "zopim.com", "initVar": "Zopim", "version": "Zopim.version"},
    {"name": "LiveAgent", "match": "liveagent.com", "initVar": "LiveAgent", "version": "LiveAgent.version"},
    {"name": "BoldChat", "match": "boldchat.com", "initVar": "BoldChat", "version": "BoldChat.version"},
    {"name": "Freshdesk", "match": "freshdesk.com", "initVar": "freshdesk", "version": "freshdesk.version"},
    
    # Voice AI & Advanced Chatbots
    {"name": "VAPI", "match": "vapi.ai", "initVar": "vapi", "textPatterns": ["vapi", "voice ai", "voice assistant"], "version": "vapi.version"},
    {"name": "ElevenLabs", "match": "elevenlabs.io", "initVar": "ElevenLabs", "textPatterns": ["elevenlabs", "voice synthesis", "text to speech"], "version": "ElevenLabs.version"},
    {"name": "OpenAI ChatGPT", "match": "openai.com", "initVar": "openai", "textPatterns": ["chatgpt", "openai", "gpt-"], "version": "openai.version"},
    {"name": "Anthropic Claude", "match": "anthropic.com", "initVar": "anthropic", "textPatterns": ["claude", "anthropic"], "version": "anthropic.version"},
    {"name": "Dialogflow", "match": "dialogflow.com", "initVar": "dialogflow", "textPatterns": ["dialogflow", "google assistant"], "version": "dialogflow.version"},
    {"name": "Microsoft Bot Framework", "match": "botframework.com", "initVar": "botframework", "textPatterns": ["bot framework", "microsoft bot"], "version": "botframework.version"},
    {"name": "Amazon Lex", "match": "aws.amazon.com/lex", "initVar": "AWSLex", "textPatterns": ["amazon lex", "aws lex"], "version": "AWSLex.version"},
    {"name": "Rasa", "match": "rasa.com", "initVar": "rasa", "textPatterns": ["rasa", "conversational ai"], "version": "rasa.version"},
    {"name": "Botpress", "match": "botpress.com", "initVar": "botpress", "textPatterns": ["botpress"], "version": "botpress.version"},
    {"name": "Voiceflow", "match": "voiceflow.com", "initVar": "voiceflow", "textPatterns": ["voiceflow", "voice app"], "version": "voiceflow.version"},
    {"name": "Landbot", "match": "landbot.io", "initVar": "landbot", "textPatterns": ["landbot"], "version": "landbot.version"},
    {"name": "ManyChat", "match": "manychat.com", "initVar": "manychat", "textPatterns": ["manychat"], "version": "manychat.version"},
    {"name": "Chatfuel", "match": "chatfuel.com", "initVar": "chatfuel", "textPatterns": ["chatfuel"], "version": "chatfuel.version"},
    {"name": "Botsify", "match": "botsify.com", "initVar": "botsify", "textPatterns": ["botsify"], "version": "botsify.version"},
    {"name": "Ada", "match": "ada.cx", "initVar": "ada", "textPatterns": ["ada support"], "version": "ada.version"},
    {"name": "Replika", "match": "replika.ai", "initVar": "replika", "textPatterns": ["replika"], "version": "replika.version"},
    {"name": "Askly", "match": "askly.me", "initVar": "askly", "textPatterns": ["askly", "chatbot", "customer support"], "elementId": "askly-widget", "version": "askly.version"},
    
    # Generic Detection Patterns
    {"name": "Generic Chatbot", "match": "chatbot", "initVar": "chatbot", "envVar": "CHATBOT_API_KEY", "textPatterns": ["chatbot", "chat widget"], "elementId": "chatbot", "version": "chatbot.version"},
    {"name": "Generic Chat Widget", "match": "chatwidget", "initVar": "chatWidget", "envVar": "CHATBOT_CONFIG", "textPatterns": ["live chat", "customer support"], "elementId": "chat-widget", "version": "chatWidget.version"},
    {"name": "New Chatbot", "match": "newchatbot.com", "initVar": "newChatbot", "textPatterns": ["new chatbot"], "version": "newChatbot.version"},
]
async def detect_chatbots(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='networkidle')

            scripts = await page.eval_on_selector_all(
                'script', 'elements => elements.map(s => s.src || s.innerText)'
            )

            content = await page.content()
            console_logs = []
            page.on('console', lambda msg: console_logs.append(msg.text()))

            found_bots = []

            for bot in KNOWN_CHATBOTS:
                matched_script = next((s for s in scripts if bot.get("match") in s), None)
                has_init_var = False
                has_element = False
                has_env_var = False
                has_text_pattern = False
                version = None

                if "initVar" in bot:
                    try:
                        has_init_var = await page.evaluate(f"typeof window['{bot['initVar']}'] !== 'undefined'")
                        if has_init_var and "version" in bot:
                            version = await page.evaluate(f"window['{bot['version']}']")
                    except:
                        pass

                if "elementId" in bot:
                    has_element = await page.query_selector(f"#{bot['elementId']}") is not None

                if "envVar" in bot:
                    try:
                        has_env_var = await page.evaluate(f"typeof window['{bot['envVar']}'] !== 'undefined'")
                    except:
                        pass

                if "textPatterns" in bot:
                    for pattern in bot["textPatterns"]:
                        if pattern in content or any(pattern in log for log in console_logs):
                            has_text_pattern = True
                            break

                if matched_script or has_init_var or has_element or has_env_var or has_text_pattern:
                    found_bots.append({
                        "name": bot["name"],
                        "matched_script": matched_script,
                        "has_init_var": has_init_var,
                        "has_element": has_element,
                        "has_env_var": has_env_var,
                        "has_text_pattern": has_text_pattern,
                        "version": version
                    })

            # Detailed output for each found bot
            for bot in found_bots:
                print(f"\n🤖 Bot Name: {bot['name']}")
                print("=" * 50)
                
                if bot['matched_script']:
                    print(f"  📜 Matched Script: {bot['matched_script']}")
                if bot['has_init_var']:
                    print("  🔧 Initialization Variable: Present")
                if bot['has_element']:
                    print("  🏷️  DOM Element: Present")
                if bot['has_env_var']:
                    print("  🌐 Environment Variable: Present")
                if bot['has_text_pattern']:
                    print("  📝 Text Pattern: Present")
                if bot['version']:
                    print(f"  📊 Version: {bot['version']}")
                
                # Extract and analyze JavaScript code
                try:
                    js_code = await page.eval_on_selector_all(
                        'script', 'elements => elements.map(s => s.innerText).join("\\n")'
                    )
                    if js_code:
                        # Filter for chatbot-related JavaScript
                        chatbot_js_lines = [line.strip() for line in js_code.split('\n') 
                                          if any(keyword in line.lower() for keyword in 
                                               ['chat', 'bot', 'widget', 'support', 'message', 'conversation'])]
                        if chatbot_js_lines:
                            print(f"  💻 JavaScript Analysis:")
                            for i, line in enumerate(chatbot_js_lines[:10]):  # Show first 10 relevant lines
                                if line:
                                    print(f"    {i+1}. {line[:100]}...")
                except Exception as e:
                    print(f"  ⚠️  JavaScript analysis failed: {e}")

                # Extract network resources
                try:
                    network_resources = await page.query_selector_all('link[href], script[src]')
                    chatbot_resources = []
                    for resource in network_resources:
                        href = await resource.get_attribute('href') or await resource.get_attribute('src')
                        if href and any(keyword in href.lower() for keyword in 
                                      ['chat', 'bot', 'widget', 'support', 'intercom', 'drift', 'zendesk']):
                            chatbot_resources.append(href)
                    
                    if chatbot_resources:
                        print(f"  🌐 Network Resources:")
                        for resource in chatbot_resources[:5]:  # Show first 5 resources
                            print(f"    • {resource}")
                except Exception as e:
                    print(f"  ⚠️  Network resource analysis failed: {e}")

                # Extract chatbot widget HTML structure
                try:
                    if 'elementId' in bot:
                        widget_html = await page.query_selector(f"#{bot['elementId']}")
                        if widget_html:
                            html_content = await widget_html.outer_html()
                            print(f"  🏗️  Widget HTML Structure:")
                            print(f"    {html_content[:200]}...")
                except Exception as e:
                    print(f"  ⚠️  Widget HTML analysis failed: {e}")

                # Extract event handlers and communication methods
                try:
                    event_handlers = [line.strip() for line in js_code.split('\n') 
                                    if any(keyword in line.lower() for keyword in 
                                         ['addeventlistener', 'onclick', 'onload', 'websocket', 'fetch', 'xmlhttprequest'])]
                    if event_handlers:
                        print(f"  🔗 Event Handlers & Communication:")
                        for handler in event_handlers[:5]:  # Show first 5 handlers
                            if handler:
                                print(f"    • {handler[:80]}...")
                except Exception as e:
                    print(f"  ⚠️  Event handler analysis failed: {e}")

                # Extract API endpoints and configuration
                try:
                    api_endpoints = [line.strip() for line in js_code.split('\n') 
                                   if any(keyword in line for keyword in ['https://', 'http://', 'api.', 'cdn.'])]
                    chatbot_apis = [endpoint for endpoint in api_endpoints 
                                  if any(keyword in endpoint.lower() for keyword in 
                                       ['chat', 'bot', 'widget', 'support', 'message'])]
                    if chatbot_apis:
                        print(f"  🔌 API Endpoints:")
                        for api in chatbot_apis[:3]:  # Show first 3 APIs
                            print(f"    • {api[:100]}...")
                except Exception as e:
                    print(f"  ⚠️  API endpoint analysis failed: {e}")

                # Extract configuration objects
                try:
                    config_lines = [line.strip() for line in js_code.split('\n') 
                                  if any(keyword in line.lower() for keyword in 
                                       ['config', 'settings', 'options', 'init'])]
                    chatbot_configs = [config for config in config_lines 
                                     if any(keyword in config.lower() for keyword in 
                                          ['chat', 'bot', 'widget', 'support'])]
                    if chatbot_configs:
                        print(f"  ⚙️  Configuration Objects:")
                        for config in chatbot_configs[:3]:  # Show first 3 configs
                            print(f"    • {config[:80]}...")
                except Exception as e:
                    print(f"  ⚠️  Configuration analysis failed: {e}")

                # Extract related links
                try:
                    links = await page.query_selector_all('a[href]')
                    chatbot_links = []
                    for link in links:
                        href = await link.get_attribute('href')
                        text = await link.inner_text()
                        if href and any(keyword in (href + text).lower() for keyword in 
                                      ['chat', 'support', 'help', 'contact', 'bot']):
                            chatbot_links.append(f"{text} -> {href}")
                    
                    if chatbot_links:
                        print(f"  🔗 Related Links:")
                        for link in chatbot_links[:3]:  # Show first 3 links
                            print(f"    • {link[:80]}...")
                except Exception as e:
                    print(f"  ⚠️  Link analysis failed: {e}")

            await browser.close()
            return found_bots

        except Exception as e:
            await browser.close()
            print(f"❌ Error loading {url}: {e}")
            return []
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot_discovery.py https://example.com")
        sys.exit(1)

    url = sys.argv[1]
    bots = asyncio.run(detect_chatbots(url))
    print(f"\n🔍 Detected chatbots on {url}:\n")
    for bot in bots:
        print(bot)
