from uptime_kuma_api import UptimeKumaApi
api = UptimeKumaApi("http://0.0.0.0:3001")
api.login("user", "pass")


tag = api.add_tag(
    name="Development", 
    color="#2b6f9c" 
)

monitor = api.add_monitor(
    type="http",
    name="VM-001",
    url="https://n8n.enterprise.com.",
    interval=60,
    retryInterval=60,
    resendInterval=0,
    maxretries=1,
    notificationIDList=[],
    expiryNotification = True,
    description='N8N environment',
    dns_resolve_server="10.200.0.2",
    dns_resolve_type="A",
    ignoreTls=False,
    upsideDown=False,
    method="GET",
    httpBodyEncoding="json",
)


id = monitor['monitorID']
api.add_monitor_tag(
    tag_id=tag['id'],
    monitor_id=id,
    value="GSeeds"
)



api.disconnect()