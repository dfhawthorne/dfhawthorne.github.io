---
layout: default
title: 'Bastion Queries'
base-url: home/procedures/oci-procedures/bastion-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

## Summary

A bastion allows connection to VMs in private sub-nets.


## List All Bastions in Compartment

With the variable, `compartment_id`, set to the required OCI compartment, run the following OCI CLI command to get all bastions in that compartment:

```bash
oci bastion bastion list                                                \
    --compartment-id ${compartment_id}                                  \
    --all                                                               \
    --query 'data[*].{Name:name,"Lifecycle State":"lifecycle-state"}'   \
    --output table
```

Sample output is:

```text
+-----------------+------------------+
| Lifecycle State | Name             |
+-----------------+------------------+
| ACTIVE          | NPLAB10BASTION01 |
+-----------------+------------------+
```

The inclusion of the `--all` parameter suppresses the following warning:

```text
WARNING: This operation supports pagination and not all resources were returned.  Re-run using the --all option to auto paginate and list all resources.
```

## Get OCID for Bastion

Selecting a basion name from the previous query, run the following command to the OCID of that bastion:

```bash
bastion_id=$(                           \
    oci bastion bastion list            \
    --compartment-id ${compartment_id}  \
    --name "NPLAB10BASTION01"           \
    --all                               \
    --query 'data[0].id'                \
    --raw-output                        \
    )
```

The inclusion of the `--all` parameter suppresses the following warning:

```text
WARNING: This operation supports pagination and not all resources were returned.  Re-run using the --all option to auto paginate and list all resources.
```

## Create Bastion Session

In order to create a bastion session, the following variables need to be set:

| ---------------- | ------------------------------------ |
| Variable         | Description                          |
| ---------------- | ------------------------------------ |
| `bastion_id`     | OCID of bastion (see previous query) |
| `compartment_id` | OCID of compartment                  | 
| `private_ip`     | IP address of VM                     |
| `vm_id`          | OCID of Compute Instance             |

__Note:__ This example assumes that you have already generated a SSH key pair (`~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`).

Run the following commands to connect to a VM via the bastion:

```bash
session_id=$(                                       \
    oci bastion session create-managed-ssh          \
        --compartment-id ${compartment-id}          \
        --bastion-id ${bastion_id}                  \
        --key-type PUB                              \
        --ssh-public-key-file ~/.ssh/id_rsa.pub     \
        --target-os-username opc                    \
        --target-private-ip ${private_ip}           \
        --target-resource-id ${vm_id}               \
        --wait-for-state SUCCEEDED                  \
        --wait-for-state FAILED                     \
        --raw-output                                \
        --query 'data.resources[0].identifier'      \
    )
eval $(                                             \
    oci bastion session get                         \
        --compartment-id ${compartment-id}          \
        --session-id ${session_id}                  \
        --query 'data."ssh-metadata".command'       \
        --raw-output |                              \
    sed -e 's!<privateKey>!~/.ssh/id_rsa!g'         \
    )
```


## Get Sessions for Bastion

```bash
oci bastion session list                \
    --bastion-id ${bastion_id}          \
    --compartment-id ${compartment_id}  \
    --all                               \
    --query 'data[0].{"Bastion Name":"bastion-name","Session Name":"display-name","Lifecycle State":"lifecycle-state","Session Type":"target-resource-details"."session-type",VM:"target-resource-details"."target-resource-display-name","User":"target-resource-details"."target-resource-operating-system-user-name"}' \
    --output table
```

Sample output is:

```text
+------------------+-----------------+-------------------------------+--------------+------+------------------------+
| Bastion Name     | Lifecycle State | Session Name                  | Session Type | User | VM                     |
+------------------+-----------------+-------------------------------+--------------+------+------------------------+
| NPLAB10BASTION01 | DELETED         | bastionsession2024-11-29-1118 | MANAGED_SSH  | opc  | instance20241129121320 |
+------------------+-----------------+-------------------------------+--------------+------+------------------------+
```

The inclusion of the `--all` parameter suppresses the following warning:

```text
WARNING: This operation supports pagination and not all resources were returned.  Re-run using the --all option to auto paginate and list all resources.
```

