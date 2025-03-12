import pandas as pd
import ipaddress
import dns.resolver
import dns.reversename
import pygeoip
import matplotlib.pyplot as plt

# Dados
data_normal = pd.read_parquet('data4.parquet')
data_attack = pd.read_parquet('test4.parquet')


# Obter o nome da organização para um endereço IP
geo1 = pygeoip.GeoIP('GeoIP.dat')
geo2 = pygeoip.GeoIP('GeoIPASNum.dat')

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

print("PASSOU")
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

# Obter IPs privados 192.168.100.* como dst_ip com muito tráfego de data_normal e contar o número de fluxos
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

print(download_attack)

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

# plot up_bytes_normal vs up_bytes_attack in a bar plot
# just for the ips in up_bytes_stat
up_bytes_stat_plot = pd.merge(up_bytes_normal, up_bytes_attack, on=['src_ip'], how='inner')
up_bytes_stat_plot = up_bytes_stat_plot[up_bytes_stat_plot['src_ip'].isin(up_bytes_stat['src_ip'])]
up_bytes_stat_plot = up_bytes_stat_plot[['src_ip','up/flows_x','up/flows_y']]
up_bytes_stat_plot = up_bytes_stat_plot.set_index('src_ip')
# change legend names
up_bytes_stat_plot = up_bytes_stat_plot.rename(columns={'up/flows_x': 'uploaded normal flows', 'up/flows_y': 'uploaded attack flows'})
up_bytes_stat_plot.plot.bar(figsize=(20,10), title='Uploaded Bytes per Flow', rot=0)
# rename x axis to Suspect IPs and y to Bytes
plt.ylabel('Bytes')
plt.xlabel('Suspect IPs')
# save figure as png
plt.savefig('images/script_3_up_bytes.png')
plt.close()



# plot the how much bytes was tranmitted with ips in up_bytes_stat
up_bytes_stat_plot = up_bytes_stat[['src_ip','up_exfiltration']]
up_bytes_stat_plot = up_bytes_stat_plot.set_index('src_ip')
up_bytes_stat_plot.plot.bar(figsize=(20,10), title='Uploaded Bytes to Public IPs', rot=0)
# save figure as png
# rename x axis to Suspect IPs and y to Bytes
plt.ylabel('Bytes')
plt.xlabel('Suspect IPs')
plt.savefig('images/script_3_up_bytes_exfiltration.png')
plt.close()

exfiltration_stat
# save exfiltration_stat to csv
exfiltration_stat.to_csv('images/script_3_exfiltration_stat.csv', index=False)


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

# make a bar plot with the difference between  all x and y for all columns less flows_to_country_*
country_diff_plot = country_diff[['dst_country','up_bytes/flows_x','up_bytes/flows_y','down_bytes/flows_x','down_bytes/flows_y']]
country_diff_plot = country_diff_plot.set_index('dst_country')
country_diff_plot.plot.bar(figsize=(20,10), title='Difference between normal and attack data bytes and flows', rot=0)
# rename up_bytes/flows_x and up_bytes/flows_y to Uploaded Bytes per Flow in normal and attack data
# rename down_bytes/flows_x and down_bytes/flows_y to Downloaded Bytes per Flow in normal and attack data
plt.legend(['Uploaded Bytes per Flow in normal data', 'Uploaded Bytes per Flow in attack data', 'Downloaded Bytes per Flow in normal data', 'Downloaded Bytes per Flow in attack data'])
# rename x axis to Countries and y to Bytes
plt.ylabel('Bytes')
plt.xlabel('Countries')
# save figure as png
plt.savefig('images/script_3_country_diff_stats.png')
plt.show()
plt.close()

# make a bar plot with the difference between  flows_to_country_x and flows_to_country_y
country_diff_plot = country_diff[['dst_country','flows_to_country_x','flows_to_country_y']]
# divide flows_to_country_x and flows_to_country_y of usa by 100
country_diff_plot.loc[country_diff_plot['dst_country'] == 'United States', ['flows_to_country_x','flows_to_country_y']] = country_diff_plot.loc[country_diff_plot['dst_country'] == 'United States', ['flows_to_country_x','flows_to_country_y']]/100
country_diff_plot = country_diff_plot.set_index('dst_country')
country_diff_plot.plot.bar(figsize=(20,10), title='Difference between normal and attack data flows', rot=0)
# add note to usa bar, make it appear top left corner
plt.annotate('Flows to USA are divided by 100', xy=(0.01, 0.85), xycoords='axes fraction', fontsize=16)
# rename flows_to_country_x and flows_to_country_y to Flows in normal and attack data
plt.legend(['Flows in normal data', 'Flows in attack data'])
# rename x axis to Countries and y to Flows
plt.ylabel('Flows')
plt.xlabel('Countries')
# save figure as png
plt.savefig('images/script_3_country_diff_flows.png')
plt.show()
plt.close()



