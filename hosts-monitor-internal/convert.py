import json

def convert_dns_to_kuma():
    try:
        # 1. Carrega o arquivo gerado pelo script da Azure
        with open('dns_zones.json', 'r', encoding='utf-8') as f:
            azure_data = json.load(f)
        
        kuma_monitors = []

        for zone in azure_data:
            zone_name = zone.get("name")
            
            for record in zone.get("records", []):
                # O FQDN (Full Qualified Domain Name) na Azure geralmente vem no campo 'fqdn'
                fqdn = record.get("fqdn")
                if not fqdn:
                    continue
                
                # Remove o ponto final do FQDN se existir (comum em DNS)
                fqdn = fqdn.rstrip('.')
                
                # Definimos o tipo de resolução DNS com base no registro
                # No seu caso, você pediu fixo "A", mas podemos identificar do registro
                record_type = record.get("type", "").split('/')[-1] # Ex: Microsoft.Network/dnszones/A -> A
                
                # Montamos o objeto para o Uptime Kuma
                monitor = {
                    "type": "http",
                    "name": fqdn, # Usando o FQDN como nome para facilitar identificação
                    "url": f"https://{fqdn}", # Converte para URL
                    "interval": 60,
                    "retryInterval": 60,
                    "resendInterval": 0,
                    "maxretries": 1,
                    "notificationIDList": [],
                    "expiryNotification": True,
                    "description": f"Importado da Zona {zone_name} ({zone.get('zoneType')})",
                    "dns_resolve_server": "10.200.32.32",
                    "dns_resolve_type": "A",
                    "ignoreTls": False,
                    "upsideDown": False,
                    "method": "GET",
                    "httpBodyEncoding": "json",
                    "conditions": [] # Adicionado para garantir compatibilidade com MariaDB
                }
                
                # Filtro opcional: apenas adicionar registros de interesse (A, CNAME)
                # Se quiser importar TUDO, remova este IF
                if record_type in ['A', 'CNAME']:
                    kuma_monitors.append(monitor)

        # 2. Salva o novo JSON formatado para o Uptime Kuma
        with open('zones.json', 'w', encoding='utf-8') as f:
            json.dump(kuma_monitors, f, indent=4)
            
        print(f"✅ Sucesso! {len(kuma_monitors)} monitores gerados em zones.json")

    except FileNotFoundError:
        print("❌ Erro: O arquivo dns_zones.json não foi encontrado.")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    convert_dns_to_kuma()