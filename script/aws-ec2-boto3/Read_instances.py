import boto3
#to read argument at startup like command like arguments
#import sys
#read its documentation
#click gives the help option by deafult
import click
#to create a session with AWS account with configured profile
session = boto3.Session(profile_name='training-user')
# Get resources for ec2 instance
ec2 = session.resource('ec2')

@click.command()
def listInstance():
    "List Instances"
    #print all instances
    #these information can be get from boto3 documentation
    for i in ec2.instances.all():
        print(',' .join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name)))

if __name__ == '__main__':

#to display the command line argument    print(sys.argv)
    listInstance()
