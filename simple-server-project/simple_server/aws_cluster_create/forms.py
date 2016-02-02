from django import forms
import boto3


class CreateClusterStep0(forms.Form):

    client = boto3.client('ec2')
    region_choices = []
    for region in client.describe_regions()['Regions']:
        x = region['RegionName']
        y = (x,x)
        region_choices.append(y)

    region = forms.ChoiceField(choices=region_choices, required=False, label='Regions')


class CreateClusterStep1(forms.Form):

    instance_types = (
        ('t2.micro', 't2.micro - 1 vCPU, 1 GiB, EBS Only'),
        ('t2.small', 't2.small - 1 vCPU, 2 GiB, EBS Only'),
        ('t2.medium', 't2.medium - 2 vCPU, 4 GiB, EBS Only'),
        ('t2.large', 't2.large - 2 vCPU, 8 GiB, EBS Only'),
        ('m3.medium', 'm3.medium - 1 vCPU, 3.75 GiB, 4 GB (SSD)'),
        ('m3.large', 'm3.large - 2 vCPU, 7.5 GiB, 32 GB (SSD)'),
        ('m3.xlarge', 'm3.xlarge - 4 vCPU, 15 GiB, 80 GB (SSD)'),
        ('m3.2xlarge', 'm3.2xlarge - 8 vCPU, 30 GiB, 160 GB (SSD)'),
        ('m4.large', 'm4.large - 2 vCPU, 8 GiB, EBS Only'),
        ('m4.xlarge', 'm4.xlarge - 4 vCPU, 16 GiB, EBS Only'),
        ('m4.2xlarge', 'm4.2xlarge - 8 vCPU, 32 GiB, EBS Only'),
        ('m4.4xlarge', 'm4.4xlarge - 16 vCPU, 64 GiB, EBS Only'),
        ('m4.10xlarge', 'm4.10xlarge - 40 vCPU, 160 GiB, EBS Only'),
        ('c3.large', 'c3.large - 2 vCPU, 3.75 GiB, 32 GB (SSD)'),
        ('c3.xlarge', 'c3.xlarge - 4 vCPU, 7.5 GiB, 80 GB (SSD)'),
        ('c3.2xlarge', 'c3.2xlarge - 8 vCPU, 15 GiB, 160 GB (SSD)'),
        ('c3.4xlarge', 'c3.4xlarge - 16 vCPU, 30 GiB, 320 GB (SSD)'),
        ('c3.8xlarge', 'c3.8xlarge - 32 vCPU, 60 GiB, 640 GB (SSD)'),
        ('c4.large', 'c4.large - 2 vCPU, 3.75 GiB, EBS Only'),
        ('c4.xlarge', 'c4.xlarge - 4 vCPU, 7.5 GiB, EBS Only'),
        ('c4.2xlarge', 'c4.2xlarge - 8 vCPU, 15 GiB, EBS Only'),
        ('c4.4xlarge', 'c4.4xlarge - 16 vCPU, 30 GiB, EBS Only'),
        ('c4.8xlarge', 'c4.8xlarge - 36 vCPU, 60 GiB, EBS Only'),
        ('r3.large', 'r3.large - 2 vCPU, 15.25 GiB, 32 GB (SSD)'),
        ('r3.xlarge', 'r3.xlarge - 4 vCPU, 30.5 GiB, 80 GB (SSD)'),
        ('r3.2xlarge', 'r3.2xlarge - 8 vCPU, 61 GiB, 160 GB (SSD)'),
        ('r3.4xlarge', 'r3.4xlarge - 16 vCPU, 122 GiB, 320 GB (SSD)'),
        ('r3.8xlarge', 'r3.8xlarge - 32 vCPU, 244 GiB, 640 GB (SSD)'),
        ('g2.2xlarge', 'g2.2xlarge - 1 GPU, 8 vCPU, 15 GiB, 60 GB (SSD)'),
        ('g2.8xlarge', 'g2.8xlarge - 4 GPU, 32 vCPU, 60 GiB, 240 GB (SSD)'),
    )

    vpc_choices = (
        ('automatic', 'Automatic VPC Creation'),
        ('existing', 'Existing VPC'),
        ('new', 'New VPC'),
    )


    name = forms.CharField(label='Name', max_length=25, required=False)
    number = forms.CharField(label='Number', max_length=2, required=False)
    instance_type = forms.ChoiceField(choices=instance_types, required=False, label='Flavor')
    region = forms.CharField(label='Region', max_length=12, required=False, widget=forms.HiddenInput())
    vpc_selection = forms.ChoiceField(choices=vpc_choices, label='VPC Options', required=False)

    def __init__(self, *args, **kwargs):

        try:
            myregion = kwargs.pop('myregion')
            super(CreateClusterStep1, self).__init__(*args, **kwargs)
            listOS = ['Amazon Linux AMI 2015*HVM*', 'Red Hat Enterprise Linux 6*HVM*',
                      'SUSE Linux Enterprise Server 12*HVM*', 'Ubuntu Server 14.04*HVM*'
                     ]
            ec2_east = boto3.client('ec2', region_name=myregion)
            ami_choices = []
            data = ec2_east.describe_images(Filters=[{'Name': 'description', 'Values': listOS}])
            for image in data['Images']:
                ami_choices.append((image['ImageId'], image['Description']))

            self.fields['ami'] = forms.ChoiceField(choices=ami_choices, required=False, label='Image Id')

        except:
            self.fields['ami'] = forms.CharField(max_length=20, required=False, label='Image Id')


class CreateClusterStep2(forms.Form):

    name = forms.CharField(label='Name', max_length=25, required=False, widget=forms.HiddenInput())
    ami = forms.CharField(label='Image Id', max_length=25, required=False, widget=forms.HiddenInput())
    vpc = forms.CharField(label='VPC', max_length=25, required=False, widget=forms.HiddenInput())
    instance_type = forms.CharField(label='Flavor', max_length=25, required=False, widget=forms.HiddenInput())
    region = forms.CharField(label='Region', max_length=12, required=False, widget=forms.HiddenInput())
    number = forms.CharField(label='Number', max_length=2, required=False, widget=forms.HiddenInput())
    vpc_selection = forms.CharField(label='vpc_name', max_length=20, required=False, widget=forms.HiddenInput())




class CreateClusterStep3(forms.Form):

    name = forms.CharField(label='Name', max_length=25, required=False, widget=forms.HiddenInput())
    ami = forms.CharField(label='Image Id', max_length=25, required=False, widget=forms.HiddenInput())
    vpc = forms.CharField(label='VPC', max_length=25, required=False, widget=forms.HiddenInput())
    instance_type = forms.CharField(label='Flavor', max_length=25, required=False, widget=forms.HiddenInput())
    region = forms.CharField(label='Region', max_length=12, required=False, widget=forms.HiddenInput())
    number = forms.CharField(label='Number', max_length=2, required=False, widget=forms.HiddenInput())
    roles = forms.CharField(label='Roles', max_length=40, required=False)
    runlist = forms.CharField(label='Runlist', max_length=40, required=False)
    myvpc = forms.CharField(label='VPC', max_length=40, required=False)
    mysubnet = forms.CharField(label='Subnet', max_length=40, required=False)
    mysg = forms.CharField(label='Security Group', max_length=40, required=False)