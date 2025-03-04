terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.19.0"
    }
  }
}

provider "google" {
    # Set 'credentials' if GOOGLE_APPLICATION_CREDENTIALS is not set
  project = "zoomcamp-airflow-450009"
  region  = "europe-west1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "zoomcamp-airflow-450009-terra-bucket" # Has to be globally unique across all GCP
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1 # In days
    }
    action {
      type = "AbortIncompleteMultipartUpload" # Split data into chunks when uploading
    }
  }
}