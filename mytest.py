import boto3


def getAllVpcs(region):

        vpcs = []
        #print(region)
        ec2 = boto3.client('ec2', region_name=region)
        data = ec2.describe_vpcs()
        #print(data)
        
        for vpc in data['Vpcs']:
            if 'Tags' in vpc:
                mytag =  ''
                for tag in vpc['Tags']:
                    if tag['Key'] == 'Name':
                        mytag = tag['Value']

                cidr = vpc['CidrBlock']
                mystr = mytag + ' - (' + cidr + ')'
                vpcs.append((mytag,mystr))
                
            else:
                cidr = vpc['CidrBlock']
                mystr = 'Default' + ' - (' + cidr + ')'
                vpcs.append(('Default',mystr))

        return vpcs




region_choices = getAllVpcs('us-east-1')
print(region_choices)
