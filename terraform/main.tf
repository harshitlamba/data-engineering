terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  credentials = "./keys/terraform-sa-key.json"
  project     = "ace-mote-484906-q2"
  region      = "us-east1"
}

# auto-expire-bucket is the terraform resource name used for references
resource "google_storage_bucket" "auto-expire-bucket" {
  # dezoom_auto_expire_bucket is the actual bucket name in GCP; it must be globally unique, in lowercase
  name = "dezoom_auto_expire_bucket"
  # US would be multi-region and us-east1 would be single region
  location = "US"
  # normally GCS buckets cannot be destroyed if they contain objects; force_destroy=true deletes everything inside 
  # it first, then delete the bucket.
  force_destroy = true

  # deletes each object (bucket content) after it has existed for 3 days
  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  # in case we want to upload a huge file to GCS, we can do it in multipart parallel uploads where the file is divided into multiple
  # chunks and parallel processes upload it, and then assemble them into a single, final object
  # finds the uploads that were started but never completed; GCS aborts them and deletes partial data if they are 1 day old or more
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# demo-dataset is Terraform resource name (used internally by Terraform, not in GCP)
resource "google_bigquery_dataset" "demo-dataset" {
  # dataset_id in BigQuery - it becomes a part of the dataset's full name - project_id:demo_dataset_id; must contain only letters, numbers and _
  dataset_id  = "demo_dataset_id"
  description = "This is a demo dataset created using terraform"
  # location where the dataset is stored; "US" means multi-region in the US; all tables in the dataset must inherit this location
  # queries across datasets must be in the same location
  location = "US"
  # default expiration time (in ms) for tables created in this dataset; any table created without its own expiration will be
  # automatically deleted after 1 hour
  default_table_expiration_ms = 3600000
  #   delete all the tables in the dataset when destroying a resource; else destroying will fail if tables are present
  delete_contents_on_destroy = true
}
