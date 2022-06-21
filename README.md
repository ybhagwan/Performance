# Performance
This project contains performance script

Pre-requisite :
1. Install package uamel.yaml : pip3 install ruamel.yaml

File **createMultipleWorkloads.py** used to create multiple workloads on a given cluster and wait for all the workloads to become ready state.

Use below command to execute create the workload :\
python3 createMultipleWorkloads.py clusterName numberOfWorkloads workloadTypes namespace waitTime

**Parameters**\
**clusterName**       : iterrate/build/full cluster name (Ex : ybhagwan-aks-build or gke_advanced-editions-engineering_us-west2_ybhagwan-gke-build)\
**numberOfWorkloads** : Eg : 10, 50, 100\
**workloadTypes**     : light/medium (light : tanzu-java-web-app and and medium : spring-petclinic)\
**namespace**         : developer namespace (Eg : my-apps or tap-install)\
**wiatTime**          : Specified time (in seconds) to wait to comeup all the workload in ready state (Eg: 3600/7200)
