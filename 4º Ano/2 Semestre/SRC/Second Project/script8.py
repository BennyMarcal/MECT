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

# Verificar a existência da coluna 'proto' e valores únicos
print("Unique values in 'proto' column for normal data:", data_normal['proto'].unique())
print("Unique values in 'proto' column for attack data:", data_attack['proto'].unique())

# Calcular a média dos fluxos TCP no conjunto de dados normal
if 'proto' in data_normal.columns and 'proto' in data_attack.columns:
    data_normal_tcp = data_normal[data_normal['proto'] == 'tcp']
    
    if not data_normal_tcp.empty:
        mean_tcp_flows = data_normal_tcp.groupby('dst_ip').size().mean()
        print(f"mean of tcp_flows: {mean_tcp_flows}")
    else:
        print("No TCP flows in normal data.")

    # Agrupar os fluxos no conjunto de dados de ataque por src_ip
    flows = data_attack.groupby('src_ip').size().reset_index(name='flows')

    # Filtrar para fluxos TCP no conjunto de dados de ataque
    data_attack_tcp = data_attack[data_attack['proto'] == 'tcp']
    tcp_flows = data_attack_tcp.groupby('src_ip').size().reset_index(name='tcp')

    # Combinar as informações em uma única tabela
    merged_flows = pd.merge(flows, tcp_flows, on='src_ip', how='left')
    merged_flows['tcp'] = merged_flows['tcp'].fillna(0)

    # Renomear a coluna 'tcp' para 'tcp_flows'
    merged_flows = merged_flows.rename(columns={'tcp': 'tcp_flows'})

    # Adicionar a coluna numberofflows (que é igual a flows aqui)
    merged_flows['numberofflows'] = merged_flows['flows']

    # Exibir a tabela
    print(merged_flows)
else:
    print("The 'proto' column does not exist in the datasets.")
