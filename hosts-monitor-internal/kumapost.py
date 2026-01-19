import json
from uptime_kuma_api import UptimeKumaApi
from time import sleep

def main():
    # 1. Conexão com a API
    api = UptimeKumaApi("http://0.0.0.0:3001")
    api.login("user", "pass")
    print("✅ Conectado ao Uptime Kuma!")

    # 2. Garantir que a Tag existe ou criá-la
    try:
        tag = api.add_tag(name="Development", color="#2b6f9c")
        print(f"🏷️ Tag '{tag['name']}' preparada.")
    except Exception:
        # Se a tag já existir, buscamos a lista para pegar o ID
        tags = api.get_tags()
        tag = next((t for t in tags if t['name'] == "Development"), None)

    # 3. Ler o arquivo zones.json gerado anteriormente
    try:
        with open('zones.json', 'r', encoding='utf-8') as f:
            monitors_to_add = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo zones.json não encontrado. Rode o conversor primeiro.")
        return

    print(f"📦 Iniciando importação de {len(monitors_to_add)} monitores...")

    # 4. Loop para preencher campo a campo
    for m_data in monitors_to_add:
        sleep(5)
        try:
            # Adiciona o monitor com todos os campos técnicos necessários
            monitor = api.add_monitor(
                type=m_data["type"],
                name=m_data["name"],
                url=m_data["url"],
                interval=m_data["interval"],
                retryInterval=m_data["retryInterval"],
                resendInterval=m_data["resendInterval"],
                maxretries=m_data["maxretries"],
                notificationIDList=m_data["notificationIDList"],
                expiryNotification=m_data["expiryNotification"],
                description=m_data["description"],
                dns_resolve_server=m_data["dns_resolve_server"],
                dns_resolve_type=m_data["dns_resolve_type"],
                ignoreTls=m_data["ignoreTls"],
                upsideDown=m_data["upsideDown"],
                method=m_data["method"],
                httpBodyEncoding=m_data["httpBodyEncoding"]
            )

            # Vincula a Tag ao monitor recém-criado
            api.add_monitor_tag(
                tag_id=tag['id'],
                monitor_id=monitor['monitorID'],
                value="GSeeds"
            )
            print(f"🚀 Sucesso: {m_data['name']} (ID: {monitor['monitorID']})")

        except Exception as e:
            print(f"⚠️ Falha ao importar {m_data['name']}: {str(e)}")

    # 5. Finalização
    api.disconnect()
    print("🏁 Processo concluído. Verifique o painel do Uptime Kuma.")

if __name__ == "__main__":
    main()