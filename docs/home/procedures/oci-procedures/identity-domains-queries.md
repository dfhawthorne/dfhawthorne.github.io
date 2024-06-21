---
layout: default
title: 'Identity Domains Queries'
base-url: home/procedures/oci-procedures/identity-domains-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
file-download-dir: home/procedures/oci-procedures/identity-domains-queries
file-download:
- 'users-list.json'
---

# Identity Domains Queries

## Summary

These are some OCI queries that I use for the `identity-domains` API.

## References

* [Oracle Cloud Infrastructure CLI Command Reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/index.html)
  * [identity-domains](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/identity-domains.html)
    * [me](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/identity-domains/me.html)
    * [users](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/identity-domains/users.html)

## Get Domain URL

All `identity-domains` API calls require the `--endpoint` parameter.

See the following screenshot for getting the endpoint from the Domain URL:

![Get endpoint from Domain URL in the overview for the Default Domain](home/procedures/oci-procedures/identity-domains-queries/get_domain_url.png))

## Show Current User

The following query shows the user name of the currently connected user:

```bash
oci identity-domains me get \
  --query 'data."user-name"' \
  --endpoint https://idcs-effc203d99de4fbf82836e80f9b26ea4.identity.oraclecloud.com:443
```

The sample output is:

```text
"tenancy_admin"
```

__Note__: The brevity of the command is enabled by settings described in "[Install OCI CLI](home/procedures/oci-procedures/install-oci-cli.html)".

## List Users in Default Domain

The following query will list all users in the default domain:

```bash
oci identity-domains users list \
    --query 'data.resources[*].["display-name","nick-name","compartment-ocid"]' \
    --endpoint https://idcs-effc203d99de4fbf82836e80f9b26ea4.identity.oraclecloud.com:443
```

The sample output is:

```text
[
  [
    "Douglas Hawthorne",
    "TAS_TENANT_ADMIN_USER",
    "ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na"
  ],
  [
    "Me",
    null,
    "ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na"
  ]
]
```

To get tabular output, run the following query:

```bash
oci identity-domains users list \
    --query 'data.resources[*].{"Display Name": "display-name", "Nick-name": "nick-name", "Compartment OCID": "compartment-ocid"}' \
    --output table \
    --endpoint https://idcs-effc203d99de4fbf82836e80f9b26ea4.identity.oraclecloud.com:443
```

The sample output is:

```text
+---------------------------------------------------------------------------------+-------------------+-----------------------+
| Compartment OCID                                                                | Display Name      | Nick-name             |
+---------------------------------------------------------------------------------+-------------------+-----------------------+
| ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na | Douglas Hawthorne | TAS_TENANT_ADMIN_USER |
| ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na | Me                | None                  |
+---------------------------------------------------------------------------------+-------------------+-----------------------+
opc-total-items: 2
```

To get all of the returned data, run the following query:

```bash
oci identity-domains users list \
  --endpoint https://idcs-effc203d99de4fbf82836e80f9b26ea4.identity.oraclecloud.com:443 \
  >users-list.json
```

The full output has been uploaded as [users-list.json](home/procedures/oci-procedures/identity-domains-queries/users-list.json).
