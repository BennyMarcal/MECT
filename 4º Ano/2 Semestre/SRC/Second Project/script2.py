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


# Verificar se servers_attack está vazio antes de fazer gráfico
if ips_to_servers_attack.empty:
    print("Erro: ips_to_servers_attack está vazio após o merge.")
else:
    # Fazer um gráfico com a diferença entre servers_normal e servers_attack
    
    # make bar plot with the count of flows to servers in normal and attack data
    ips_to_servers_attack.plot(x='src_ip', y=['counts_x', 'counts_y'], kind='bar', figsize=(20,10), title='Number of Flows to servers - Normal and Attack data')   
    plt.xlabel('IPs that have 2 times more flows to servers in attack data')
    plt.legend(['Number of flows to servers - Normal data', 'Number of flows to servers - Attack data'])
    plt.savefig('images/script_2_ips_to_servers.png')
    plt.show()
    
    
#FAZER O CSV
# keep the ones with rise > 5
ips_to_servers_attack = ips_to_servers_attack[ips_to_servers_attack['rise'] > 9.99]

# get the timeline for these ips in attack data
ips_to_servers_attack = data_attack.loc[(data_attack['src_ip'].isin(ips_to_servers_attack['src_ip']))]
# apply timestamp_to_hour to timestamp column
ips_to_servers_attack['timestamp'] = ips_to_servers_attack['timestamp'].apply(timestamp_to_hour)

# keep the first 30 rows with src_ip 192.168.100.176
ips_199 = ips_to_servers_attack.loc[(ips_to_servers_attack['src_ip'] == '192.168.104.199')]
ips_199 = ips_199.head(30)
# remove index
ips_199 = ips_199.reset_index(drop=True)
# save ips_to_servers_attack to csv
ips_199.to_csv('images/script_2_csvtable.csv', index=False)
ips_199