from django import forms


class CreateClusterStep1(forms.Form):

    image_choices = (
        ('b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150706-en-us-30GB',
         'Ubuntu 14.04 LTS AMD64 Server EN_US 30GB'),
        ('0b11de9248dd4d87b18621318e037d37__RightImage-CentOS-6.5-x64-v14.1', 'CentOS 6.5 x64'),
    )

    flavor_choices = (
        ('Basic_A0', 'Basic_A0'),
        ('Basic_A1', 'Basic_A1'),
        ('Basic_A2', 'Basic_A2'),
        ('Basic_A3', 'Basic_A3'),
        ('Basic_A4', 'Basic_A4'),
        ('ExtraSmall', 'ExtraSmall'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('ExtraLarge', 'ExtraLarge'),
        ('A5', 'A5'),
        ('A6', 'A6'),
        ('A8', 'A8'),
        ('A9', 'A9'),
        ('A10', 'A10'),
        ('A11', 'A11'),
        ('Standard_D1', 'Standard_D1'),
        ('Standard_D2', 'Standard_D2'),
        ('Standard_D3', 'Standard_D3'),
        ('Standard_D4', 'Standard_D4'),
        ('Standard_D11', 'Standard_D11'),
        ('Standard_D12', 'Standard_D12'),
        ('Standard_D13', 'Standard_D13'),
        ('Standard_D14', 'Standard_D14'),
        ('Standard_D1_v2', 'Standard_D1_v2'),
        ('Standard_D2_v2', 'Standard_D2_v2'),
        ('Standard_D3_v2', 'Standard_D3_v2'),
        ('Standard_D4_v2', 'Standard_D4_v2'),
        ('Standard_D5_v2', 'Standard_D5_v2'),
        ('Standard_D11_v2', 'Standard_D11_v2'),
        ('Standard_D12_v2', 'Standard_D12_v2'),
        ('Standard_D13_v2', 'Standard_D13_v2'),
        ('Standard_D14_v2', 'Standard_D14_v2'),
        ('Standard_DS1', 'Standard_DS1'),
        ('Standard_DS2', 'Standard_DS2'),
        ('Standard_DS3', 'Standard_DS3'),
        ('Standard_DS4', 'Standard_DS4'),
        ('Standard_DS11', 'Standard_DS11'),
        ('Standard_DS12', 'Standard_DS12'),
        ('Standard_DS13', 'Standard_DS13'),
        ('Standard_DS14', 'Standard_DS14'),
        ('Standard_G1', 'Standard_G1'),
        ('Standard_G2', 'Standard_G2'),
        ('Standard_G3', 'Standard_G3'),
        ('Standard_G4', 'Standard_G4'),
        ('Standard_G5', 'Standard_G5'),

    )

    location_choices = (
        ('Central US', 'Central US - Iowa'),
        ('East US', 'East US - Virginia'),
        ('East US 2', 'East US 2 - Virginia'),
        ('North Central US', 'North Central US - Illinois'),
        ('South Central US', 'South Central US - Texas'),
        ('West US', 'West US - California'),
        ('North Europe', 'North Europe - Ireland'),
        ('West Europe', 'West Europe - Netherlands'),
        ('East Asia', 'East Asia - Hong Kong'),
        ('Southeast Asia', 'Southeast Asia - Singapore'),
        ('Japan East', 'Japan East - Tokyo, Saitama'),
        ('Japan West', 'Japan West - Osaka'),
        ('Brazil South', 'Brazil South - Sao Paulo'),
        ('Australia East', 'Australia East - New South Wales'),
        ('Australia Southeast', 'Australia Southeast - Victoria'),
        ('Central India', 'Central India - Pune'),
        ('South India', 'South India - Chennai'),
        ('West India', 'West India - Mumbai'),
    )

    name = forms.CharField(label='Name', max_length=25, required=False)
    image_id = forms.ChoiceField(choices=image_choices, required=False, label='Image Id')
    vm_size = forms.ChoiceField(choices=flavor_choices, required=False, label='VM Size')
    location = forms.ChoiceField(choices=location_choices, required=False)
    number = forms.CharField(label='Number', max_length=2, required=False)
    #password = forms.CharField(label='Password', max_length=12, required=False)
    #cloud_service_name = forms.CharField(label='Cloud Service Name', max_length=12, required=False)
    #storage_account_name = forms.CharField(label='Storage Account Name', max_length=12, required=False)
    tcp_endpoints = forms.CharField(label='TCP Endpoints', max_length=12, required=False)


class CreateClusterStep2(forms.Form):

    name = forms.CharField(label='Name', max_length=25, required=False, widget=forms.HiddenInput())
    image_id = forms.CharField(label='Image Id', max_length=125, required=False, widget=forms.HiddenInput())
    vm_size = forms.CharField(label='VM Size', max_length=25, required=False, widget=forms.HiddenInput())
    location = forms.CharField(label='Location', max_length=12, required=False, widget=forms.HiddenInput())
    number = forms.CharField(label='Number', max_length=2, required=False, widget=forms.HiddenInput())
    #password = forms.CharField(label='Password', max_length=12, required=False, widget=forms.HiddenInput())
    #cloud_service_name = forms.CharField(label='Cloud Service Name', max_length=12, required=False)
    #storage_account_name = forms.CharField(label='Storage Account Name', max_length=12, required=False)
    tcp_endpoints = forms.CharField(label='TCP Endpoints', max_length=12, required=False, widget=forms.HiddenInput())
    roles = forms.CharField(label='Roles', max_length=40, required=False)
    runlist = forms.CharField(label='Runlist', max_length=40, required=False)

