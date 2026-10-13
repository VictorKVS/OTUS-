# DZ20 Terraform-style pseudocode.
# Provider-specific resources are intentionally abstracted for the homework.

terraform {
  required_version = ">= 1.6.0"
}

module "network" {
  source = "./modules/network"
  name   = "father-ai-prod"
  cidr   = "10.40.0.0/16"
}

module "kubernetes" {
  source     = "./modules/kubernetes"
  network_id = module.network.id
  node_pool  = "ai-runtime"
}

module "object_storage" {
  source = "./modules/object-storage"
  buckets = [
    "father-datasets",
    "father-model-artifacts",
    "father-rag-artifacts",
    "father-release-evidence"
  ]
}

module "artifact_registry" {
  source = "./modules/artifact-registry"
  name   = "father-ai-images"
}

module "observability" {
  source     = "./modules/observability"
  cluster_id = module.kubernetes.id
}

output "kubernetes_cluster" {
  value = module.kubernetes.name
}

output "artifact_registry" {
  value = module.artifact_registry.uri
}

output "model_artifact_bucket" {
  value = module.object_storage.bucket["father-model-artifacts"]
}
