#!/usr/bin/env python3
"""
Test Suite for Subdomain Enumeration Project
Automated validation and testing for GitHub repository
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description, timeout=30):
    """Run a command and return success status"""
    print(f"\n[TEST] {description}")
    print(f"[CMD]  {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            print(f"[✅]   PASSED - {description}")
            return True
        else:
            print(f"[❌]   FAILED - {description}")
            if result.stderr:
                print(f"[ERR]  {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[⏰]   TIMEOUT - {description}")
        return False
    except Exception as e:
        print(f"[❌]   ERROR - {description}: {str(e)}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'dns_enumeration.py',
        'subdomain_enumeration.py',
        'wordlists/subdomains.txt',
        'requirements.txt',
        'README.md',
        'LICENSE',
        '.gitignore'
    ]
    
    print(f"\n[PHASE 1] Repository Structure Test")
    print("-" * 40)
    
    passed = 0
    total = len(required_files)
    
    for file in required_files:
        if os.path.exists(file):
            print(f"[✅]   {file}")
            passed += 1
        else:
            print(f"[❌]   {file} missing")
    
    return passed, total

def test_python_syntax():
    """Test Python syntax validation"""
    python_files = ['dns_enumeration.py', 'subdomain_enumeration.py']
    
    print(f"\n[PHASE 2] Python Syntax Validation")
    print("-" * 40)
    
    passed = 0
    total = len(python_files)
    
    for file in python_files:
        if os.path.exists(file):
            if run_command(f"python -m py_compile {file}", f"Compile {file}"):
                passed += 1
        else:
            print(f"[❌]   {file} not found")
    
    return passed, total

def test_help_commands():
    """Test help command functionality"""
    help_tests = [
        ("python dns_enumeration.py --help", "DNS tool help"),
        ("python subdomain_enumeration.py --help", "Subdomain tool help")
    ]
    
    print(f"\n[PHASE 3] Help Command Tests")
    print("-" * 40)
    
    passed = 0
    total = len(help_tests)
    
    for cmd, desc in help_tests:
        if run_command(cmd, desc):
            passed += 1
    
    return passed, total

def test_dependencies():
    """Test if dependencies can be installed"""
    print(f"\n[PHASE 4] Dependency Check")
    print("-" * 40)
    
    passed = 0
    total = 1
    
    if run_command("pip install -q -r requirements.txt", "Install dependencies"):
        passed += 1
    
    return passed, total

def test_wordlist():
    """Test wordlist validation"""
    print(f"\n[PHASE 5] Wordlist Validation")
    print("-" * 40)
    
    wordlist_file = 'wordlists/subdomains.txt'
    passed = 0
    total = 1
    
    try:
        if os.path.exists(wordlist_file):
            with open(wordlist_file, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                
            if len(lines) >= 50:  # Should have at least 50 subdomains
                print(f"[✅]   Wordlist contains {len(lines)} valid entries")
                passed += 1
            else:
                print(f"[❌]   Wordlist too small: {len(lines)} entries")
        else:
            print(f"[❌]   Wordlist file not found: {wordlist_file}")
            
    except Exception as e:
        print(f"[❌]   Error reading wordlist: {str(e)}")
    
    return passed, total

def test_basic_functionality():
    """Test basic tool functionality with safe domain"""
    print(f"\n[PHASE 6] Basic Functionality Tests")
    print("-" * 40)
    
    # Test with a known safe domain
    basic_tests = [
        ("python dns_enumeration.py example.com", "DNS enumeration basic test"),
    ]
    
    passed = 0
    total = len(basic_tests)
    
    for cmd, desc in basic_tests:
        if run_command(cmd, desc):
            passed += 1
    
    return passed, total

def generate_report(all_results):
    """Generate final test report"""
    total_passed = sum(result[0] for result in all_results)
    total_tests = sum(result[1] for result in all_results)
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n{'='*60}")
    print("GITHUB REPOSITORY VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Tests: {total_tests}")
    print(f"Tests Passed: {total_passed}")
    print(f"Tests Failed: {total_tests - total_passed}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print(f"\nDetailed Results:")
    phases = [
        "Repository Structure",
        "Python Syntax", 
        "Help Commands",
        "Dependencies",
        "Wordlist Validation",
        "Basic Functionality"
    ]
    
    for i, (passed, total) in enumerate(all_results):
        status = "✅ PASS" if passed == total else "❌ FAIL"
        print(f"  {phases[i]}: {passed}/{total} {status}")
    
    if success_rate >= 90:
        print(f"\n🎉 REPOSITORY READY FOR GITHUB SUBMISSION!")
        print(f"📊 Excellent quality score: {success_rate:.1f}%")
        return 0
    elif success_rate >= 70:
        print(f"\n⚠️  Repository mostly ready with minor issues")
        print(f"📊 Good quality score: {success_rate:.1f}%")
        return 1
    else:
        print(f"\n❌ Repository needs significant improvements")
        print(f"📊 Quality score: {success_rate:.1f}%")
        return 2

def main():
    """Run all validation tests"""
    print("🔍 SUBDOMAIN ENUMERATION PROJECT - GITHUB VALIDATION")
    print("=" * 60)
    
    # Create wordlists directory if it doesn't exist
    os.makedirs('wordlists', exist_ok=True)
    
    # Move wordlist to correct location if needed
    if os.path.exists('wordlists-subdomains.txt') and not os.path.exists('wordlists/subdomains.txt'):
        os.rename('wordlists-subdomains.txt', 'wordlists/subdomains.txt')
        print("[INFO] Moved wordlist to correct directory structure")
    
    # Run all test phases
    results = []
    results.append(test_file_structure())
    results.append(test_python_syntax())
    results.append(test_help_commands())
    results.append(test_dependencies())
    results.append(test_wordlist())
    results.append(test_basic_functionality())
    
    # Generate final report
    return generate_report(results)

if __name__ == "__main__":
    sys.exit(main())