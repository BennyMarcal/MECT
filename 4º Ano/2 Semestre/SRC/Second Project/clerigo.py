import pandas as pd
import pygeoip
import ipaddress
import matplotlib.pyplot as plt

# Load the data
datafile = './data1.parquet'
data = pd.read_parquet(datafile)

# Load GeoIP databases
gi = pygeoip.GeoIP('./GeoIP_DBs/GeoIP.dat')

# Determine if an IP is private
def is_private(ip):
    return ipaddress.ip_address(ip).is_private

# Calculate average flows per user
data['is_private_dst'] = data['dst_ip'].apply(is_private)
flows_to_internet = data[~data['is_private_dst']].groupby('src_ip').size()
flows_within_network = data[data['is_private_dst']].groupby('src_ip').size()

average_flows_to_internet = flows_to_internet.mean()
average_flows_within_network = flows_within_network.mean()

# Plot the results
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['To Internet', 'Within Network']
averages = [average_flows_to_internet, average_flows_within_network]
bars = ax.bar(categories, averages, color=['#1f77b4', '#ff7f0e'], edgecolor='black')

# Add labels
ax.set_xlabel('Flow Destination', fontsize=14, fontweight='bold')
ax.set_ylabel('Average Number of Flows', fontsize=14, fontweight='bold')
ax.set_title('Average Data Flows per User', fontsize=16, fontweight='bold')

# Annotate bars with values
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=12)

# Save the plot
plt.tight_layout()
plt.savefig('./plots/average_data_flows_per_user.png')
plt.show()
