Self Signed Cert
=========

This ansible role allows for generating self-signed certificates. As a result, it will generate 3 pem certificates with keys: ca, client and server. Additionally to that, it will also generate 2 pfx certificates for client and server.


## General variables

### Certificate dir
```yaml
self_signed_cert_dir: /etc/certs/
```
This is a directory where certificates will be saved.

### cfssl and cfssl_json download url
```yaml
self_signed_cert_cfssl_url: https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
self_signed_cert_cfssl_json_url: https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
```
You can specify which version of cfssl and cfssl_tool you want to download.

## Profiles
```yaml
self_signed_cert_profiles:
  - name: server
    expirity: 8760h
    usages:
      - signing
      - key encipherment
      - server auth
      - client auth
```
cfssl support multiple profiles. Each profiles has it own unique name. The expirity date determinates when the certificate generated using this profile will be expired. The usages determinates purpose of the certificate. Allowed values are:
* Key Usages: signing, digital signature, content committment, key encipherment, key agreement, data encipherment, cert sign, crl sign, encipher only, decipher only,
* Ext Key Usages: any, server auth, client auth, code signing, email protection, s/mime, ipsec end system, ipsec tunnel, ipsec user, timestamping, ocsp signing, microsoft sgc, netscape sgc
 
## Certificate authority
```yaml
self_signed_cert_ca_certs:
  - name: example-ca
    cn: example.com
    key_algo: rsa
    key_size: 2048
    country: EU
    location: Internet
    organisation: Example
    organisation_unit: IT
    state: internet
    trust_ca_cert: false
```
Certificate authority `key_algo` can has one of values: ECDSA256, RSA. `trust_ca_cert` will inject ca certificated to the trusted root certificates.

## Certificates
```yaml
self_signed_cert_certs:
  - name: server
    profile: server
    ca_name: example-ca
    export_to_pfx: true
    cn: example.com
    hosts:
      - example.com
      - www.example.com
    key_algo: rsa
    key_size: 2048
    country: EU
    location: Internet
    organisation: Example
    organisation_unit: IT
    state: internet
```

Example Playbook
----------------

```yaml
- hosts: localhost
  become: yes
  roles:
    - self-signed-cert
  vars:
    self_signed_cert_cfssl_url: https://github.com/cloudflare/cfssl/releases/download/v1.4.1/cfssl_1.4.1_linux_amd64
    self_signed_cert_cfssl_json_url: https://github.com/cloudflare/cfssl/releases/download/v1.4.1/cfssljson_1.4.1_linux_amd64

    self_signed_cert_dir: /etc/certs/

    self_signed_cert_profiles:
      - name: server
        expirity: 8760h
        usages:
          - signing
          - key encipherment
          - server auth
          - client auth
      - name: client
        expirity: 8760h
        usages:
          - signing
          - key encipherment
          - client auth

    self_signed_cert_ca_certs:
      - name: example-ca
        cn: example.com
        key_algo: rsa
        key_size: 2048
        country: EU
        location: Internet
        organisation: Example
        organisation_unit: IT
        state: internet
        trust_ca_cert: false

    self_signed_cert_certs:
      - name: server
        profile: server
        ca_name: example-ca
        export_to_pfx: true
        cn: example.com
        hosts:
          - example.com
          - www.example.com
        key_algo: rsa
        key_size: 2048
        country: EU
        location: Internet
        organisation: Example
        organisation_unit: IT
        state: internet
      - name: client
        profile: client
        ca_name: example-ca
        export_to_pfx: true
        cn: example.com
        hosts:
          - example.com
          - www.example.com
        key_algo: rsa
        key_size: 2048
        country: EU
        location: Internet
        organisation: Example
        organisation_unit: IT
        state: internet
```