import pandas as pd
import ipaddress
import dns.resolver
import dns.reversename
import pygeoip
import matplotlib.pyplot as plt

# Dados
data_normal = pd.read_parquet('data1.parquet')
data_attack = pd.read_parquet('test1.parquet')


# Obter o nome da organização para um endereço IP
geo1 = pygeoip.GeoIP('./GeoIP_DBs/GeoIP.dat')
geo2 = pygeoip.GeoIP('./GeoIP_DBs/GeoIPASNum.dat')

def get_countryname(ip):
    return geo1.country_name_by_addr(ip)

# Verificar se todas as portas são iguais em data_normal e data_attack
if (data_normal['port'].unique() != data_attack['port'].unique()).all():
    print("Different ports in data_normal vs data_attack")

# Verificar se todos os protocolos são iguais em data_normal e data_attack
if (data_normal['proto'].unique() != data_attack['proto'].unique()).all():
    print("Different protocols in data_normal vs data_attack")

#print("Comparando etiquetas de país...")
data_normal['dst_country'] = data_normal['dst_ip'].apply(get_countryname)
data_attack['dst_country'] = data_attack['dst_ip'].apply(get_countryname)


def timestamp_to_hour(timestamp):
    timestamp = timestamp / 100
    hours, remainder = divmod(timestamp, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

# POSSIBLE BOTNET
#print("Analisando IPs de servidores em dados normais...")
# Obter IPs privados com mais tráfego de data_normal, tanto src_ip quanto dst_ip
server_ips_normal = data_normal.loc[((data_normal['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)))]

# Verificar conteúdo de server_ips_normal
#print("server_ips_normal head:")
#print(server_ips_normal.head())

# Obter IPs privados 192.168.* como dst_ip com muito tráfego de data_normal e contar o número de fluxos
servers_normal = server_ips_normal.loc[(server_ips_normal['dst_ip'].apply(lambda x: x.startswith('192.168.')))].groupby(['dst_ip']).size().reset_index(name='counts')

# Verificar conteúdo de servers_normal
#print("servers_normal head:")
#print(servers_normal.head())

#print("Analisando IPs de servidores em dados de ataque...")
# Obter IPs privados com mais tráfego de data_attack, tanto src_ip quanto dst_ip
server_ips_attack = data_attack.loc[((data_attack['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)))]

# Verificar conteúdo de server_ips_attack
#print("server_ips_attack head:")
#print(server_ips_attack.head())

# Obter IPs privados 192.168.100.* como dst_ip com muito tráfego TCP de data_attack e contar o número de fluxos
servers_attack = server_ips_attack.loc[(server_ips_attack['dst_ip'].apply(lambda x: x.startswith('192.168.')))].groupby(['dst_ip']).size().reset_index(name='counts')

# Verificar conteúdo de servers_attack
#print("servers_attack head antes do merge:")
#print(servers_attack.head())

# Obter a diferença entre servers_normal e servers_attack
servers_attack = pd.merge(servers_normal, servers_attack, on=['dst_ip'], how='outer')

# Verificar conteúdo de servers_attack após o merge
#print("servers_attack head após o merge:")
#print(servers_attack.head())

# Preencher NaN com 0
servers_attack = servers_attack.fillna(0)

# Attack to Servers C&C

# ON NORMAL DATA
# get ips with flows to servers and count the number of flows
ips_to_servers_normal = data_normal.loc[(data_normal['dst_ip'].isin(servers_normal['dst_ip']))].groupby(['src_ip']).size().reset_index(name='counts')

# ON ATTACK DATA
# get ips with flows to servers and count the number of flows
ips_to_servers_attack = data_attack.loc[(data_attack['dst_ip'].isin(servers_normal['dst_ip']))].groupby(['src_ip']).size().reset_index(name='counts')

# get the difference between ips_to_servers_normal and ips_to_servers_attack
ips_to_servers_attack = pd.merge(ips_to_servers_normal, ips_to_servers_attack, on=['src_ip'], how='outer')
# fill Nan with 0
ips_to_servers_attack = ips_to_servers_attack.fillna(0)
# calculate the rise of flows to servers in %
ips_to_servers_attack['rise'] = (ips_to_servers_attack['counts_y'] - ips_to_servers_attack['counts_x']) / ips_to_servers_attack['counts_x']

# keeo the ones with rise > 200% or rise is infinity and have more than 100 flows to servers in count_y
ips_to_servers_attack = ips_to_servers_attack[((ips_to_servers_attack['rise'] > 1.99) | (ips_to_servers_attack['rise'] == float('inf'))) & (ips_to_servers_attack['counts_y'] > 2000)]

    

# In normal data:
# get flows from private ips to internet and count the number of flows
download_normal = data_normal.loc[((data_normal['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False))].groupby(['src_ip','dst_ip']).size().reset_index(name='counts')
download_normal = download_normal[download_normal['counts'] > 100]

# In attack data:
# get flows from private ips to internet and count the number of flows
download_attack = data_attack.loc[((data_attack['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False))].groupby(['src_ip','dst_ip']).size().reset_index(name='counts')
download_attack = download_attack[download_attack['counts'] > 100]

# get the difference between download_normal and download_attack
download_attack = pd.merge(download_normal, download_attack, on=['src_ip','dst_ip'], how='right')

# calculate the rise of flows to servers in %
download_attack['rise'] = (download_attack['counts_y'] - download_attack['counts_x']) / download_attack['counts_x'] * 100

# keep the ones with rise > 200% or rise is infinity and have more than 100 flows to servers in count_y
download_attack = download_attack[((download_attack['rise'] > 200) | (download_attack['rise'] == float('inf'))) & (download_attack['counts_y'] > 100)]

# get down_bytes from pair src_ip and dst_ip in download_attack
download_attack_flows = data_attack.loc[(data_attack['src_ip'].isin(download_attack['src_ip'])) & (data_attack['dst_ip'].isin(download_attack['dst_ip']))].groupby(['src_ip','dst_ip'])['down_bytes'].sum().reset_index(name='down_bytes')

# merge download_attack_flows with download_attack
download_attack = pd.merge(download_attack, download_attack_flows, on=['src_ip','dst_ip'], how='outer')


# EXFILTRATION?

# ON DATA NORMAL
# from the src_ip count the up_bytes to the internet
up_bytes_normal = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')
# from the src_ip count the number of flows to the internet
flows_normal = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip']).size().reset_index(name='flows')
# merge up_bytes and flows and get the average up_bytes per flow
up_bytes_normal = pd.merge(up_bytes_normal, flows_normal, on=['src_ip'], how='inner')
up_bytes_normal['up/flows'] = up_bytes_normal['up_bytes']/up_bytes_normal['flows']

# ON DATA ATTACK
# from the src_ip count the up_bytes to the internet
up_bytes_attack = data_attack.loc[(data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')
# from the src_ip count the number of flows to the internet
flows_attack = data_attack.loc[(data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip']).size().reset_index(name='flows')
# merge up_bytes and flows and get the average up_bytes per flow
up_bytes_attack = pd.merge(up_bytes_attack, flows_attack, on=['src_ip'], how='inner')
up_bytes_attack['up/flows'] = up_bytes_attack['up_bytes']/up_bytes_attack['flows']

# merge up_bytes_normal and up_bytes_attack and get the difference between up/flows and get the ones that have a 99% increase
up_bytes_diff = pd.merge(up_bytes_normal, up_bytes_attack, on=['src_ip'], how='inner')
up_bytes_diff = up_bytes_diff[(up_bytes_diff['up/flows_y'] > (up_bytes_diff['up/flows_x']*1.99))]

# get the dst_ip that have communication with the src_ip in up_bytes_diff and their org
exfiltration = data_attack.loc[(data_attack['src_ip'].isin(up_bytes_diff['src_ip'])) & (data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)]
exfiltration = exfiltration[['src_ip','dst_ip','timestamp']]
exfiltration['org'] = exfiltration['dst_ip'].apply(lambda x: geo2.org_by_addr(x))
exfiltration['timestamp'] = exfiltration['timestamp'].apply(timestamp_to_hour)
exfiltration['dst_country'] = exfiltration['dst_ip'].apply(get_countryname)

# from these src_ip get the up_bytes to the internet total from data_attack
up_bytes_stat = data_attack.loc[(data_attack['src_ip'].isin(exfiltration['src_ip'])) & (data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_exfiltration')
# from these src_ip get the up_bytes to the internet total from data_normal
up_bytes_stat['up_normal'] = data_normal.loc[(data_normal['src_ip'].isin(exfiltration['src_ip'])) & (data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_normal')['up_normal']
# new column with the difference between up_exfiltration and up_normal in percentage
up_bytes_stat['diff'] = (up_bytes_stat['up_exfiltration'] - up_bytes_stat['up_normal'])/up_bytes_stat['up_normal']*100

# keep the ones that transmitted more than 1GB
up_bytes_stat_1gb = up_bytes_stat[up_bytes_stat['up_exfiltration'] > 1000000000]

# get to know the dst_ip that have communication with the src_ip in up_bytes_stat and their org and dns
exfiltration_stat = data_attack.loc[(data_attack['src_ip'].isin(up_bytes_stat_1gb['src_ip'])) & (data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)]

# group by src_ip and dst_ip and count the number of flows
exfiltration_stat = exfiltration_stat.groupby(['src_ip','dst_ip']).size().reset_index(name='counts')
# from the data_attack get the up_bytes from the src_ip and dst_ip -> src_ip, dst_ip, up_bytes
get_up_bytes = data_attack.loc[(data_attack['src_ip'].isin(exfiltration_stat['src_ip'])) & (data_attack['dst_ip'].isin(exfiltration_stat['dst_ip']))].groupby(['src_ip','dst_ip'])['up_bytes'].sum().reset_index(name='up_bytes')
# merge get_up_bytes with exfiltration_stat
exfiltration_stat = pd.merge(exfiltration_stat, get_up_bytes, on=['src_ip','dst_ip'], how='inner')



# keep the ones that have more than 1GB
exfiltration_stat = exfiltration_stat[exfiltration_stat['up_bytes'] > 1000000000]
# get their org 
exfiltration_stat['org'] = exfiltration_stat['dst_ip'].apply(lambda x: geo2.org_by_addr(x))
# get their country
exfiltration_stat['dst_country'] = exfiltration_stat['dst_ip'].apply(get_countryname)




# COUNTRY STATISTICS

# ON DATA NORMAL
# get the number of flows has destination to each country
normal_country = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['dst_country']).size().reset_index(name='flows_to_country')
# get the number of up_bytes has destination to each country
normal_country['up_bytes'] = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['dst_country'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']
# get the number of down_bytes has destination to each country
normal_country['down_bytes'] = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['dst_country'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']

# make the mean between the up_bytes of one country and the flows to that country
normal_country['up_bytes/flows'] = normal_country['up_bytes']/normal_country['flows_to_country']
# make the mean between the down_bytes of one country and the flows to that country
normal_country['down_bytes/flows'] = normal_country['down_bytes']/normal_country['flows_to_country']

# ON DATA ATTACK
# get the number of flows has destination to each country
attack_country = data_attack.loc[(data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['dst_country']).size().reset_index(name='flows_to_country')
# get the number of up_bytes has destination to each country
attack_country['up_bytes'] = data_attack.loc[(data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['dst_country'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']
# get the number of down_bytes has destination to each country
attack_country['down_bytes'] = data_attack.loc[(data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['dst_country'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']

# make the mean between the up_bytes of one country and the flows to that country
attack_country['up_bytes/flows'] = attack_country['up_bytes']/attack_country['flows_to_country']
# make the mean between the down_bytes of one country and the flows to that country
attack_country['down_bytes/flows'] = attack_country['down_bytes']/attack_country['flows_to_country']

# merge normal_country and attack_country and get the difference between % flows, up_bytes/flows and down_bytes/flows and get the ones that have a 99% increase and more than 100 flows
country_diff = pd.merge(normal_country, attack_country, on=['dst_country'], how='right')
#fill NaN with 0
country_diff = country_diff.fillna(0)

# remove the ones that have less than 100 flows_to_country_y or have a .99 increase between country_diff['flows_to_country_x'] and country_diff['flows_to_country_y'] or have a .5 increase between country_diff['up_bytes/flows_x'] and country_diff['up_bytes/flows_y'] or have a .5 increase between country_diff['down_bytes/flows_x'] and country_diff['down_bytes/flows_y']
country_diff = country_diff[((country_diff['flows_to_country_y'] > 100) & ((country_diff['flows_to_country_y'] > (country_diff['flows_to_country_x']*1.99)) | (country_diff['up_bytes/flows_y'] > (country_diff['up_bytes/flows_x']*1.5)) | (country_diff['down_bytes/flows_y'] > (country_diff['down_bytes/flows_x']*1.5))))]


# TIME STATISTICS

# ON DATA NORMAL
# get src_ip and its min timestamp and max timestamp
normal_time  = data_normal.groupby(['src_ip'])['timestamp'].agg(['min','max']).reset_index()

# get the mean min timestamp and max timestamp between all src_ip
mean_min_time = normal_time['min'].mean()
mean_max_time = normal_time['max'].mean()

# ON DATA ATTACK
start_work = 7
end_work = 22
# get the src_ip and its min timestamp and max timestamp
attack_time  = data_attack.groupby(['src_ip'])['timestamp'].agg(['min','max']).reset_index()
attack_time['min'] = attack_time['min'].apply(timestamp_to_hour)
attack_time['max'] = attack_time['max'].apply(timestamp_to_hour)

# keep the ones that min_time is before 7:00:00 or max_time is after 22:00:00
attack_time = attack_time[((attack_time['min'] < '07:00:00') | (attack_time['max'] > '22:00:00'))]

# get number of total flows from data_attack
attack_time['flows_anomaly'] = data_attack.groupby(['src_ip']).size().reset_index(name='flows')['flows']
# get number of total flows from data_normal
attack_time['flows_normal'] = data_normal.groupby(['src_ip']).size().reset_index(name='flows')['flows']
# get the % of increase of flows
attack_time['flows_rise'] = (attack_time['flows_anomaly'] - attack_time['flows_normal'])/attack_time['flows_normal']

# get number of total up_bytes from data_attack
attack_time['up_bytes_anomaly'] = data_attack.groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']
# get up_bytes per flow from data_attack
attack_time['up_bytes/flows_anomaly'] = attack_time['up_bytes_anomaly']/attack_time['flows_anomaly']
# get number of total up_bytes from data_normal
attack_time['up_bytes_normal'] = data_normal.groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']
# get up_bytes per flow from data_normal
attack_time['up_bytes/flows_normal'] = attack_time['up_bytes_normal']/attack_time['flows_normal']
# get the % of increase of up_bytes/flows
attack_time['up_bytes_rise'] = (attack_time['up_bytes/flows_anomaly'] - attack_time['up_bytes/flows_normal'])/attack_time['up_bytes/flows_normal']

# get number of total down_bytes from data_attack
attack_time['down_bytes_anomaly'] = data_attack.groupby(['src_ip'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']
# get down_bytes per flow from data_attack
attack_time['down_bytes/flows_anomaly'] = attack_time['down_bytes_anomaly']/attack_time['flows_anomaly']
# get number of total down_bytes from data_normal
attack_time['down_bytes_normal'] = data_normal.groupby(['src_ip'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']
# get down_bytes per flow from data_normal
attack_time['down_bytes/flows_normal'] = attack_time['down_bytes_normal']/attack_time['flows_normal']
# get the % of increase of down_bytes/flows
attack_time['down_bytes_rise'] = (attack_time['down_bytes/flows_anomaly'] - attack_time['down_bytes/flows_normal'])/attack_time['down_bytes/flows_normal']

# keep the ones with flows_rise > 100% or up_bytes_rise > 50% or down_bytes_rise > 50%
attack_time = attack_time[((attack_time['flows_rise'] > 1) | (attack_time['up_bytes_rise'] > 0.5) | (attack_time['down_bytes_rise'] > 0.5))]

# get all flows from ip 192.168.100.23 in data_attack
ip_192_168_107_104 = data_attack.loc[(data_attack['src_ip']=='192.168.107.227')]
# timestamp to hour
ip_192_168_107_104['timestamp'] = ip_192_168_107_104['timestamp'].apply(timestamp_to_hour)
# get org from dst_ip
ip_192_168_107_104['org'] = ip_192_168_107_104['dst_ip'].apply(lambda x: geo2.org_by_addr(x))
# get the down_bytes total of the ip
ip_192_168_107_104['down_bytes'] = ip_192_168_107_104.groupby(['src_ip'])['down_bytes'].transform('sum')
# get the up_bytes total of the ip
ip_192_168_107_104['up_bytes'] = ip_192_168_107_104.groupby(['src_ip'])['up_bytes'].transform('sum')
# get the down_bytes of org
ip_192_168_107_104['down_bytes_org'] = ip_192_168_107_104.groupby(['org'])['down_bytes'].transform('sum')
# get the up_bytes of org
ip_192_168_107_104['up_bytes_org'] = ip_192_168_107_104.groupby(['org'])['up_bytes'].transform('sum')

# get all flows from ip 192.168.100.59 in data_attack
ip_192_168_100_59 = data_attack.loc[(data_attack['src_ip']=='192.168.107.234')]
# timestamp to hour
ip_192_168_100_59['timestamp'] = ip_192_168_100_59['timestamp'].apply(timestamp_to_hour)
# get org from dst_ip
ip_192_168_100_59['org'] = ip_192_168_100_59['dst_ip'].apply(lambda x: geo2.org_by_addr(x))
# get the down_bytes total of the ip
ip_192_168_100_59['down_bytes'] = ip_192_168_100_59.groupby(['src_ip'])['down_bytes'].transform('sum')
# get the up_bytes total of the ip
ip_192_168_100_59['up_bytes'] = ip_192_168_100_59.groupby(['src_ip'])['up_bytes'].transform('sum')
# get the down_bytes of org
ip_192_168_100_59['down_bytes_org'] = ip_192_168_100_59.groupby(['org'])['down_bytes'].transform('sum')
# get the up_bytes of org
ip_192_168_100_59['up_bytes_org'] = ip_192_168_100_59.groupby(['org'])['up_bytes'].transform('sum')


# Let's analise only the data_normal

# get private ips with more traffic from data_normal both src_ip and dst_ip
server_ips_normal = data_normal.loc[((data_normal['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)))]
# get private ip 192.168.* as dst_ip with alot of traffic from data_normal and count the number of flows
servers_normal = server_ips_normal.loc[(server_ips_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (server_ips_normal['dst_ip'].apply(lambda x: x.startswith('192.168.')))].groupby(['dst_ip']).size().reset_index(name='counts')

# get the mean between all src_ip:
#   - flows 
#   - flows to internet
#   - flows to private ips
#   - flows to servers internal
#   - total up_bytes
#   - up_bytes_per_flow
#   - total down_bytes
#   - down_bytes_per_flow
#   - % of udp flows
#   - % of tcp flows
#   - up_bytes_per_tcp_flow
#   - up_bytes_per_udp_flow
#   - down_bytes_per_tcp_flow
#   - down_bytes_per_udp_flow


normal_stat = data_normal.groupby(['src_ip']).size().reset_index(name='flows')
normal_stat['flows_to_internet'] = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)==False)].groupby(['src_ip']).size().reset_index(name='flows_to_internet')['flows_to_internet']
normal_stat['flows_to_private_ips'] = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private))].groupby(['src_ip']).size().reset_index(name='flows_to_private_ips')['flows_to_private_ips']
normal_stat['flows_to_servers'] = data_normal.loc[(data_normal['dst_ip'].isin(servers_normal['dst_ip']))].groupby(['src_ip']).size().reset_index(name='flows_to_servers')['flows_to_servers']
normal_stat['total_up_bytes'] = data_normal.groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']
normal_stat['up_bytes_per_flow'] = data_normal.groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']/normal_stat['flows']
normal_stat['total_down_bytes'] = data_normal.groupby(['src_ip'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']
normal_stat['down_bytes_per_flow'] = data_normal.groupby(['src_ip'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']/normal_stat['flows']
normal_stat['% udp_flows'] = data_normal.loc[(data_normal['proto']=='udp')].groupby(['src_ip']).size().reset_index(name='udp_flows')['udp_flows']/normal_stat['flows']
normal_stat['% tcp_flows'] = data_normal.loc[(data_normal['proto']=='tcp')].groupby(['src_ip']).size().reset_index(name='tcp_flows')['tcp_flows']/normal_stat['flows']
normal_stat['up_bytes_per_tcp_flow'] = data_normal.loc[(data_normal['proto']=='tcp')].groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']/normal_stat['% tcp_flows']
normal_stat['up_bytes_per_udp_flow'] = data_normal.loc[(data_normal['proto']=='udp')].groupby(['src_ip'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']/normal_stat['% udp_flows']
normal_stat['down_bytes_per_tcp_flow'] = data_normal.loc[(data_normal['proto']=='tcp')].groupby(['src_ip'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']/normal_stat['% tcp_flows']
normal_stat['down_bytes_per_udp_flow'] = data_normal.loc[(data_normal['proto']=='udp')].groupby(['src_ip'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']/normal_stat['% udp_flows']

mean_flows = normal_stat['flows'].mean()
mean_flows_to_internet = normal_stat['flows_to_internet'].mean()
mean_flows_to_private_ips = normal_stat['flows_to_private_ips'].mean()
mean_flows_to_servers = normal_stat['flows_to_servers'].mean()
mean_total_up_bytes = normal_stat['total_up_bytes'].mean()
mean_up_bytes_per_flow = normal_stat['up_bytes_per_flow'].mean()
mean_total_down_bytes = normal_stat['total_down_bytes'].mean()
mean_down_bytes_per_flow = normal_stat['down_bytes_per_flow'].mean()
mean_perc_udp_flows = normal_stat['% udp_flows'].mean()
mean_perc_tcp_flows = normal_stat['% tcp_flows'].mean()
mean_up_bytes_per_tcp_flow = normal_stat['up_bytes_per_tcp_flow'].mean()
mean_up_bytes_per_udp_flow = normal_stat['up_bytes_per_udp_flow'].mean()
mean_down_bytes_per_tcp_flow = normal_stat['down_bytes_per_tcp_flow'].mean()
mean_down_bytes_per_udp_flow = normal_stat['down_bytes_per_udp_flow'].mean()



# stats for country
# - flows to country
# - up_bytes to country
# - down_bytes to country
# - up_bytes per flow to country
# - down_bytes per flow to country
normal_country_stat = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: not ipaddress.ip_address(x).is_private))].groupby(['dst_country']).size().reset_index(name='flows_to_country')
normal_country_stat['up_bytes_to_country'] = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: not ipaddress.ip_address(x).is_private))].groupby(['dst_country'])['up_bytes'].sum().reset_index(name='up_bytes')['up_bytes']
normal_country_stat['down_bytes_to_country'] = data_normal.loc[(data_normal['dst_ip'].apply(lambda x: not ipaddress.ip_address(x).is_private))].groupby(['dst_country'])['down_bytes'].sum().reset_index(name='down_bytes')['down_bytes']
normal_country_stat['up_bytes_per_flow_to_country'] = normal_country_stat['up_bytes_to_country']/normal_country_stat['flows_to_country']
normal_country_stat['down_bytes_per_flow_to_country'] = normal_country_stat['down_bytes_to_country']/normal_country_stat['flows_to_country']

# remove the countries that have less than 10 flows
normal_country_stat = normal_country_stat[(normal_country_stat['flows_to_country'] > 10)]

mean_flows_to_country = normal_country_stat['flows_to_country'].mean()
mean_up_bytes_to_country = normal_country_stat['up_bytes_to_country'].mean()
mean_down_bytes_to_country = normal_country_stat['down_bytes_to_country'].mean()
mean_up_bytes_per_flow_to_country = normal_country_stat['up_bytes_per_flow_to_country'].mean()
mean_down_bytes_per_flow_to_country = normal_country_stat['down_bytes_per_flow_to_country'].mean()


#make a plot bar with ONLY the variables mean flows, mean flows to internet, mean flows to private ips
flows_plot = pd.DataFrame({'mean_flows': [mean_flows], 'mean_flows_to_internet': [mean_flows_to_internet], 'mean_flows_to_private_ips': [mean_flows_to_private_ips]})
flows_plot.plot.bar(figsize=(20,10), title='Mean Flows to Internet', rot=0)
# rename y to Flows
plt.ylabel('Flows')
# rename legend to Mean Flows, Mean Flows to Internet and Mean Flows to Private IPs
plt.legend(['Mean Flows', 'Mean Flows to Internet', 'Mean Flows to Private IPs'])
# add percentage to the top of each bar, mean flows is 100%, mean flows to internet is mean_flows_to_internet/mean_flows and mean flows to private ips is mean_flows_to_private_ips/mean_flows
plt.annotate(str(round(mean_flows_to_internet/mean_flows*100,2))+'%', xy=(0.475, 0.5), xycoords='axes fraction', fontsize=16)
plt.annotate(str(round(mean_flows_to_private_ips/mean_flows*100,2))+'%', xy=(0.65, 0.20), xycoords='axes fraction', fontsize=16)
# save figure as png
plt.savefig('images/mean_flows.png')
plt.show()
plt.close()

#make a plot bar with ONLY the variables % udp flows and % tcp flows
flows_plot = pd.DataFrame({'mean_perc_udp_flows': [mean_perc_udp_flows], 'mean_perc_tcp_flows': [mean_perc_tcp_flows]})
flows_plot.plot.bar(figsize=(20,10), title='Mean (%) of UDP and TCP Flows', rot=0)
# rename x axis to Mean UDP and TCP Flows and y to % 
plt.ylabel('% of Flows')
plt.xlabel('UDP and TCP Flows')
# rename legend to Mean % of UDP Flows and Mean % of TCP Flows
plt.legend(['Mean % of UDP Flows', 'Mean % of TCP Flows'])
# add percentage to the top of each bar, mean % of udp flows is mean_perc_udp_flows*100 and mean % of tcp flows is mean_perc_tcp_flows*100
plt.annotate(str(round(mean_perc_udp_flows*100,2))+'%', xy=(0.35, 0.05), xycoords='axes fraction', fontsize=16)
plt.annotate(str(round(mean_perc_tcp_flows*100,2))+'%', xy=(0.6, 0.5), xycoords='axes fraction', fontsize=16)
# save figure as png
plt.savefig('images/mean_perc_udp_tcp_flows.png')
plt.show()
plt.close()

#make a plot bar with ONLY the variables mean up_bytes per tcp flow and mean down_bytes per tcp flow, and mean up_bytes per udp flow and mean down_bytes per udp flow
flows_plot = pd.DataFrame({'mean_up_bytes_per_tcp_flow': [mean_up_bytes_per_tcp_flow], 'mean_down_bytes_per_tcp_flow': [mean_down_bytes_per_tcp_flow], 'mean_up_bytes_per_udp_flow': [mean_up_bytes_per_udp_flow], 'mean_down_bytes_per_udp_flow': [mean_down_bytes_per_udp_flow]})
flows_plot.plot.bar(figsize=(20,10), title='Mean Bytes - TCP and UDP Flows', rot=0)
# rename y to Bytes
plt.ylabel('Bytes')
# rename legend to Mean Uploaded Bytes per TCP Flow, Mean Downloaded Bytes per TCP Flow, Mean Uploaded Bytes per UDP Flow and Mean Downloaded Bytes per UDP Flow
plt.legend(['Mean Up Bytes per TCP Flow', 'Mean Down Bytes per TCP Flow', 'Mean Up Bytes per UDP Flow', 'Mean Down Bytes per UDP Flow'])
# save figure as png
plt.savefig('images/mean_bytes.png')
plt.show()
plt.close()
# calculate as var the rise between mean up_bytes per tcp flow and mean down_bytes per tcp flow in percentage
var_up_down_bytes_per_tcp_flow = abs((mean_up_bytes_per_tcp_flow - mean_down_bytes_per_tcp_flow)/mean_down_bytes_per_tcp_flow) * 100
# calculate as var the rise between mean up_bytes per udp flow and mean down_bytes per udp flow in percentage
var_up_down_bytes_per_udp_flow = abs((mean_up_bytes_per_udp_flow - mean_down_bytes_per_udp_flow)/mean_down_bytes_per_udp_flow) * 100

# make a plot with the country up_bytes per flow and with a line with the mean up_bytes per flow 
country_plot = normal_country_stat[['dst_country','up_bytes_per_flow_to_country']]
country_plot = country_plot.set_index('dst_country')
country_plot.plot.bar(figsize=(30,10), title='Uploaded Bytes - Flow to Country', rot=0)
# rename x axis to Countries and y to Bytes
plt.ylabel('Bytes')
plt.xlabel('Countries')
plt.xticks(rotation=45)
# add a line with the mean up_bytes per flow
plt.axhline(y=mean_up_bytes_per_flow_to_country, color='r', linestyle='-')
# save figure as png
plt.savefig('images/up_bytes_per_flow_to_country.png')
plt.show()
plt.close()

# make a plot with the country down_bytes per flow and with a line with the mean down_bytes per flow
country_plot = normal_country_stat[['dst_country','down_bytes_per_flow_to_country']]
country_plot = country_plot.set_index('dst_country')
country_plot.plot.bar(figsize=(30,10), title='Downloaded Bytes - Flow to Country', rot=0)
# rename x axis to Countries and y to Bytes
plt.ylabel('Bytes')
plt.xlabel('Countries')
# make x values appear 45 degrees
plt.xticks(rotation=45)
# add a line with the mean down_bytes per flow
plt.axhline(y=mean_down_bytes_per_flow_to_country, color='r', linestyle='-')
# save figure as png
plt.savefig('images/down_bytes_per_flow_to_country.png')
plt.show()
plt.close()

# make a plot with flows to country and with a line with the mean flows to country
country_plot = normal_country_stat[['dst_country','flows_to_country']]
country_plot = country_plot.set_index('dst_country')
country_plot.plot.bar(figsize=(30,10), title='Flows to Country', rot=0)
# rename x axis to Countries and y to Flows
plt.ylabel('Flows')
plt.xlabel('Countries')
# make x values appear 45 degrees
plt.xticks(rotation=45)
# add a line with the mean flows to country
plt.axhline(y=mean_flows_to_country, color='r', linestyle='-')
# save figure as png
plt.savefig('images/flows_to_country.png')
plt.show()
plt.close()

