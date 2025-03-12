#DONE 4.4
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

# Filtrar os dados para incluir apenas registros onde dst_country é 'Internal'
internal_data_normal = data_normal[data_normal['dst_country'] == 'Internal']
internal_data_attack = data_attack[data_attack['dst_country'] == 'Internal']

# Selecionar apenas as colunas desejadas
filtered_data_normal = internal_data_normal[['src_ip', 'dst_ip', 'dst_country']]
filtered_data_attack = internal_data_attack[['src_ip', 'dst_ip', 'dst_country']]

# Remover duplicatas para garantir que cada src_ip apareça apenas uma vez
filtered_data_normal = filtered_data_normal.drop_duplicates(subset=['src_ip'])
filtered_data_attack = filtered_data_attack.drop_duplicates(subset=['src_ip'])

# Exibir os dados filtrados
print(filtered_data_normal)
print(filtered_data_attack)
