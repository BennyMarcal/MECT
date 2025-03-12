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


# Verificar se servers_attack está vazio antes de fazer gráfico
if servers_attack.empty:
    print("Erro: servers_attack está vazio após o merge.")
else:
    # Fazer um gráfico com a diferença entre servers_normal e servers_attack
    
    servers_attack.plot(x='dst_ip', y=['counts_x', 'counts_y'], kind='bar', figsize=(20, 10), title='Flows per server - Normal and Attack Data')
    plt.xlabel('Servers IP')
    plt.legend(['Number of flows to servers in normal data', 'Number of flows to servers in attack data'])
    plt.savefig('images/script_1_server_flows.png')
    plt.show()
    
    