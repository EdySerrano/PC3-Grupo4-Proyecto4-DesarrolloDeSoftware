# Define los proveedores que Terraform necesita descargar
terraform {
  required_providers {
    # Usaremos el proveedor de Docker para crear contenedores "target"
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}