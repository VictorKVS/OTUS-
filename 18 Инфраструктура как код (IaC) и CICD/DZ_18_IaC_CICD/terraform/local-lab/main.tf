resource "docker_network" "father_vpc" {
  name = "father-dz18-vpc"
}

resource "docker_image" "minio" {
  name         = "minio/minio:latest"
  keep_locally = true
}

resource "docker_container" "minio" {
  name  = "father-dz18-minio"
  image = docker_image.minio.image_id

  command = ["server", "/data", "--console-address", ":9001"]

  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]

  networks_advanced {
    name = docker_network.father_vpc.name
  }

  ports {
    internal = 9000
    external = 9000
  }

  ports {
    internal = 9001
    external = 9001
  }
}

resource "terraform_data" "kind_cluster" {
  input = var.cluster_name

  provisioner "local-exec" {
    command = "python \"${path.module}/../../scripts/ensure_kind_cluster.py\" --name \"${var.cluster_name}\" --config \"${path.module}/../../kind/kind-config.yaml\""
  }

  depends_on = [docker_network.father_vpc]
}
