# Import necessary libraries
import pandas as pd
import numpy as np
import ipaddress
import dns.resolver
import dns.reversename
import pygeoip
import matplotlib.pyplot as plt
import os

# Load GeoIP databases
gi = pygeoip.GeoIP('./GeoIP_DBS/GeoIP.dat')
gi2 = pygeoip.GeoIP('./GeoIP_DBS/GeoIPASNum.dat')

# Create output directory for graphs
output_dir = 'graphs'
os.makedirs(output_dir, exist_ok=True)

### Functions for IP geolocalization and DNS resolution
def geolocate_ip(ip):
    try:
        cc = gi.country_code_by_addr(ip)
        org = gi2.org_by_addr(ip)
        return cc, org
    except Exception as e:
        return None, None

def resolve_dns(domain):
    try:
        addr = dns.resolver.resolve(domain, 'A')
        return [str(a) for a in addr]
    except Exception as e:
        return []

def reverse_dns(ip):
    try:
        name = dns.reversename.from_address(ip)
        addr = dns.resolver.resolve(name, 'PTR')
        return [str(a) for a in addr]
    except Exception as e:
        return []

### Read parquet data files
data = pd.read_parquet("./dataset1/data1.parquet")
test_data = pd.read_parquet("./dataset1/test1.parquet")
servers_data = pd.read_parquet("./dataset1/servers1.parquet")

# Add country information
data['src_country'] = data['src_ip'].apply(lambda ip: geolocate_ip(ip)[0])
data['dst_country'] = data['dst_ip'].apply(lambda ip: geolocate_ip(ip)[0])

# Convert timestamp column
data['timestamp'] = pd.to_timedelta(data['timestamp'] * 10000, unit='us')
data['timestamp'] = pd.Timestamp("2023-01-01") + data['timestamp']

# Get general statistics of the data
general_stats = data.describe(include='all')
print("General Statistics:\n", general_stats)

# Identify internal servers/services
internal_network = ipaddress.IPv4Network('192.168.1.0/24')
data['is_internal_src'] = data['src_ip'].apply(lambda ip: ipaddress.IPv4Address(ip) in internal_network)
data['is_internal_dst'] = data['dst_ip'].apply(lambda ip: ipaddress.IPv4Address(ip) in internal_network)

internal_servers = data[data['is_internal_dst']]['dst_ip'].unique()
print(f"Internal Servers/Services: {internal_servers}")

# Describe and quantify traffic exchanges
internal_to_internal = data[data['is_internal_src'] & data['is_internal_dst']]
internal_to_external = data[data['is_internal_src'] & ~data['is_internal_dst']]
external_to_internal = data[~data['is_internal_src'] & data['is_internal_dst']]

print(f"Internal to Internal Traffic:\n{internal_to_internal.describe()}")
print(f"Internal to External Traffic:\n{internal_to_external.describe()}")
print(f"External to Internal Traffic:\n{external_to_internal.describe()}")

### Visualizations for traffic exchanges
# Traffic exchanges from internal users with internal and external servers
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
internal_to_internal['up_bytes'].hist(bins=50)
plt.title('Internal to Internal Traffic: Uploaded Bytes')
plt.savefig(os.path.join(output_dir, 'internal_to_internal_uploads.png'))

plt.subplot(2, 1, 2)
internal_to_external['up_bytes'].hist(bins=50)
plt.title('Internal to External Traffic: Uploaded Bytes')
plt.savefig(os.path.join(output_dir, 'internal_to_external_uploads.png'))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'traffic_exchanges_internal.png'))
plt.close()

# Traffic exchanges from external users with the corporation public servers
plt.figure(figsize=(12, 6))
external_to_internal['up_bytes'].hist(bins=50)
plt.title('External to Internal Traffic: Uploaded Bytes')
plt.xlabel('Upload Bytes')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_dir, 'external_to_internal_uploads.png'))
plt.close()

### SIEM Rules Definition and Justification

# Rule 1: Detect internal BotNet activities
# Justification: A BotNet often generates a high volume of traffic or unusual traffic patterns (e.g., high upload/download ratio).
def detect_botnet_activities(data):
    threshold_ratio = 10  # Example threshold for upload/download ratio
    a1 = data.groupby(['src_ip'])['up_bytes'].sum()
    a2 = data.groupby(['src_ip'])['down_bytes'].sum()
    a3 = pd.DataFrame(a2 / a1, columns=['ratio'])
    suspicious_ips = a3[(a3['ratio'] > threshold_ratio) | (a3['ratio'] < 1 / threshold_ratio)].index
    return suspicious_ips

