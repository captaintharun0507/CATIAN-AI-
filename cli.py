#!/usr/bin/env python3
"""
⚓ CAPTAIN AI - Command Line Interface
Easy-to-use CLI for the CAPTAIN AI assistant.
"""

import sys
import os
from captain import PerplexityClone


def print_banner():
    """Print the CAPTAIN AI banner"""
    print("=" * 70)
    print("⚓ CAPTAIN AI - Your AI Navigator for Web Intelligence ⚓")
    print("=" * 70)


def main():
    """Main CLI application"""
    
    print_banner()
    print("\n📌 SETUP:")
    print("1. Get FREE API key: https://platform.openai.com/signup")
    print("2. Set environment variable OR pass it below:")
    print("   Windows: set OPENAI_API_KEY=your_key_here")
    print("   Mac/Linux: export OPENAI_API_KEY=your_key_here")
    print("=" * 70)
    
    # Get API key from user
    api_key = input("\n🔑 Enter your OpenAI API key (or press Enter to use env var): ").strip()
    
    if not api_key:
        api_key = None  # Will use environment variable
    
    try:
        # Initialize the AI
        ai = PerplexityClone(api_key=api_key)
        print("\n✅ AI initialized successfully!\n")
        
        # Interactive chat loop
        print("💬 Ask anything! Type 'quit' or 'exit' to stop.")
        print("💬 Type 'reset' to clear conversation history.\n")
        
        while True:
            try:
                user_input = input("⚓ Captain> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Thanks for sailing with CAPTAIN AI. ⚓")
                    break
                
                if user_input.lower() == 'reset':
                    ai.reset_conversation()
                    continue
                
                if not user_input:
                    continue
                
                # Get answer with search + citations
                answer = ai.ask(user_input)
                
                print("\n" + "=" * 70)
                print("🤖 CAPTAIN AI:")
                print("=" * 70)
                print(answer)
                print("=" * 70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\n📌 To fix:")
        print("1. Get free API key: https://platform.openai.com/signup")
        print("2. Set it as environment variable:")
        print("   Windows: set OPENAI_API_KEY=sk-your-key-here")
        print("   Mac/Linux: export OPENAI_API_KEY=sk-your-key-here")
        print("3. Run this script again")


if __name__ == "__main__":
    main()