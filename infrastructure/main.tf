terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.57.0"
    }
  }

  # remember to use:
  # export ARM_ACCESS_KEY="F6Xq1...+RWH7+AStiFwNhw==" 

  backend "azurerm" {
    resource_group_name  = "" # example RG created by main.azcli
    storage_account_name = "tfstate1d7c07"
    container_name       = "terraformstate"
    key                  = "terraform.tfstate"
  }

}

provider "azurerm" {
  features {}
  subscription_id = "l"
}


