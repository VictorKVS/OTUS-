output "local_vpc_name" {
  value = docker_network.father_vpc.name
}

output "minio_api" {
  value = "http://127.0.0.1:9000"
}

output "minio_console" {
  value = "http://127.0.0.1:9001"
}

output "kind_cluster_name" {
  value = terraform_data.kind_cluster.output
}
