#!/usr/bin/env python3
"""
DNS Enumeration Tool - Enhanced Version
Professional DNS record enumeration for cybersecurity reconnaissance
Author: 3UN014
GitHub: https://github.com/3UN014/subdomain-enumeration
"""

import dns.resolver
import argparse
import json
import csv
import sys
from datetime import datetime

def print_banner():
    """Display tool banner"""  https://github.com/3UN014/subdomain-enumeration
    banner = """
╔══════════════════════════════════════════════╗
║            DNS Enumeration Tool              ║
║              Enhanced Version                ║
║                   3UN014                     ║
╚══════════════════════════════════════════════╝
    """
    print(banner)

def enumerate_dns(target_domain, output_file=None, verbose=False):
    """
    Enumerate DNS records for a target domain
    
    Args:
        target_domain (str): Domain to enumerate
        output_file (str): Optional output file path
        verbose (bool): Enable verbose output
    
    Returns:
        bool: Success status
    """
    # Comprehensive record types for thorough enumeration
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SOA', 'NS', 'PTR', 'SRV']
    
    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 30
    
    results = {}
    total_records = 0
    
    print(f"\n[*] Starting DNS enumeration for: {target_domain}")
    print(f"[*] Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    for record_type in record_types:
        try:
            if verbose:
                print(f"[*] Querying {record_type} records...")
            
            answer = resolver.resolve(target_domain, record_type)
            records = []
            
            for data in answer:
                records.append(str(data))
            
            if records:
                results[record_type] = {
                    'records': records,
                    'count': len(records),
                    'ttl': answer.ttl
                }
                
                print(f"\n[+] {record_type} records for {target_domain} ({len(records)} found):")
                for record in records:
                    print(f"    {record}")
                
                total_records += len(records)
            
        except dns.resolver.NoAnswer:
            if verbose:
                print(f"[-] No {record_type} records found")
            continue
            
        except dns.resolver.NXDOMAIN:
            print(f"[!] Domain {target_domain} does not exist!")
            return False
            
        except dns.resolver.Timeout:
            print(f"[!] Timeout querying {record_type} records")
            continue
            
        except Exception as e:
            print(f"[!] Error querying {record_type}: {str(e)}")
            continue
    
    # Display summary
    print(f"\n{'='*60}")
    print("DNS ENUMERATION SUMMARY")
    print(f"{'='*60}")
    print(f"Target Domain: {target_domain}")
    print(f"Total Records Found: {total_records}")
    print(f"Record Types Found: {len(results)}")
    
    # Save results if output file specified
    if output_file:
        save_results(target_domain, results, output_file)
    
    return True

def save_results(domain, results, output_file):
    """Save enumeration results to file"""
    try:
        if output_file.endswith('.json'):
            output_data = {
                'domain': domain,
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'tool': 'DNS Enumeration Tool - Enhanced Version',
                'repository': 'https://github.com/3UN014/subdomain-enumeration'
            }
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
                
        elif output_file.endswith('.csv'):
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Record_Type', 'Record_Data', 'TTL'])
                
                for record_type, data in results.items():
                    for record in data['records']:
                        writer.writerow([record_type, record, data['ttl']])
                        
        else:  # Default to text format
            with open(output_file, 'w') as f:
                f.write(f"DNS Enumeration Results for {domain}\n")
                f.write(f"Tool: DNS Enumeration Tool - Enhanced Version\n")
                f.write(f"Repository: https://github.com/3UN014/subdomain-enumeration\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for record_type, data in results.items():
                    f.write(f"{record_type} Records ({data['count']} found):\n")
                    for record in data['records']:
                        f.write(f"    {record}\n")
                    f.write("\n")
        
        print(f"[+] Results saved to: {output_file}")
        
    except Exception as e:
        print(f"[!] Error saving results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='DNS Enumeration Tool - Enhanced Version',
        epilog='Example: python %(prog)s example.com -o results.json -v\n'
               'Repository: https://github.com/3UN014/subdomain-enumeration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('domain', help='Target domain to enumerate')
    parser.add_argument('-o', '--output', help='Output file (supports .txt, .json, .csv)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='DNS Enumeration Tool v2.0')
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        success = enumerate_dns(args.domain, args.output, args.verbose)
        
        if not success:
            sys.exit(1)
            
        print(f"\n[+] DNS enumeration completed successfully!")
        print(f"[*] For more tools visit: https://github.com/3UN014/")
        
    except KeyboardInterrupt:
        print("\n[!] Enumeration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
