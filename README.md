Subdomain Enumeration 

Key Features

- Enhanced DNS Enumeration: Comprehensive DNS record type querying (A, AAAA, CNAME, MX, TXT, SOA, NS, PTR, SRV)
- Multi-threaded Subdomain Discovery: Efficient concurrent scanning with ThreadPoolExecutor
- Multiple Output Formats: JSON, CSV, and TXT export capabilities
- HTTP/HTTPS Testing: Protocol support with status code analysis
- Server Fingerprinting: Web server identification and metadata extraction
- Professional CLI: Full command-line interface with argument parsing
- Comprehensive Error Handling: Robust timeout and exception management

Quick Start

 prerequisites

- Python 3.7+
- pip package manager

Installation

1. Clone the repository:
bash
git clone https://github.com/yourusername/subdomain-enumeration-project.git
cd subdomain-enumeration-project


2. Install dependencies:
bash
pip install -r requirements.txt


3. Run the tools:
bash
DNS Enumeration
python dns_enumeration.py example.com -v -o results.json

Subdomain Discovery
python subdomain_enumeration.py example.com -t 50 -o subdomains.csv

Usage

DNS Enumeration Tool

bash
Basic usage
python dns_enumeration.py target.com

Advanced usage with options
python dns_enumeration.py target.com -o dns_results.json -v

Help
python dns_enumeration.py --help


Options:
- `-o, --output`: Output file (supports .json, .csv, .txt)
- `-v, --verbose`: Enable verbose output

Subdomain Enumeration Tool

bash
Basic usage
python subdomain_enumeration.py target.com

Advanced usage with custom settings
python subdomain_enumeration.py target.com \
    -w wordlists/subdomains.txt \
    -t 100 \
    --timeout 15 \
    -o results.csv \
    -v


Options:
- `-w, --wordlist`: Wordlist file (default: wordlists/subdomains.txt)
- `-t, --threads`: Number of threads (default: 50)
- `--timeout`: Request timeout in seconds (default: 10)
- `-o, --output`: Output file (supports .json, .csv, .txt)
- `-v, --verbose`: Enable verbose output

Sample Output

DNS Enumeration


```
     DNS Enumeration Tool              
       Enhanced Version                


[+] A records for example.com (1 found): 93.184.216.34

[+] MX records for example.com (1 found): 0 .
```


```
DNS ENUMERATION SUMMARY

Target Domain: example.com
Total Records Found: 2
Record Types Found: 2
```

Subdomain Enumeration
```
Subdomain Enumeration Tool           
    Enhanced Version                


[+] Found: www.example.com [HTTP:200 | HTTPS:200] [93.184.216.34]
[+] Found: mail.example.com [HTTPS:200] [93.184.216.35]'
```

ENUMERATION SUMMARY
```
Target Domain: example.com
Subdomains Tested: 294
Subdomains Discovered: 2
Success Rate: 0.7%
Elapsed Time: 12.3 seconds
Average Rate: 23.9 requests/second
```
Testing

Run the automated test suite to validate functionality:

bash
python tests/test_tools.py


Technical Details

DNS Enumeration Features
- Record Types: A, AAAA, CNAME, MX, TXT, SOA, NS, PTR, SRV (9 types)
- Output Formats: Console, JSON, CSV, TXT
- Error Handling: Timeout, NXDOMAIN, NoAnswer exceptions
- Performance: Configurable timeouts and retries

Subdomain Enumeration Features
- Threading: ThreadPoolExecutor with configurable thread count
- Protocols: HTTP and HTTPS with status code analysis
- Features: IP resolution, server fingerprinting, statistics
- Performance: 20-100+ requests/second depending on configuration
- Output: Multiple formats with detailed metadata

Security & Ethics

Legal Notice
This tool is for educational and authorized testing purposes only.

- Only scan domains you own or have explicit written permission to test
- Respect robots.txt and website terms of service
- Use reasonable rate limits to avoid overwhelming servers
- Follow responsible disclosure practices for any vulnerabilities found

Best Practices
- Start with low thread counts (10-25) for initial testing
- Use longer timeouts for slower networks
- Monitor system resources during large scans
- Document all testing activities for compliance

Educational Value

This project demonstrates:
- DNS Protocol Understandin: Comprehensive DNS record enumeration
- Network Programming: HTTP/HTTPS protocols and socket programming
- Concurrent Programming: Multi-threading with ThreadPoolExecutor
- Error Handling: Robust exception management and timeout controls
- Cybersecurity Concepts: Reconnaissance techniques and ethical hacking
- Software Engineering: CLI design, testing, and documentation

Key Improvements

This enhanced version addresses several issues from basic implementations:

Fixes Applied:
- Fixed Critical Typo: `discivered_subdomains` → `discovered_subdomains`
- Enhanced Error Handling: Comprehensive exception management
- Improved Threading: ThreadPoolExecutor for controlled concurrency
- Added CLI Support: Professional command-line argument parsing

Features Added:
- Multiple Output Formats: JSON, CSV, TXT support
- HTTP/HTTPS Testing: Both protocols with status code analysis
- Performance Monitoring: Statistics tracking and reporting
- Server Fingerprinting: Web server identification
- Professional Output: Banners, progress indicators, summaries

Performance Benchmarks

| Thread Count | Requests/Second | Recommended Use Case |
|--------------|-----------------|---------------------|
| 10-25        | 15-30          | Initial testing, slow networks |
| 50-100       | 30-60          | Standard scanning |
| 100+         | 60-100+        | High-speed authorized testing |

Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `python tests/test_tools.py`
5. Submit a pull request

License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Acknowledgments

- Developed as part of cybersecurity education curriculum
- Inspired by professional penetration testing methodologies
- Built with Python's excellent networking and threading libraries

Related Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [DNS Protocol Specification](https://tools.ietf.org/html/rfc1035)
- [Ethical Hacking Guidelines](https://www.sans.org/white-papers/33901/)

---

Disclaimer: This tool is for educational and authorized security testing only. Users are responsible for complying with all applicable laws and regulations. Unauthorized scanning may violate terms of service and local laws.
