---
layout: default
title: 'OCI Limits Queries'
base-url: home/procedures/oci-procedures/oci-limits-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

# OCI Limits

## Summary

These are some OCI CLI queries for getting limits and availability for resources in the tenancy.

## Find All VCN Limit Names

I used the following commands to get the names of limits for Virtual Cloud Networks (VCNs) in my tenancy. I used the `printf` command to get the quoting right for the query:

```bash
printf -v query 'data[?contains("service-name",%s)].{"Name":name,"Description":description}' "'vcn'"
oci limits definition list              \
    --compartment-id ${tenancy_ocid}    \
    --query "${query}"                  \
    --all                               \
    --output table
```

The output for always-free OCI account is:

```text
+--------------------------------------------------------------+----------------------------+
| Description                                                  | Name                       |
+--------------------------------------------------------------+----------------------------+
| Max byoip ranges per region per tenant                       | byoip-ranges-per-region    |
| DHCP Options (per VCN)                                       | dhcp-option-count          |
| FlowLogConfig Count                                          | flow-log-config-count      |
| Internet Gateways (per VCN)                                  | internet-gateway-count     |
| Max compartment limit for IP Inventory per region per tenant | ip-inventory-compartments  |
| NAT Gateways (per VCN)                                       | nat-gateway-count          |
| Max public ip pools per region per tenant                    | public-ip-pools-per-region |
| Reserved Public IP Count                                     | reserved-public-ip-count   |
| Route Tables (per VCN)                                       | route-table-count          |
| Security Lists (per VCN)                                     | security-list-count        |
| Subnets (per VCN)                                            | subnet-count               |
| Virtual Cloud Networks Count                                 | vcn-count                  |
+--------------------------------------------------------------+----------------------------+
```

## Get the Used and Available Counts for VCNs

Run the following command to get available and used counts for VCNs:

```bash
oci limits resource-availability get    \
    --compartment-id ${tenancy_ocid}    \
    --service-name "vcn"                \
    --limit-name "vcn-count"
```

The sample output is:

```text
{
  "data": {
    "available": 1,
    "effective-quota-value": null,
    "fractional-availability": 1.0,
    "fractional-usage": 1.0,
    "used": 1
  }
}
```


