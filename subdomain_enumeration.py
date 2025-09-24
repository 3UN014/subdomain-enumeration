#!/usr/bin/env python3
"""
Subdomain Enumeration Tool - Enhanced Version
Professional multi-threaded subdomain discovery for cybersecurity reconnaissance
Author: 3UN014
GitHub: https://github.com/3UN014/subdomain-enumeration
"""

import requests
import threading
import argparse
import sys
import time
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import json
import csv

# Disable SSL warnings for testing purposes
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SubdomainEnumerator:
    def __init__(self, domain, wordlist_file, threads=50, timeout=10, output_file=None, verbose=False):
        self.domain = domain
        self.wordlist_file = wordlist_file
        self.max_threads = threads
        self.timeout = timeout
        self.output_file = output_file
        self.verbose = verbose
        
        # Fixed typo: changed 'discivered_subdomains' to 'discovered_subdomains'
        self.discovered_subdomains = []
        self.lock = threading.Lock()
        
        # Configure requests session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SubdomainEnum/2.0 (Educational Tool; +https://github.com/3UN014/subdomain-enumeration)'
        })
        
        # Statistics
        self.stats = {
            'tested': 0,
            'discovered': 0,
            'errors': 0,
            'start_time': time.time()
        }
    
    def print_banner(self):
        """Display tool banner"""
        banner = """
╔══════════════════════════════════════════════╗
║         Subdomain Enumeration Tool           ║
║              Enhanced Version                ║
║                   3UN014                     ║
╚══════════════════════════════════════════════╝
        """
        print(banner)
        print(f"Target Domain: {self.domain}")
        print(f"Wordlist: {self.wordlist_file}")
        print(f"Max Threads: {self.max_threads}")
        print(f"Timeout: {self.timeout}s")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
    
    def load_wordlist(self):
        """Load subdomain wordlist from file"""
        try:
            with open(self.wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                subdomains = [line.strip().lower() for line in f if line.strip()]
            
            # Remove duplicates
            unique_subdomains = list(set(subdomains))
            print(f"[+] Loaded {len(unique_subdomains)} unique subdomains from wordlist")
            return unique_subdomains
            
        except FileNotFoundError:
            print(f"[!] Wordlist file '{self.wordlist_file}' not found!")
            print("[!] Please ensure the wordlist file exists in the correct path.")
            print("[*] You can download wordlists from:")
            print("    - https://github.com/3UN014/subdomain-enumeration/tree/main/wordlists")
            sys.exit(1)
            
        except Exception as e:
            print(f"[!] Error loading wordlist: {str(e)}")
            return []
    
    def check_subdomain(self, subdomain):
        """Check if subdomain exists and gather information"""
        full_subdomain = f"{subdomain}.{self.domain}"
        
        result = {
            'subdomain': full_subdomain,
            'http_accessible': False,
            'https_accessible': False,
            'http_status': None,
            'https_status': None,
            'ip_address': None,
            'server': None,
            'discovered_at': datetime.now().isoformat()
        }
        
        with self.lock:
            self.stats['tested'] += 1
        
        try:
            # Try to resolve IP address first
            try:
                ip_address = socket.gethostbyname(full_subdomain)
                result['ip_address'] = ip_address
            except socket.gaierror:
                # If DNS resolution fails, subdomain doesn't exist
                return None
            
            # Test HTTP
            try:
                http_url = f"http://{full_subdomain}"
                response = self.session.get(http_url, timeout=self.timeout, allow_redirects=True)
                result['http_accessible'] = True
                result['http_status'] = response.status_code
                result['server'] = response.headers.get('Server', 'Unknown')
            except requests.RequestException:
                pass
            
            # Test HTTPS
            try:
                https_url = f"https://{full_subdomain}"
                response = self.session.get(https_url, timeout=self.timeout, allow_redirects=True, verify=False)
                result['https_accessible'] = True
                result['https_status'] = response.status_code
                if not result['server'] or result['server'] == 'Unknown':
                    result['server'] = response.headers.get('Server', 'Unknown')
            except requests.RequestException:
                pass
            
            # If either HTTP or HTTPS worked, it's a valid subdomain
            if result['http_accessible'] or result['https_accessible']:
                with self.lock:
                    self.discovered_subdomains.append(result)
                    self.stats['discovered'] += 1
                
                # Display immediate results
                status_parts = []
                if result['http_accessible']:
                    status_parts.append(f"HTTP:{result['http_status']}")
                if result['https_accessible']:
                    status_parts.append(f"HTTPS:{result['https_status']}")
                
                status_str = " | ".join(status_parts)
                print(f"[+] Found: {full_subdomain} [{status_str}] [{result['ip_address']}]")
                
                return result
                
        except Exception as e:
            with self.lock:
                self.stats['errors'] += 1
            if self.verbose:
                print(f"[-] Error checking {full_subdomain}: {str(e)}")
        
        return None
    
    def enumerate_subdomains(self):
        """Main enumeration function"""
        self.print_banner()
        
        # Load wordlist
        subdomains = self.load_wordlist()
        if not subdomains:
            print("[!] No subdomains to test!")
            return
        
        print(f"[*] Starting enumeration with {len(subdomains)} subdomains...")
        print(f"[*] Using {self.max_threads} threads\n")
        
        # Use ThreadPoolExecutor for controlled threading
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Submit all tasks
            futures = [executor.submit(self.check_subdomain, sub) for sub in subdomains]
            
            # Wait for completion (optional progress tracking)
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    if self.verbose:
                        print(f"[!] Task error: {str(e)}")
        
        print(f"\n[*] Enumeration completed!")
        self.display_summary()
        
        # Save results if output file specified
        if self.output_file:
            self.save_results()
    
    def display_summary(self):
        """Display enumeration summary"""
        elapsed_time = time.time() - self.stats['start_time']
        
        print(f"\n{'='*60}")
        print("ENUMERATION SUMMARY")
        print(f"{'='*60}")
        print(f"Target Domain: {self.domain}")
        print(f"Subdomains Tested: {self.stats['tested']}")
        print(f"Subdomains Discovered: {self.stats['discovered']}")
        print(f"Errors Encountered: {self.stats['errors']}")
        print(f"Success Rate: {(self.stats['discovered'] / max(self.stats['tested'], 1)) * 100:.1f}%")
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        print(f"Average Rate: {self.stats['tested'] / elapsed_time:.1f} requests/second")
        
        if self.discovered_subdomains:
            print(f"\nDiscovered Subdomains:")
            for result in sorted(self.discovered_subdomains, key=lambda x: x['subdomain']):
                status_parts = []
                if result['http_accessible']:
                    status_parts.append(f"HTTP:{result['http_status']}")
                if result['https_accessible']:
                    status_parts.append(f"HTTPS:{result['https_status']}")
                
                status_str = " | ".join(status_parts)
                print(f"  {result['subdomain']} [{status_str}] [{result['ip_address']}]")
        
        print(f"\n[*] Repository: https://github.com/3UN014/subdomain-enumeration")
    
    def save_results(self):
        """Save results to file"""
        try:
            if self.output_file.endswith('.json'):
                output_data = {
                    'domain': self.domain,
                    'timestamp': datetime.now().isoformat(),
                    'statistics': self.stats,
                    'discovered_subdomains': self.discovered_subdomains,
                    'tool': 'Subdomain Enumeration Tool - Enhanced Version',
                    'repository': 'https://github.com/3UN014/subdomain-enumeration'
                }
                with open(self.output_file, 'w') as f:
                    json.dump(output_data, f, indent=2, default=str)
            
            elif self.output_file.endswith('.csv'):
                with open(self.output_file, 'w', newline='') as f:
                    if self.discovered_subdomains:
                        fieldnames = self.discovered_subdomains[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.discovered_subdomains)
            
            else:  # Default to text format
                with open(self.output_file, 'w') as f:
                    f.write(f"Subdomain Enumeration Results for {self.domain}\n")
                    f.write(f"Tool: Subdomain Enumeration Tool - Enhanced Version\n")
                    f.write(f"Repository: https://github.com/3UN014/subdomain-enumeration\n")
                    f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for result in self.discovered_subdomains:
                        f.write(f"{result['subdomain']}\n")
            
            print(f"[+] Results saved to: {self.output_file}")
            
        except Exception as e:
            print(f"[!] Error saving results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Subdomain Enumeration Tool - Enhanced Version',
        epilog='Example: python %(prog)s example.com -w wordlists/subdomains.txt -t 100 -o results.json\n'
               'Repository: https://github.com/3UN014/subdomain-enumeration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('domain', help='Target domain to enumerate')
    parser.add_argument('-w', '--wordlist', default='wordlists/subdomains.txt', help='Wordlist file (default: wordlists/subdomains.txt)')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('-o', '--output', help='Output file (supports .txt, .json, .csv)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='Subdomain Enumeration Tool v2.0')
    
    args = parser.parse_args()
    
    # Initialize enumerator
    enumerator = SubdomainEnumerator(
        domain=args.domain,
        wordlist_file=args.wordlist,
        threads=args.threads,
        timeout=args.timeout,
        output_file=args.output,
        verbose=args.verbose
    )
    
    try:
        # Start enumeration
        enumerator.enumerate_subdomains()
        
    except KeyboardInterrupt:
        print("\n[!] Enumeration interrupted by user")
        enumerator.display_summary()
        if enumerator.output_file:
            enumerator.save_results()
        sys.exit(1)

if __name__ == "__main__":
    main()
