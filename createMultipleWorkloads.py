#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import sys
import os
from ruamel.yaml import YAML
import time
from datetime import datetime
import subprocess
#python3 createWorkload2.py gke_advanced-editions-engineering_us-west2_ybhagwan-gke-build1 50 medium tap-install 360
#python3 deliverables.ya "build cluster" "run cluster" "n-workloads" "dev-namespace"
#python3 deliverables.ya gke_advanced-editions-engineering_us-west2_ybhagwan-gke-build1 gke_advanced-editions-engineering_us-central1_ybhagwan-gke-run2 "n-workloads" "dev-namespace"

yaml = YAML()
yaml.preserve_quotes = True

ExecStartTime = datetime.now()
print("Start time : "+str(ExecStartTime))

def checkWorkloadsStatus(nworkloads, nameSpace, period):
    timeLapse = 0
    startTime = time.time()
    while(timeLapse <= period):
        try:
            proc = subprocess.Popen("/usr/local/bin/tanzu apps workload list -n "+nameSpace,shell = True, stdout=subprocess.PIPE)
            result,err = proc.communicate()
            readyCount = result.decode('ascii').count("Ready")
            print("Total number of Ready workloads   : "+str(readyCount))
            print("Total number of Unknown workloads : "+str(workloads - readyCount))
            print("Total time elapsed in seconds     : "+str(timeLapse))
            if(readyCount == nworkloads):
                print("All workloads are in ready state in "+str(timeLapse)+" sec")
                break
            time.sleep(3)
            timeLapse = int(time.time() - startTime)
        except UnicodeDecodeError as e:
            print(e)

def createWorkload(wType, num, waitTime, nameSpace):
    workloadFile = "small"
    workloadName = "tanzu-java-web-app-"
    if(wType == "medium"):
        workloadFile = "mediumWorkload.yaml"
        workloadName = "spring-petclinic-"
    else:
        workloadFile = "smallWorkload.yaml"
    for i in range(1,workloads+1):
        with open(workloadFile) as data:
            documents = yaml.load(data)
            print(documents['metadata']['name'])
            documents['metadata']['name'] = workloadName+str(i)
            print(documents['metadata']['name'])
            with open("workload_temp.yaml", "w+") as wt:
                yaml.dump(documents, wt)
            #os.system('tanzu apps workload apply -f workload_temp.yaml -n '+nameSpace+' --yes')
            proc2 = subprocess.Popen('tanzu apps workload apply -f workload_temp.yaml -n '+nameSpace+' --yes',shell = True, stdout=subprocess.PIPE)
            result,err = proc2.communicate()
            print(result.decode('ascii'))


buildCluster = sys.argv[1]
workloads = int(sys.argv[2])
workloadType = sys.argv[3]
nameSpace = sys.argv[4]
period = int(sys.argv[5])

#os.system('kubectl config use-context '+ buildCluster)
proc1 = subprocess.Popen('kubectl config use-context '+ buildCluster,shell = True, stdout=subprocess.PIPE)
result,err = proc1.communicate()
print(result.decode('ascii'))
time.sleep(5)


createWorkload(workloadType, workloads, period, nameSpace)
checkWorkloadsStatus(workloads, nameSpace, period)

ExecEndTime = datetime.now()
print("===========================")
print("Execution Start Time : "+str(ExecStartTime))
print("Execution End Time   : "+str(ExecEndTime))
