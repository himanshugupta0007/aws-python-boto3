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

#master group
@click.group()
def cli():
    """ Group for CLI """


#create group for volumne
@cli.group('volume')
def volumne():
    """Command for Volumnes """
#to group instances command
@cli.group('instance')
def instance():
    """Command for Instances"""

@cli.group('snapshot')
def snapshot():
    """ Command for Snapshot """

#to list all snapshots
@snapshot.command('list')
@click.option('--project', default=None,
help="Only Snapshot of Volumnes for instances for project (tag Project:<name>)")
def listSnapshot(project):
        ec2resource = getInstance(project)
        for e in ec2resource:
            for v in e.volumes.all():
                for s in v.snapshots.all():
                    print(", ".join((
                        s.id,
                        v.id,
                        e.id,
                        s.state,
                        s.progress,
                        s.start_time.strftime("%c")
                )))
        return

#to create a snapshot from an instances
@instance.command('snapshot')
@click.option('--project', default=None,
help="Only Volumnes for instances for project (tag Project:<name>)")
def create_snapshot(project):
    """ Create snapshot for EC2 Instance """
    ec2resource = getInstance(project)
    for e in ec2resource:
        for v in e.volumes.all():
            print("Creating Snapshot for Volume {0} ".format(v.id))
            v.create_snapshot(Description="Created by Python Script")
        return

@volumne.command('list')
@click.option('--project', default=None,
help="Only Volumnes for instances for project (tag Project:<name>)")
def listVolumne(project):
    ec2resource = getInstance(project)
    for e in ec2resource:
        for v in e.volumes.all():
            print(", ".join((
                v.id,
                e.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return


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
    cli()
