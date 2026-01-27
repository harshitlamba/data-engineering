variable "credentials" {
  description = "My Credentials"
  default     = "../../../terraform/keys/terraform-sa-key.json"
}

variable "project" {
  description = "Project"
  default     = "ace-mote-484906-q2"
}

variable "region" {
  description = "Region"
  default     = "us-east1"
}

variable "location" {
  description = "Project Location"
  default     = "us-east1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "module1_hw_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "module1_hw_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
