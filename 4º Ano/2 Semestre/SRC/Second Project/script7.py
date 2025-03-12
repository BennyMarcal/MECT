#DONE CORRETLY

import pandas as pd
import ipaddress
import pygeoip
import matplotlib.pyplot as plt

# Load the data
data_normal = pd.read_parquet('data4.parquet')
data_attack = pd.read_parquet('test4.parquet')

# Get the country name for an IP address
geo1 = pygeoip.GeoIP('GeoIP.dat')
geo2 = pygeoip.GeoIP('GeoIPASNum.dat')

def get_countryname(ip):
    return geo1.country_name_by_addr(ip)

# Add the country column
data_normal['dst_country'] = data_normal['dst_ip'].apply(get_countryname)
data_attack['dst_country'] = data_attack['dst_ip'].apply(get_countryname)

print("FINISHING")

# Calculate the average number of flows to servers in the normal dataset
avg_flows_to_servers = data_normal.groupby('dst_ip').size().mean()
print(f"Average number of flows to servers: {avg_flows_to_servers}")

# Group the attack data by src_ip and dst_ip and count the number of flows
flows_to_servers = data_attack.groupby(['src_ip', 'dst_ip']).size().reset_index(name='flows_count')

# Identify the two IPs with the most flows to servers
top_ips_to_servers = flows_to_servers.groupby('src_ip')['flows_count'].sum().reset_index()
top_ips_to_servers = top_ips_to_servers.sort_values(by='flows_count', ascending=False).head(2)
print(top_ips_to_servers)
