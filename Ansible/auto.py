import boto
import time
import traceback
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne',endpoint='nova.rc.nectar.org.au')
ACCESS_KEY='5fdf9640ed6e42db8755fe81e87781be'
SERECT_KEY='a83d2b19d1ba4e3c82ca1af73233016e'

print('establish connection...')

try:
    ec2_conn = boto.connect_ec2(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SERECT_KEY,
                            is_secure=True,
                            region=region,
                            port=8773,
                            path='/services/Cloud',
                            validate_certs=False)
except Exception as e:
    print("Exception: "+str(e))


print("creating 8 instances")

instanceNum=8
ec2_conn.run_instances('ami-00003837', max_count=instanceNum, key_name='mykey', instance_type='m1.small', placement='melbourne-qh2', security_groups=['mysecurity'])

for i in range(8):
    vol_req=ec2_conn.create_volume(10,'melbourne-qh2')

print("finished")

instances = ec2_conn.get_only_instances()
vols = ec2_conn.get_all_volumes();
print('checking instance status')

for i in instances:
    while i.update()!="running":
        time.sleep(5)
print("all nodes have been created successfully!")

#list instances details

print("list instance details")
IPs =[]
for i in instances:
    print(i.private_ip_address)
    IPs.append(i.private_ip_address)

#attach volume
print('attaching volume to instance')
for ins, vol in zip([i for i in instances],[vol for vol in vols] ):
    ec2_conn.attach_volume(vol.id,ins.id,"/dev/vdc")
print('attach finished')


#write IP for ansible
filePath1 ='Users/yirupan/Desktop/Ansible/host'
with open(filePath1, 'w') as f:
    content="[Demo]\n"+IPs[0]+"\n"+IPs[1]+"\n"+IPs[2]+"\n"+IPs[3]+"\n"+IPs[4]+"\n"+IPs[5]+"\n"+IPs[6]+"\n"+IPs[7]+"\n"+"[all:vars]\n"+"ansible_ssh_user=ubuntu\n"+"ansible_ssh_private_key_file=/Users/yirupan/.ssh/cloud.key\n"

print("write file finished")