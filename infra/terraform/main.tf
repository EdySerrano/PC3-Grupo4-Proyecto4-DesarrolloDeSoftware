# Define la imagen de Nginx
resource "docker_image" "nginx_target" {
  name = "nginx:1.21"
}


resource "docker_container" "nginx_container_target" {
  image = docker_image.nginx_target.image_id
  name  = "audit-cli-target-nginx-s2"

  # Mapea el puerto 80-> 8080
  ports {
    internal = 80
    external = 8080
  }
}