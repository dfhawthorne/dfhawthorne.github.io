---
layout: default
title: 'Identity Domains Queries'
base-url: docs/home/procedures/oci-procedures/identity-domains-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

# Identity Domains Queries

## Summary

These are some OCI queries that I use for the `identity-domains` API.

## Show Current User

The following query shows the user name of the currently connected user:

```bash
oci identity-domains me get --query 'data."user-name"'
```

The sample output is:

```text
"tenancy_admin"
```

__Note__: The brevity of the command is enabled by settings described in "[Install OCI CLI](home/procedures/oci-procedures/install-oci-cli.html)".

## List Users in Default Domain

The following query will list all users in the default domain:

```bash
oci identity-domains users list --query 'data.resources[*].["display-name","nick-name","compartment-ocid"]'
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
oci identity-domains users list --query 'data.resources[*].["display-name","nick-name","compartment-ocid"]' --output table
```

The sample output is:

```text
+-------------------+-----------------------+---------------------------------------------------------------------------------+
| Column1           | Column2               | Column3                                                                         |
+-------------------+-----------------------+---------------------------------------------------------------------------------+
| Douglas Hawthorne | TAS_TENANT_ADMIN_USER | ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na |
| Me                | None                  | ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na |
+-------------------+-----------------------+---------------------------------------------------------------------------------+
opc-total-items: 2
```
