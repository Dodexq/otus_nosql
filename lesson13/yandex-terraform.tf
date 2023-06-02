terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  zone = "ru-central1-a"
}

resource "yandex_compute_instance" "vm-1" {
  count    = 1
  name     = "mongodb-${count.index}"
  hostname = "mongodb-${count.index}"


  resources {
    cores         = 2
    memory        = 2
    core_fraction = 20
  }

  boot_disk {
    initialize_params {
      image_id = "fd8firhksp7daa6msfes"
      size     = 20
    }
  }

  network_interface {
    subnet_id = "e9b1klk6eag8t0kvasdm"
    nat       = true
  }

  metadata = {
    # user-data = file("${path.module}/metadata.yaml")
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }

  scheduling_policy {
    preemptible = true
  }
}