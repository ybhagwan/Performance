# Performance
This project contains performance script


File **createMultipleWorkloads.py** used to create multiple workloads on a given cluster and wait for all the workloads to become ready state.

Use below command to execute create the workload :\
python3 createMultipleWorkloads.py clusterName numberOfWorkloads workloadTypes namespace

**Parameters**\
-------\
**clusterName** : iterrate/build/full cluster name (ex : ybhagwan-aks-build or gke_advanced-editions-engineering_us-west2_ybhagwan-gke-build)\
**numberOfWorkloads** : eg : 10, 50, 100\
**workloadTypes** : light/medium (light : tanzu-java-web-app and medium : spring-petclinic)
