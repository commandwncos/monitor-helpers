
# 🏗️ Infrastructure as Code – Azure + Terraform + Docker

Este repositório contém a **infraestrutura completa** para provisionar uma VM no Azure, configurar **remote state do Terraform**, e executar uma stack Docker com **Nginx + Uptime Kuma + Certificados SSL**.

A infraestrutura segue boas práticas de:

* Segurança
* Separação de responsabilidades
* Automação
* Não versionamento de segredos

---

## 📁 Estrutura do Projeto

```text
.
├── infrastructure
│   ├── containers
│   │   ├── compose.yaml
│   │   └── nginx
│   │       ├── certs
│   │       └── conf.d
│   │           └── uptime-kuma.conf
│   ├── default.tf
│   └── main.tf
└── main.azcli
```

---

# 🚀 ETAPA ZERO — Bootstrap da Infraestrutura Azure (OBRIGATÓRIA)

> ⚠️ **Essa etapa deve ser executada antes de qualquer comando Terraform**

A Etapa Zero é responsável por **criar os recursos base** que o Terraform precisa para funcionar corretamente com **remote state** no Azure.

### 🎯 O que essa etapa cria

O script `main.azcli` cria automaticamente:

* ✅ Resource Group dedicado
* ✅ Storage Account
* ✅ Blob Container para o Terraform State
* ✅ Key Vault
* ✅ Armazena segredos sensíveis no Key Vault:

  * Access Key do Storage Account
  * Connection String do Storage Account

Esses recursos **NÃO são gerenciados pelo Terraform**, pois o próprio Terraform depende deles.

---

## 📜 Arquivo: `main.azcli`

### 🔹 Objetivo

Provisionar o **backend remoto do Terraform** de forma segura.

### 🔹 Tecnologias usadas

* Azure CLI
* Azure Storage
* Azure Key Vault
* Azure RBAC

---

### 🧠 Fluxo do Script

1. Gera nomes únicos (UUID + random hash)
2. Cria Resource Group
3. Registra providers necessários
4. Cria Storage Account
5. Cria Container Blob (`terraformstate`)
6. Cria Key Vault
7. Concede permissão ao usuário atual
8. Salva segredos no Key Vault
9. Exibe informações finais

---

### ▶️ Como executar a Etapa Zero

#### Pré-requisitos

```bash
az login
az account set --subscription <SUBSCRIPTION_ID>
```

#### Executar

```bash
chmod +x main.azcli
./main.azcli
```

---

### 📤 Saída esperada

```text
Resource Group: RG-XXXX
Storage Account: tfstateXXXX
Container: terraformstate
Key Vault: kv-tfXXXX
Secrets: tfstate-key, tfstate-connectionstring
```

> 🔐 **Esses valores não devem ser commitados no Git**

---

## 🔐 Segurança (IMPORTANTE)

* ❌ Nenhuma chave é armazenada no código
* ❌ Nenhum segredo é versionado
* ✅ Terraform consome segredos via Key Vault
* ✅ Controle de acesso via RBAC

---

# 🧱 ETAPA UM — Terraform (Infrastructure Provisioning)

Após a Etapa Zero:

* O Terraform usa o **Storage Account** como backend remoto
* O estado (`terraform.tfstate`) fica **centralizado e seguro**
* A infraestrutura provisionada inclui:

  * Virtual Network
  * Subnet
  * NSG
  * Public IP
  * Network Interface
  * Virtual Machine Linux

Arquivos principais:

* `infrastructure/main.tf`
* `infrastructure/default.tf`

---

## ▶️ Inicializar Terraform

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

---

# 🐳 ETAPA DOIS — Containers (Docker + Nginx + Uptime Kuma)

Após a VM estar disponível:

1. Conectar via SSH
2. Instalar Docker
3. Subir stack com Docker Compose

Diretório:

```text
infrastructure/containers/
```

Componentes:

* **Uptime Kuma** → monitoramento
* **Nginx** → reverse proxy
* **Certificados SSL** → Let’s Encrypt ou autoassinado

---

# 🔐 Certificados SSL

### Ambientes

| Ambiente  | Método                  |
| --------- | ----------------------- |
| Local     | Autoassinado            |
| Produção  | Let’s Encrypt (Certbot) |
| Azure DNS | DNS-01 (recomendado)    |

> Certificados **não são versionados** e são gerados **em runtime**.

---

# 🧹 O que NÃO vai para o GitHub

* `terraform.tfvars`
* `*.tfstate`
* Certificados SSL
* Volumes Docker
* Chaves privadas

---

# 📌 Boas Práticas Aplicadas

* Infra declarativa
* Remote state
* Zero secrets no Git
* Containers desacoplados
* TLS obrigatório
* Infra reprodutível

---

# 🧭 Próximos Passos (Opcional)

* 🔄 Automatizar Certbot no Docker Compose
* 🔁 Migrar para Traefik
* 🔐 Integrar com Azure DNS (DNS-01)
* 📈 Monitorar a própria VM com Uptime Kuma
* 🚀 CI/CD com GitHub Actions

---

## ✅ Conclusão

Este projeto fornece uma base **segura, escalável e profissional** para executar workloads Docker em Azure usando Terraform e boas práticas de segurança.


