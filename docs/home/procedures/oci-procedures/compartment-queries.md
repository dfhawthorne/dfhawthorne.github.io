---
layout: default
title: 'Compartment Queries'
base-url: docs/home/procedures/oci-procedures/compartment-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

# Compartment Queries

## Summary

These are some OCI queries that I use for the `iam compartment` API.

## References

* [Oracle Cloud Infrastructure CLI Command Reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/index.html)
  * [iam](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/iam.html)
    * [compartment](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/iam/compartment.html)
      * [list](https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.43.0/oci_cli_docs/cmdref/iam/compartment/list.html)

## List All Compartments in a Tenancy

To list all compartments in the tenancy, run:

```bash
oci iam compartment list                                  \
    --query 'data[*].{"Compartment Name": "name", "Compartment Description": "description", "Compartment ID": "id"}' \
    --include-root                                        \
    --output table
```

The editted output is:

```text
+--------------------------------------------------------------------------+-------------------------------------------------------------------------------------+---------------------------+
| Compartment Description                                                  | Compartment ID                                                                      | Compartment Name          |
+--------------------------------------------------------------------------+-------------------------------------------------------------------------------------+---------------------------+
| dhawthorne80                                                             | ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na     | dhawthorne80              |
| idcs-effc203d99de4fbf82836e80f9b26ea4*********************************** | ocid1.compartment.oc1..aaaaaaaa6wcn7fgccosatmofyxgmgtrntfqd6wcitewbdyjlc2rbjptwq5oq | ManagedCompartmentForPaaS |
| Mastadon Sample Deployment from OCI Ops Professional Course              | ocid1.compartment.oc1..aaaaaaaax4nkky4yov3bahtf3cg226ya2ngsaru7vxkv6pavdjwzz5udsojq | mastadon_compartment      |
| Personal applications                                                    | ocid1.compartment.oc1..aaaaaaaaxkug4sujmcc65lxxf7pb65alifwibd6wmbj7ohqlykeezt4lr5cq | Personal                  |
| Sandbox                                                                  | ocid1.compartment.oc1..aaaaaaaamoo6uz2qmix2adls2cgoqxxhdt4wuam3wbcrw6co6z4osweos6da | Sandbox                   |
+--------------------------------------------------------------------------+-------------------------------------------------------------------------------------+---------------------------+
```

## Get OCID for a Compartment

To get the OCID for the `Sandbox` compartment, run the following command:

```bash
printf "The OCID for Sandbox compartment is %s\n" \
    $(oci iam compartment list --query 'data[0].id' --name 'Sandbox' --raw-output)
```

The sample output is:

```text
The OCID for Sandbox compartment is ocid1.compartment.oc1..aaaaaaaamoo6uz2qmix2adls2cgoqxxhdt4wuam3wbcrw6co6z4osweos6da
```
