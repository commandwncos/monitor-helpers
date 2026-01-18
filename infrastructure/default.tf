# ---------------------------
# Variables
# ---------------------------
variable "location" {
  default = "eastus2"
}

variable "my_ip" {
  description = "Your public IP for SSH access (ex: 1.2.3.4/32)"
  type        = string
}

variable "ssh_public_key_path" {
  description = "Path to your SSH public key"
  type        = string
}

# ---------------------------
# Resource Group
# ---------------------------
resource "azurerm_resource_group" "rg" {
  name     = upper("rg-${uuid()}")
  location = var.location
}

# ---------------------------
# Virtual Network + Subnet
# ---------------------------
resource "random_id" "vnet" {
  byte_length = 2
}

resource "random_id" "subnet" {
  byte_length = 2
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-${random_id.vnet.hex}"
  address_space       = ["10.0.0.0/24"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "subnet-${random_id.subnet.hex}"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.0.0/27"]
}

# ---------------------------
# Public IP
# ---------------------------
resource "random_id" "pip" {
  byte_length = 2
}

resource "azurerm_public_ip" "public_ip" {
  name                = "pip-${random_id.pip.hex}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# ---------------------------
# Network Security Group
# ---------------------------
resource "random_id" "nsg" {
  byte_length = 2
}

resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-${random_id.nsg.hex}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "ssh" {
  name                        = "Allow-SSH"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = var.my_ip
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.nsg.name
}

resource "azurerm_network_security_rule" "https" {
  name                        = "Allow-HTTPS"
  priority                    = 110
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.nsg.name
}

# ---------------------------
# Network Interface
# ---------------------------
resource "random_id" "nic" {
  byte_length = 2
}

resource "azurerm_network_interface" "nic" {
  name                = "nic-${random_id.nic.hex}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

resource "azurerm_network_interface_security_group_association" "nic_nsg" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# ---------------------------
# Virtual Machine (Ubuntu)
# ---------------------------
resource "random_id" "vm" {
  byte_length = 2
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                = "vm-${random_id.vm.hex}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_D2s_v3"
  admin_username      = "azureuser"

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  admin_ssh_key {
    username   = "azureuser"
    public_key = file(var.ssh_public_key_path)
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16_04-lts-gen2"
    version   = "latest"
  }
}

# ---------------------------
# Outputs
# ---------------------------
output "resource_group" {
  value = azurerm_resource_group.rg.name
}

output "vm_public_ip" {
  value = azurerm_public_ip.public_ip.ip_address
}

output "vm_username" {
  value = "azureuser"
}

output "subnet_id" {
  value = azurerm_subnet.subnet.id
}

output "nsg_id" {
  value = azurerm_network_security_group.nsg.id
}
