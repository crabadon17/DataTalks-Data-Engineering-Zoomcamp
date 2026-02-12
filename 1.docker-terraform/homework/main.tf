
provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

data "google_service_account_access_token" "default" {
  provider               = google
  target_service_account = "terraform-runner@de-zoomcamp-486100.iam.gserviceaccount.com"
  scopes                 = ["https://www.googleapis.com/auth/cloud-platform"]
  lifetime               = "3600s"
}

provider "google" {
  alias        = "impersonated"
  access_token = data.google_service_account_access_token.default.access_token

  project = var.project
  region  = var.region
  zone    = var.zone
}
