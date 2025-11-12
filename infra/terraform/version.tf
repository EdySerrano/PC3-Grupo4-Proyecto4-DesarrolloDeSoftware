# Define los proveedores que Terraform necesita descargar
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    # Usaremos el proveedor de Docker para crear contenedores "target"
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}
