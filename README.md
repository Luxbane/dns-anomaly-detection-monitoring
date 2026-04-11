# 🌐 DNS Anomaly Detection & Monitoring

A monitoring system to analyze DNS resolution behavior across multiple public resolvers and detect anomalies such as filtering, sinkhole responses, and latency differences.

---

## 📌 Overview

This project monitors how different DNS providers resolve the same domain and identifies inconsistencies that may indicate:

* DNS filtering / blocking
* Sinkhole responses
* Resolver performance differences
* Potential network anomalies

The system compares multiple DNS providers including:

* AdGuard
* Cloudflare (1.1.1.1)
* Google (8.8.8.8)
* Quad9 (9.9.9.9)

---

## ❓ Why This Matters

DNS inconsistencies can indicate filtering, misconfiguration, or security policies that affect service accessibility.

A domain may appear accessible under one DNS resolver but be silently blocked or altered under another. This can lead to confusing behavior where users experience different results depending on their network configuration.

---

## 🔍 Key Insight

Some DNS resolvers do not fail requests when blocking a domain. Instead, they return altered IP addresses (known as sinkhole responses).

This makes the domain appear resolved successfully, while actually preventing access to the intended service.

---

## 🎯 Features

* ✅ Multi-DNS resolution comparison
* ⚡ DNS latency measurement
* 🚫 Detection of invalid/sinkhole responses
* 📊 Prometheus metrics export
* 📈 Grafana dashboard visualization
* 🔍 Anomaly detection using majority-based validation

---

## 🧠 How It Works

1. The system queries a domain using multiple DNS resolvers
2. Each resolver returns an IP address
3. The system determines the **majority IP (consensus)**
4. Any resolver returning a different IP is flagged as:

   * ❌ Invalid / Blocked
   * ✅ Valid (if matching majority)

---

## 🧪 Metrics

The exporter exposes the following metrics:

### DNS Validity

```
dns_resolve_valid{dns="google"} 1
dns_resolve_valid{dns="adguard"} 0
```

### DNS Latency

```
dns_resolve_time_seconds{dns="cloudflare"} 0.03
```

---

## 📊 Dashboard

Grafana is used to visualize:

* DNS accessibility (success / blocked)
* Resolution latency comparison
* Stability over time
* DNS inconsistency detection

---

## 🧾 Case Study

This project was tested using:

```
binusianorg-my.sharepoint.com
```

Findings:

* Some DNS providers returned different IP addresses
* Indicates potential filtering or sinkhole behavior
* Public DNS (Google, Cloudflare) showed consistent results

---

## ⚙️ Tech Stack

* Python (dnspython, prometheus_client)
* Prometheus
* Grafana
* Windows environment

---

## 🚀 How to Run

### 1. Create environment

```
conda create -n dns-monitor python=3.11
conda activate dns-monitor
```

### 2. Install dependencies

```
pip install dnspython prometheus_client
```

### 3. Run exporter

```
python dns_test.py
```

### 4. Access metrics

```
http://localhost:8000/metrics
```

---

## 📈 Future Improvements

* Add HTTP-level reachability checks
* Support multiple domains
* Add alerting (Prometheus Alertmanager)
* Detect DNS hijacking patterns

---

## 📌 Notes

DNS resolution success does not always mean accessibility.
Some resolvers may return sinkhole IPs instead of failing, which is why validation logic is required.

---

## 🤝 Author

Built as a network monitoring and analysis project.
