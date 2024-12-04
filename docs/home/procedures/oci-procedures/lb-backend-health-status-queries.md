---
layout: default
title: 'LB Backend Health Status Queries'
base-url: home/procedures/oci-procedures/lb-backend-health-status-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

## Summary

This procedure lists the health status of an OCI Load Balancer Back End.

## Procedure

The following procedure lists the health status of the first backend in the first backend set of the load balancer, called "IAD-NP-LAB11-LB-01":

```bash
compartment_id=... # Set Compartment OCID
lb_id=$(                                        \
    oci lb load-balancer list                   \
        --compartment-id ${compartment_id}      \
        --all                                   \
        --display-name "IAD-NP-LAB11-LB-01"     \
        --query 'data[0].id'                    \
        --raw-output                            \
    )
bs_name=$(                                      \
    oci lb backend-set list                     \
        --all                                   \
        --load-balancer-id ${lb_id}             \
        --query 'data[0].name'                  \
        --raw-output                            \
    )
be_name=$(                                      \
    oci lb backend list                         \
        --all                                   \
        --backend-set-name ${bs_name}           \
        --load-balancer-id ${lb_id}             \
        --query 'data[0].name'                  \
        --raw-output                            \
    )
oci lb backend-health get                       \
    --backend-name ${be_name}                   \
    --backend-set-name ${bs_name}               \
    --load-balancer-id ${lb_id}                 \
    --query 'data."health-check-results"[*].{Status:"health-check-status","Time Stamp":timestamp}' \
    --output table
```

Sample output is:

```text
+--------+----------------------------------+
| Status | Time Stamp                       |
+--------+----------------------------------+
| OK     | 2024-12-04T14:23:06.225000+00:00 |
| OK     | 2024-12-04T14:23:37.190000+00:00 |
+--------+----------------------------------+
```
