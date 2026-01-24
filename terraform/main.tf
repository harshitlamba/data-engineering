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
  # dezoom-auto-expire-bucket is the actual bucket name in GCP; it must be globally unique, in lowercase
  name = "dezoom-auto-expire-bucket"
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
