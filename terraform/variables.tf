variable "project-name" {
  type        = string
  default     = "ace-mote-484906-q2"
  description = "Name of the project"
}

variable "location" {
  type        = string
  default     = "us-east1"
  description = "Region where the resource will be deployed"
  validation {
    condition     = (var.location == "us-east1" || var.location == "us-central1")
    error_message = "Region must be either us-east1 or us-central1."
  }
}

variable "tf-sa-key-path" {
  type        = string
  default     = "./keys/terraform-sa-key.json"
  description = "Terraform service account json file"
  sensitive   = true
  validation {
    condition     = endswith(var.tf-sa-key-path, ".json")
    error_message = "Provide a valid link to the terraform service account json file."
  }
}
