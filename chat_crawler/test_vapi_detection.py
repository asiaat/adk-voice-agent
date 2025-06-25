#!/usr/bin/env python3
"""
Test script to verify Vapi detection patterns work correctly
"""

def test_vapi_detection_patterns():
    """Test the enhanced Vapi detection patterns"""
    
    # Import the enhanced patterns
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from detectchat import VOICE_CHAT_SERVICES
    
    print("🧪 TESTING ENHANCED VAPI DETECTION PATTERNS")
    print("=" * 60)
    
    # Find Vapi service definition
    vapi_service = next((s for s in VOICE_CHAT_SERVICES if s['name'] == 'Vapi'), None)
    
    if not vapi_service:
        print("❌ ERROR: Vapi service not found in definitions")
        return False
    
    print(f"✅ Found Vapi service definition:")
    print(f"   Name: {vapi_service['name']}")
    print(f"   Category: {vapi_service['category']}")
    print(f"   Description: {vapi_service['description']}")
    
    print(f"\n🔍 DETECTION PATTERNS:")
    print(f"   URL patterns: {vapi_service.get('match', [])}")
    print(f"   JS variables: {vapi_service.get('initVar', [])}")
    print(f"   Environment variables: {vapi_service.get('envVar', [])}")
    print(f"   Text patterns: {vapi_service.get('textPatterns', [])}")
    
    print(f"\n🎯 CYBERPLANET.TECH EVIDENCE SIMULATION:")
    
    # Simulate the evidence we found on cyberplanet.tech
    test_cases = [
        {
            "type": "Console Log",
            "content": "VITE_VAPI_PUBLIK_KEY is not set in environment variables.",
            "should_match": True
        },
        {
            "type": "Page Content", 
            "content": "Web Assistant - Watra is an innovative web-based AI voice assistant solution",
            "should_match": True
        },
        {
            "type": "Page Content",
            "content": "AI voice assistant that takes your customer interaction to a completely new level",
            "should_match": True
        },
        {
            "type": "Script Content",
            "content": "import { vapi } from '@vapi-ai/web'",
            "should_match": True
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['type']}")
        print(f"   Content: \"{test_case['content']}\"")
        
        content_lower = test_case['content'].lower()
        matches = []
        
        # Check environment variables
        for env_var in vapi_service.get('envVar', []):
            if env_var.lower() in content_lower:
                matches.append(f"Environment variable '{env_var}'")
        
        # Check text patterns
        for pattern in vapi_service.get('textPatterns', []):
            if pattern.lower() in content_lower:
                matches.append(f"Text pattern '{pattern}'")
        
        # Check URL patterns
        for match_pattern in vapi_service.get('match', []):
            if match_pattern.lower() in content_lower:
                matches.append(f"URL pattern '{match_pattern}'")
        
        # Check JS variables
        for var in vapi_service.get('initVar', []):
            if var.lower() in content_lower:
                matches.append(f"JS variable '{var}'")
        
        if matches:
            print(f"   ✅ DETECTED: {', '.join(matches)}")
            if not test_case['should_match']:
                print(f"   ⚠️  Unexpected match!")
                all_passed = False
        else:
            print(f"   ❌ NOT DETECTED")
            if test_case['should_match']:
                print(f"   ⚠️  Expected to match but didn't!")
                all_passed = False
    
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ ALL TESTS PASSED - Enhanced Vapi detection should work!")
    else:
        print("❌ SOME TESTS FAILED - Detection patterns need adjustment")
    
    print(f"\n📋 SUMMARY:")
    print(f"   The enhanced script now detects Vapi through:")
    print(f"   • Environment variable references (VITE_VAPI_PUBLIK_KEY)")
    print(f"   • Console log analysis")
    print(f"   • Text content patterns ('voice assistant', 'AI voice assistant')")
    print(f"   • Script content analysis")
    print(f"   • Traditional URL and JS variable detection")
    
    return all_passed

if __name__ == "__main__":
    test_vapi_detection_patterns()
