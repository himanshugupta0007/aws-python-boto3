import boto3

#to create a session with AWS account with configured profile
session = boto3.Session(profile_name='training-user')
# Get resources for ec2 instance
ec2 = session.resource('ec2')
#print all instances
for i in ec2.instances.all():
    print(i)
