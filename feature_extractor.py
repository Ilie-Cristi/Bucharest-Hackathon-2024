import tldextract
import re
from urllib.parse import urlparse, parse_qs
import dns.resolver
import requests
import whois as whois
from datetime import datetime
import ssl
import socket




def char_counter(string):
    url_chars = ['.', '-', '_', '/', '?', '=', '@', '&', '!', ' ', '~', ',', '+', '*', '#', '$', '%']
    res = []
    for ch in url_chars:
        res.append(string.count(ch))

    return res



def len_tld(url):
    extracted = tldextract.extract(url)
    return len(extracted.suffix)


def string_len(url):
    return len(url)


def count_vowels(string):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    count = 0

    for char in string:
        if char.lower() in vowels:
            count += 1
    return count


def contains_ip(url):
    ipv4_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    ipv6_pattern = r'\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b|\b(?:[A-F0-9]{1,4}:){1,7}:(?:[A-F0-9]{1,4}:){1,7}[A-F0-9]{1,4}\b'

    return re.search(ipv4_pattern, url) is not None or re.search(ipv6_pattern, url) is not None


def contains_server_or_client(string):
    if "server" in string.lower() or "client" in string.lower():
        return True
    else:
        return False


def count_parameters(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return len(query_params)


def get_parameter_length_sum(url):
    parsed_url = urlparse(url)

    params = parse_qs(parsed_url.query)

    length_sum = sum(len(value[0]) for value in params.values())

    return length_sum



def contains_email(url):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return re.search(email_pattern, url) is not None




def has_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')

        for rdata in answers:
            if "v=spf1" in rdata.strings:
                return True
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
    except dns.resolver.NoAnswer:
        print(f"No SPF record found for {domain}.")
    except dns.exception.Timeout:
        print("DNS query timed out.")

    return False


def get_ip_address(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return answers[0].address
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
    except dns.resolver.NoAnswer:
        print(f"No A record found for {domain}.")
    except dns.exception.Timeout:
        print("DNS query timed out.")

    return None


def get_asn(ip_address):
    try:
        answers = dns.resolver.resolve(f'{ip_address}.origin.asn.cymru.com', 'TXT')

        for rdata in answers:
            m = re.match(r'^\d+\s+\|\s+(\d+)\s+\|\s+\d+\s+\|\s+\d+$', rdata.strings[0].decode('utf-8'))
            if m:
                return int(m.group(1))
    except dns.resolver.NoAnswer:
        print(f"No ASN information found for {ip_address}.")
    except dns.exception.Timeout:
        print("DNS query timed out.")

    return None


def get_response_time(url):
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_domain_age(domain):
    try:
        # Query WHOIS information for the domain
        domain_info = whois.whois(domain)

        # Extract the creation date of the domain
        creation_date = domain_info.creation_date

        # If creation_date is a list (for some TLDs), take the first element
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # Calculate the age of the domain in days
        age = (datetime.now() - creation_date).days
        return age
    except whois.parser.PywhoisError as e:
        print(f"Error: {e}")
        return None


def get_domain_expiration_age(domain):
    try:
        # Query WHOIS information for the domain
        domain_info = whois.whois(domain)

        # Extract the expiration date of the domain
        expiration_date = domain_info.expiration_date

        # If expiration_date is a list (for some TLDs), take the first element
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        # Calculate the remaining time until domain expiration in days
        remaining_days = (expiration_date - datetime.now()).days
        return remaining_days
    except whois.parser.PywhoisError as e:
        print(f"Error: {e}")
        return None


def get_ttl(hostname):
    try:
        # Query DNS for A records of the hostname
        answers = dns.resolver.resolve(hostname, 'A')

        # Retrieve the TTL value from the first answer
        ttl = answers.rrset.ttl
        return ttl
    except dns.resolver.NXDOMAIN:
        print(f"Hostname {hostname} does not exist.")
    except dns.resolver.NoAnswer:
        print(f"No DNS records found for {hostname}.")
    except dns.exception.Timeout:
        print("DNS query timed out.")

    return None




def has_valid_certificate(domain):
    try:
        # Create a connection to the domain
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # If the connection succeeds, the certificate is valid
                return True
    except ssl.SSLError:
        # If there's a SSL error, the certificate is invalid
        return False
    except Exception as e:
        # Other exceptions could indicate network issues or domain not found
        print("Error:", e)
        return False


def get_number_of_redirects(url):
    try:
        response = requests.get(url, allow_redirects=True)

        # Get the history of redirects and count the number of redirects
        redirects = response.history
        return len(redirects)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None



url = "example.com"
api_key = "YOUR_API_KEY"
cx = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

def is_indexed_on_google(url, api_key, cx):
    try:
        # Make a request to the Custom Search API
        response = requests.get(
            f"https://www.googleapis.com/customsearch/v1?q=site:{url}&key={api_key}&cx={cx}"
        )

        # Check if the response is successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if any search results are returned
            if "items" in data:
                return True
            else:
                return False
        else:
            print(f"Failed to retrieve search results. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False


def is_url_shortened(url):
    # Regular expressions for common URL shortening service patterns
    patterns = [
        r"^https?://(?:www\.)?bit\.ly/",  # bit.ly
        r"^https?://(?:www\.)?t\.co/",  # t.co (Twitter)
        r"^https?://(?:www\.)?goo\.gl/",  # goo.gl (Google)
        # Add more patterns for other URL shortening services as needed
    ]

    # Check if the URL matches any of the patterns
    for pattern in patterns:
        if re.match(pattern, url):
            return True

    return False


def get_resolved_ip_count(url):
    try:
        # Perform a DNS lookup for the IP addresses associated with the URL
        ip_addresses = socket.getaddrinfo(url, None)

        # Count the number of unique IP addresses
        unique_ips = set(ip[4][0] for ip in ip_addresses)
        return len(unique_ips)
    except socket.gaierror as e:
        print(f"Error resolving IP addresses: {e}")
        return None


def get_resolved_nameserver_count(domain):
    try:
        # Perform a DNS lookup for the NS (Name Server) records associated with the domain
        answers = dns.resolver.resolve(domain, 'NS')

        # Count the number of resolved name servers
        return len(answers)
    except dns.resolver.NoAnswer:
        print(f"No name servers found for {domain}.")
        return 0
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
        return 0
    except dns.exception.Timeout:
        print("DNS query timed out.")
        return None


def get_resolved_mx_server_count(domain):
    try:
        # Perform a DNS lookup for the MX (Mail Exchange) records associated with the domain
        answers = dns.resolver.resolve(domain, 'MX')

        # Count the number of resolved MX servers
        return len(answers)
    except dns.resolver.NoAnswer:
        print(f"No MX servers found for {domain}.")
        return 0
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
        return 0
    except dns.exception.Timeout:
        print("DNS query timed out.")
        return None

