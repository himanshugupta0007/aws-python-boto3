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

#to group instances command
@click.group()
def instance():
    """Command for Instances"""

@instance.command('list')
#gives option to provide parameter
@click.option('--project', default=None,
help="Only Instances for project (tag Project:<name>)")
def listInstance(project):
    "List Instances"
    instances = getInstance(project)
    #print all instances
    #these information can be get from boto3 documentation
    for i in instances:
        tags= {t['Key']: t['Value'] for t in i.tags or []}
        print(',' .join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

@instance.command('stop')
@click.option('--project', default=None,
help="Only Instances for project (tag Project:<name>)")
def stopInstance(project):
    """Stop Instances"""
    instances = getInstance(project)
    for i in instances:
        print("Stopping instance {0}....".format(i))
        i.stop();

@instance.command('start')
@click.option('--project', default=None,
help="Only Instances for project (tag Project:<name>)")
def stopInstance(project):
    """Start Instances"""
    instances = getInstance(project)
    for i in instances:
        print("Start instance {0}....".format(i))
        i.start();

@instance.command('restart')
@click.option('--project', default=None,
help="Only Instances for project (tag Project:<name>)")
def stopInstance(project):
    """Restarting Instances"""
    instances = getInstance(project)
    for i in instances:
        print("Restarting instance {0}....".format(i))
        i.restart();

#method to get list of all instances
def getInstance(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

if __name__ == '__main__':

#to display the command line argument    print(sys.argv)
    instance()
