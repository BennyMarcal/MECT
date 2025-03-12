import pandas as pd
import ipaddress
import pygeoip
import matplotlib.pyplot as plt

# Carregar os dados
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

# Adicionar a coluna de país
data_normal['dst_country'] = data_normal['dst_ip'].apply(get_countryname)
data_attack['dst_country'] = data_attack['dst_ip'].apply(get_countryname)

print("PASSOU")

def timestamp_to_hour(timestamp):
    timestamp = timestamp / 100
    hours, remainder = divmod(timestamp, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

# Filtrar IPs privados
server_ips_normal = data_normal.loc[((data_normal['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_normal['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)))]

# Obter IPs privados 192.168.*.* como dst_ip com muito tráfego de data_normal e contar o número de fluxos
servers_normal = server_ips_normal.loc[(server_ips_normal['dst_ip'].apply(lambda x: x.startswith('192.168.')))].groupby(['dst_ip']).size().reset_index(name='counts')

# Calcular a média de acessos aos servidores no conjunto de dados normal
avg_server_access = server_ips_normal.groupby(['src_ip']).size().reset_index(name='counts')['counts'].mean()
print("Average server IPs access: \n" + str(int(avg_server_access)))

# Verificar os acessos no conjunto de dados de ataque
server_ips_attack = data_attack.loc[((data_attack['src_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)) & (data_attack['dst_ip'].apply(lambda x: ipaddress.ip_address(x).is_private)))]
test_server_access = server_ips_attack.groupby(['src_ip']).size().reset_index(name='counts')
test_server_access = test_server_access[test_server_access['counts'] > (avg_server_access * 3)]

print("Test server IPs access: \n" + str(test_server_access))
