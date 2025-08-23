#!/usr/bin/env python3
"""
Test script to validate improved input handling and prompt understanding
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multi_agent_orchestrator import MultiAgentOrchestrator
import json

def test_input_scenarios():
    """Test various input scenarios to validate improved system behavior"""
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Greeting Only",
            "input": "hi",
            "expected_behavior": "Should provide helpful guidance, not generate roadmap"
        },
        {
            "name": "Vague Input",
            "input": "parking space finder",
            "expected_behavior": "Should ask for more details about the project"
        },
        {
            "name": "Very Short Input",
            "input": "app",
            "expected_behavior": "Should request more specific project details"
        },
        {
            "name": "Valid Mobile App Project",
            "input": "Build a parking space finder mobile app that helps drivers locate available parking spots in real-time using GPS and crowd-sourced data",
            "expected_behavior": "Should generate mobile app roadmap"
        },
        {
            "name": "Valid IoT Project", 
            "input": "Create a smart aquarium monitoring system with temperature, pH, and water level sensors using ESP32",
            "expected_behavior": "Should generate IoT hardware roadmap"
        },
        {
            "name": "Valid Web Platform",
            "input": "Develop a web-based project management platform with team collaboration features and real-time updates",
            "expected_behavior": "Should generate web platform roadmap"
        },
        {
            "name": "Non-Project Input",
            "input": "What's the weather like today?",
            "expected_behavior": "Should explain it's for project roadmaps only"
        }
    ]
    
    print("🧪 Testing AI Project Refiner Input Validation\n")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"Input: '{test_case['input']}'")
        print(f"Expected: {test_case['expected_behavior']}")
        print("-" * 40)
        
        try:
            # Test the validation directly
            validation_result = orchestrator._validate_user_input(test_case['input'])
            
            if validation_result['is_valid']:
                print("✅ VALIDATION: Passed - Input accepted for processing")
                if 'detected_type' in validation_result:
                    print(f"   Detected Type: {validation_result['detected_type']}")
                if 'confidence' in validation_result:
                    print(f"   Confidence: {validation_result['confidence']:.2f}")
            else:
                print("❌ VALIDATION: Failed - Input rejected")
                print("   Response:")
                # Print first few lines of response
                response_lines = validation_result['response'].split('\n')[:3]
                for line in response_lines:
                    if line.strip():
                        print(f"   {line}")
                if len(validation_result['response'].split('\n')) > 3:
                    print("   ...")
                    
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
        
        print()
    
    print("=" * 60)
    print("✅ Input validation testing completed!")
    print("\nTo test the full system:")
    print("1. Deploy the updated code to Vercel")
    print("2. Try the test inputs through the web interface")
    print("3. Verify appropriate responses for each scenario")

def test_project_type_detection():
    """Test project type detection accuracy"""
    
    orchestrator = MultiAgentOrchestrator()
    
    test_inputs = [
        ("Build an iOS app for fitness tracking", "mobile_app"),
        ("Create a smart home IoT system with sensors", "iot_hardware"), 
        ("Develop an e-commerce website with payment integration", "web_platform"),
        ("Build an AI chatbot for customer service", "ai_ml"),
        ("Create an online marketplace for handmade crafts", "ecommerce"),
        ("Develop a desktop application for file management", "general_software")
    ]
    
    print("\n🎯 Testing Project Type Detection\n")
    print("=" * 50)
    
    for input_text, expected_type in test_inputs:
        detected_type = orchestrator._detect_project_type(input_text)
        status = "✅" if detected_type == expected_type else "❌"
        
        print(f"{status} Input: {input_text}")
        print(f"   Expected: {expected_type}")
        print(f"   Detected: {detected_type}")
        print()

if __name__ == "__main__":
    print("🚀 AI Project Refiner - Input Validation Test Suite")
    print("=" * 60)
    
    test_input_scenarios()
    test_project_type_detection()
    
    print("\n📋 Next Steps:")
    print("1. Apply the proposed code changes")
    print("2. Deploy to Vercel") 
    print("3. Test with real user inputs")
    print("4. Monitor for any edge cases that need handling")
