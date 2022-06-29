#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
from threading import Thread
import sys
from ruamel.yaml import YAML
import os
import time
from datetime import datetime
import subprocess
#python3 deliverables.ya "build cluster" "run cluster"  "workloadType" "n-workloads" "dev-namespace" "period

yaml = YAML()
yaml.preserve_quotes = True
timestamp1 = datetime.now()
timestamp = timestamp1.strftime('%d-%b-%Y-%H-%M-%S')
dir1 = os.getcwd() + 'deliverables-'+timestamp
os. makedirs(dir1)

ExecStartTime = datetime.now()
print("Start time : "+str(ExecStartTime))

def createDeliverables(buildCluster, workloadType, nWorkloads, nameSpace):
    proc1 = subprocess.Popen('kubectl config use-context '+ buildCluster,shell = True, stdout=subprocess.PIPE)
    result,err = proc1.communicate()
    print(result.decode('ascii'))
    time.sleep(5)
    #deliverableName default name
    deliverableName = "tanzu-java-web-app-"
    if(workloadType == "medium"):
        deliverableName = "spring-petclinic-"

    for i in range(1,nWorkloads+1):
        proc1 = subprocess.Popen('kubectl get deliverable'+deliverableName+str(i)+' --namespace '+nameSpace+' -oyaml > '+dir1+'deliverables-'+deliverableName+str(i)+'.yaml')
        result,err = proc1.communicate()
        print(result.decode('ascii'))
        with open(dir1+'/deliverables-'+deliverableName+str(i)+'.yaml', 'w+') as stream:
            try:
                d=yaml.safe_load(stream)
                del(d['status'])
                del(d['metadata']['ownerReferences'])
                stream.flush()
                yaml.dump(d, stream, allow_unicode=True)
            except yaml.YAMLError as e:
                print(e)

def importDeliverables(runCluster, workloadType, nWorkloads, nameSpace):
    proc1 = subprocess.Popen('kubectl config use-context '+ runCluster,shell = True, stdout=subprocess.PIPE)
    result,err = proc1.communicate()
    print(result.decode('ascii'))
    time.sleep(5)
    #defining default name
    deliverableName = "tanzu-java-web-app-"
    if(workloadType == "medium"):
        deliverableName = "spring-petclinic-"

    for i in range(1,workloads+1):
        proc1 = subprocess.Popen('kubectl apply -f '+dir1+'/deliverables-'+deliverableName+str(i)+'.yaml -n '+nameSpace+' &')
        result,err = proc1.communicate()
        print(result.decode('ascii'))

def checkWorkloadsStatus(nworkloads, nameSpace, period):
    timeLapse = 0
    startTime = time.time()
    while(timeLapse <= period):
        try:
            proc = subprocess.Popen("kubectl get ksvc -n "+nameSpace,shell = True, stdout=subprocess.PIPE)
            result,err = proc.communicate()
            ksvcStaus = result.decode('ascii').count("True")
            print("Total number of workloads have ksvc in True state : "+str(ksvcStaus))
            print("Total number of workloads have ksvc in False state: "+str(nworkloads - ksvcStaus))
            print("Total time elapsed in seconds     : "+str(timeLapse))
            if(ksvcStaus == nworkloads):
                print("All workloads ksvc are in True state in "+str(timeLapse)+" sec")
                break
            time.sleep(3)
            timeLapse = int(time.time() - startTime)
        except UnicodeDecodeError as e:
            print(e)


buildCluster = sys.argv[1]
runCluster = sys.argv[2]
workloadType = sys.argv[3]
workloads = int(sys.argv[4])
nameSpace = sys.argv[5]
period = sys.argv[6]

createDeliverables(buildCluster, workloadType, workloads, nameSpace)
importDeliverables(runCluster, workloadType, workloads, nameSpace)
checkWorkloadsStatus(workloads, nameSpace, period)

ExecEndTime = datetime.now()
print("===========================")
print("Execution Start Time : "+str(ExecStartTime))
print("Execution End Time   : "+str(ExecEndTime))