# Rule 2: Detect data exfiltration using HTTPS
# Justification: Data exfiltration may involve unusually large volumes of HTTPS traffic.
def detect_data_exfiltration(data):
    high_upload_threshold = 1e6  # Threshold for high upload bytes
    suspicious_ips = data.loc[(data['port'] == 443) & (data['up_bytes'] > high_upload_threshold), 'src_ip']
    return suspicious_ips.unique()

# Rule 3: Detect C&C activities using DNS
# Justification: C&C servers often use DNS to communicate with compromised devices, resulting in high volumes of DNS queries.
def detect_cnc_activities(data):
    dns_queries = data[data['port'] == 53]
    high_dns_query_threshold = 100  # Threshold for high DNS query count
    suspicious_ips = dns_queries['src_ip'].value_counts()
    return suspicious_ips[suspicious_ips > high_dns_query_threshold].index

# Rule 4: Detect anomalous external interactions with corporate servers
# Justification: Anomalous interactions may involve unusual source countries or unexpected high traffic volumes.
def detect_anomalous_external_interactions(data):
    external_ips = data['src_ip'].unique()
    anomalies = []
    for ip in external_ips:
        cc, org = geolocate_ip(ip)
        if cc != 'expected_country_code':  # Replace with the expected country code for your corporation
            anomalies.append(ip)
    return anomalies

### Test of the SIEM Rules and Identification of Anomalous Devices
# Apply SIEM rules to test data
botnet_ips = detect_botnet_activities(test_data)
data_exfiltration_ips = detect_data_exfiltration(test_data)
cnc_ips = detect_cnc_activities(test_data)
anomalous_external_ips = detect_anomalous_external_interactions(servers_data)

print(f"Detected Botnet IPs: {botnet_ips}")
print(f"Detected Data Exfiltration IPs: {data_exfiltration_ips}")
print(f"Detected C&C Activity IPs: {cnc_ips}")
print(f"Detected Anomalous External IPs: {anomalous_external_ips}")

### Visualizing Anomalous Activity
fig, axs = plt.subplots(2, 1, figsize=(12, 10))

# Anomalous upload activity histogram
anomalies_upload = test_data[test_data['src_ip'].isin(botnet_ips)]
anomalies_upload['up_bytes'].hist(bins=50, ax=axs[0])
axs[0].set_title('Anomalous Upload Activity')
axs[0].set_xlabel('Upload Bytes')
axs[0].set_ylabel('Frequency')

# Anomalous download activity histogram
anomalies_download = test_data[test_data['src_ip'].isin(data_exfiltration_ips)]
anomalies_download['down_bytes'].hist(bins=50, ax=axs[1])
axs[1].set_title('Anomalous Download Activity')
axs[1].set_xlabel('Download Bytes')
axs[1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'anomalous_activity.png'))
plt.close()

### Report Generation
report = f"""
### SIEM Rules and Anomaly Detection Report ###

#### 1. Typical Behavior Analysis ####
- Internal Servers/Services: {list(internal_servers)}
- Internal to Internal Traffic: {internal_to_internal.describe().to_dict()}
- Internal to External Traffic: {internal_to_external.describe().to_dict()}
- External to Internal Traffic: {external_to_internal.describe().to_dict()}

#### 2. Anomaly Detection ####
- Detected Botnet IPs: {list(botnet_ips)}
- Detected Data Exfiltration IPs: {list(data_exfiltration_ips)}
- Detected C&C Activity IPs: {list(cnc_ips)}
- Detected Anomalous External IPs: {list(anomalous_external_ips)}

#### 3. Anomalous Activity Analysis ####
- Anomalous upload activity: {anomalies_upload.to_dict()}
- Anomalous download activity: {anomalies_download.to_dict()}
"""

# Save the report to a file
with open("SIEM_report.txt", "w") as f:
    f.write(report)

print("SIEM rules and anomaly detection report generated and saved as SIEM_report.txt")
print("All graphs have been saved to the 'graphs' directory.")
