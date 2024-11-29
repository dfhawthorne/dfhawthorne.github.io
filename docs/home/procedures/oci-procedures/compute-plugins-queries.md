---
layout: default
title: 'Compute Plugins Queries'
base-url: home/procedures/oci-procedures/compute-plugins-queries.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
---

## Summary

There is no separate list of available agents that are available for the launch of a compute instance. Instead, a compute instance needs to be launched first, then that instance is interrogated to find what agent plug-ins are available.

## Get All Available Agent Plug-ins for a Compute Instance

Run the following OCI CLI commands to generate a table of available agent plug-ins along with the current status:

```bash
instance_id=$(                                  \
    oci compute instance list                   \
    --compartment-id ${compartment_id}          \
    --query 'data[0].id'                        \
    --raw-output                                \
    )
oci instance-agent plugin list                  \
    --compartment-id ${compartment_id}          \
    --instanceagent-id ${instance_id}           \
    --query "data[*].{Name:name,Status:status}" \
    --output table
```

## Sample Output

Sample output is:

```text
+-------------------------------------+---------------+
| Name                                | Status        |
+-------------------------------------+---------------+
| Custom Logs Monitoring              | RUNNING       |
| Compute Instance Run Command        | RUNNING       |
| OS Management Service Agent         | STOPPED       |
| Cloud Guard Workload Protection     | RUNNING       |
| WebLogic Management Service         | STOPPED       |
| Vulnerability Scanning              | STOPPED       |
| Compute HPC RDMA Authentication     | NOT_SUPPORTED |
| OS Management Hub Agent             | STOPPED       |
| Management Agent                    | STOPPED       |
| Oracle Java Management Service      | STOPPED       |
| Compute RDMA GPU Monitoring         | NOT_SUPPORTED |
| Compute HPC RDMA Auto-Configuration | NOT_SUPPORTED |
| Block Volume Management             | STOPPED       |
| Oracle Autonomous Linux             | STOPPED       |
| Compute Instance Monitoring         | RUNNING       |
| Bastion                             | STOPPED       |
+-------------------------------------+---------------+
```
