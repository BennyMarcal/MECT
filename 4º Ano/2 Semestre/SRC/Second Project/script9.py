import pandas as pd
import pygeoip
import ipaddress

# Carregar os dados
data_normal = pd.read_parquet('data4.parquet')
data_attack = pd.read_parquet('test4.parquet')

# Obter o nome da organização para um endereço IP
geo1 = pygeoip.GeoIP('GeoIP.dat')
geo2 = pygeoip.GeoIP('GeoIPASNum.dat')

def get_countryname(ip):
    try:
        return geo1.country_name_by_addr(ip)
    except:
        return 'Unknown'

# Função para rotular IPs internos
def label_internal(ip):
    try:
        ip_addr = ipaddress.ip_address(ip)
        if ip_addr.is_private:
            return 'Internal'
        else:
            return get_countryname(ip)
    except ValueError:
        return 'Invalid IP'

# Adicionar a coluna de país
data_normal['dst_country'] = data_normal['dst_ip'].apply(label_internal)
data_attack['dst_country'] = data_attack['dst_ip'].apply(label_internal)

print("PASSOU")

# Cálculo da média de fluxos por país no conjunto de dados normal
avg_flows_country = data_normal.loc[~data_normal['dst_ip'].str.startswith('192.168.104.')].groupby(['dst_country']).size().reset_index(name='avg_flows_country')

# Agrupar os fluxos no conjunto de dados de ataque por src_ip e dst_country
test_flows_country = data_attack.loc[~data_attack['dst_ip'].str.startswith('192.168.104.')].groupby(['src_ip', 'dst_country']).size().reset_index(name='flows_country')

# Combinar as informações em uma única tabela
result = pd.merge(test_flows_country, avg_flows_country, on='dst_country', how='left')

# Preencher NaN com 0 (opcional, dependendo do que você deseja fazer com países sem média de fluxo)
result['avg_flows_country'] = result['avg_flows_country'].fillna(0)

# Bloquear IPs que se comunicam com a Federação Russa
blocked_ips = result[result['dst_country'] == 'Russian Federation']['src_ip'].unique()
print("Source IPs that communicate with Russian Federation: BLOCKED")
for ip in blocked_ips:
    print(ip)

# Alertar sobre IPs que se comunicam com países que não estão no conjunto de dados normal
normal_countries = avg_flows_country['dst_country'].unique()
alert_ips = result[~result['dst_country'].isin(normal_countries)]['src_ip'].unique()
print("\nSource IPs that communicate with a country that is not in normal data: ALERT")
for ip in alert_ips:
    print(ip)

# Identificar IPs com mais de 4x o número médio de fluxos e flows_country > 100
suspicious_ips = result[(result['flows_country'] > 4 * result['avg_flows_country']) & (result['flows_country'] > 100)]
print("\nSource IPs that communicate with a country but have 4x more flows than the average to that country and flows_country > 100:")
print(suspicious_ips[['dst_country', 'avg_flows_country', 'src_ip', 'flows_country']])
