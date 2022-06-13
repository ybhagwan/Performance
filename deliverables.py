#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
from threading import Thread
import sys
import yaml
import os
import time
from datetime import datetime

#python3 deliverables.ya "build cluster" "run cluster" "n-workloads" "dev-namespace"

timestamp1 = datetime.now()
timestamp = timestamp1.strftime('%d-%b-%Y-%H-%M-%S')
dir1 = os.getcwd() + 'deliverables-'+timestamp
os. makedirs(dir1)
buildCluster = sys.argv[1]
runCluster = sys.argv[2]
workloads = int(sys.argv[3])
nameSpace = sys.argv[4]

os.system('kubectl config use-context '+ buildCluster)
print("contexts set to build cluster")
time.sleep(5)
for i in range(1,workloads+1):
    os.system('kubectl get deliverable spring-petclinic-'+str(i)+' --namespace '+nameSpace+' -oyaml > deliverables-spring-petclinic-'+str(i)+'.yaml')
    with open(dir1+'/deliverables-spring-petclinic-'+str(i)+'.yaml', 'w+') as stream:
        try:
            print(stream)
            d=yaml.safe_load(stream)
            del(d['status'])
            del(d['metadata']['ownerReferences'])
            stream.flush()
            yaml.dump(d, stream, allow_unicode=True)
        except yaml.YAMLError as e:
            print(e)

print('Switching to run cluster from build cluster')
os.system('kubectl config use-context '+runCluster)
os.system('kubectl config get-contexts')
print('Successfully switched to run cluster')
for i in range(1,workloads+1):
    os.system('kubectl apply -f '+dir1+'/deliverables-spring-petclinic-'+str(i)+'.yaml -n '+nameSpace+' &')

print('waiting for 30 sec after importing build cluster deliverables in run cluster')
time.sleep(30)
os.system('kubectl get deliverables -A')
