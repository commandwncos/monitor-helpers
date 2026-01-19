import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.privatedns import PrivateDnsManagementClient

def list_all_dns_data():
    credential = DefaultAzureCredential()
    sub_client = SubscriptionClient(credential)
    
    results = []

    # Itera por todas as subscrições disponíveis
    for sub in sub_client.subscriptions.list():
        sub_id = sub.subscription_id
        
        # Cliente para DNS Público
        dns_client = DnsManagementClient(credential, sub_id)
        # Cliente para DNS Privado
        private_dns_client = PrivateDnsManagementClient(credential, sub_id)

        # 1. Processamento de Zonas Públicas
        try:
            for zone in dns_client.zones.list():
                zone_data = {
                    "name": zone.name,
                    "resourceGroup": zone.id.split('/')[4],
                    "subscription": sub_id,
                    "zoneType": "Public",
                    "records": []
                }
                
                # Lista todos os record sets da zona pública
                record_sets = dns_client.record_sets.list_all_by_dns_zone(zone_data["resourceGroup"], zone.name)
                for rs in record_sets:
                    # Converte o objeto do SDK para um dicionário serializável
                    zone_data["records"].append(rs.as_dict())
                
                results.append(zone_data)
        except Exception:
            pass # Ignora subscrições sem permissão ou sem o provedor registado

        # 2. Processamento de Zonas Privadas
        try:
            for p_zone in private_dns_client.private_zones.list():
                p_zone_data = {
                    "name": p_zone.name,
                    "resourceGroup": p_zone.id.split('/')[4],
                    "subscription": sub_id,
                    "zoneType": "Private",
                    "records": []
                }
                
                # Lista todos os record sets da zona privada
                p_record_sets = private_dns_client.record_sets.list(p_zone_data["resourceGroup"], p_zone.name)
                for prs in p_record_sets:
                    p_zone_data["records"].append(prs.as_dict())
                
                results.append(p_zone_data)
        except Exception:
            pass

    # Guarda o resultado final num ficheiro JSON
    with open('dns_zones.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    list_all_dns_data()