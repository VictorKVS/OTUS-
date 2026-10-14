variable "cluster_name" {
  type        = string
  description = "Kind cluster name."
  default     = "father-dz18"
}

variable "minio_root_user" {
  type        = string
  description = "Local lab MinIO root user."
  sensitive   = true
}

variable "minio_root_password" {
  type        = string
  description = "Local lab MinIO root password."
  sensitive   = true
}
