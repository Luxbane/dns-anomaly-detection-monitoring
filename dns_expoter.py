import dns.resolver
import time
from prometheus_client import start_http_server, Gauge
from collections import Counter

servers = {
    "adguard": "94.140.14.14",
    "cloudflare": "1.1.1.1",
    "google": "8.8.8.8",
    "quad9": "9.9.9.9"
}

domain = "binusianorg-my.sharepoint.com"

g_time = Gauge('dns_resolve_time_seconds', 'DNS resolve time', ['dns'])
g_valid = Gauge('dns_resolve_valid', 'DNS validity based on majority', ['dns'])

def check_dns():
    results = {}

    # 🔹 Step 1: resolve semua DNS
    for name, ip in servers.items():
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]

        start = time.time()
        try:
            answer = resolver.resolve(domain)
            duration = time.time() - start
            resolved_ip = answer[0].to_text()

            results[name] = (resolved_ip, duration)

        except:
            results[name] = (None, 0)

    # 🔹 Step 2: cari mayoritas IP
    ips = [ip for ip, _ in results.values() if ip is not None]
    majority_ip = None

    if ips:
        majority_ip = Counter(ips).most_common(1)[0][0]

    # 🔹 Step 3: assign valid / invalid
    for name, (ip, duration) in results.items():
        if ip is None:
            valid = 0
        elif ip == majority_ip:
            valid = 1
        else:
            valid = 0

        g_time.labels(dns=name).set(duration)
        g_valid.labels(dns=name).set(valid)

        print(f"{name}: {ip} → {'VALID' if valid else 'BLOCKED'}")

if __name__ == "__main__":
    start_http_server(8000)
    print("DNS exporter running on :8000")

    while True:
        check_dns()
        time.sleep(5)