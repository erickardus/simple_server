from django import forms


class CreateClusterStep1(forms.Form):

    image_choices = (
        ('b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150706-en-us-30GB',
         'Ubuntu 14.04 LTS AMD64 Server EN_US 30GB'),
    )

    flavor_choices = (
        ('Standard_D1', 'Standard_D1'),

    )

    name = forms.CharField(label='Name', max_length=25, required=False)
    image_id = forms.ChoiceField(choices=image_choices, required=False, label='Image Id')
    vm_size = forms.ChoiceField(choices=flavor_choices, required=False, label='VM Size')
    location = forms.CharField(label='Location', max_length=12, required=False)
    number = forms.CharField(label='Number', max_length=2, required=False)
    password = forms.CharField(label='Password', max_length=12, required=False)
    cloud_service_name = forms.CharField(label='Cloud Service Name', max_length=12, required=False)
    storage_account_name = forms.CharField(label='Storage Account Name', max_length=12, required=False)
    tcp_endpoints = forms.CharField(label='TCP Endpoints', max_length=12, required=False)


class CreateClusterStep2(forms.Form):

    name = forms.CharField(label='Name', max_length=25, required=False, widget=forms.HiddenInput())
    image_id = forms.CharField(label='Image Id', max_length=25, required=False, widget=forms.HiddenInput())
    vm_size = forms.CharField(label='VM Size', max_length=25, required=False, widget=forms.HiddenInput())
    location = forms.CharField(label='Location', max_length=12, required=False, widget=forms.HiddenInput())
    number = forms.CharField(label='Number', max_length=2, required=False, widget=forms.HiddenInput())
    password = forms.CharField(label='Password', max_length=12, required=False, widget=forms.HiddenInput())
    cloud_service_name = forms.CharField(label='Cloud Service Name', max_length=12, required=False, widget=forms.HiddenInput())
    storage_account_name = forms.CharField(label='Storage Account Name', max_length=12, required=False, widget=forms.HiddenInput())
    tcp_endpoints = forms.CharField(label='TCP Endpoints', max_length=12, required=False, widget=forms.HiddenInput())
    roles = forms.CharField(label='Roles', max_length=40, required=False)
    runlist = forms.CharField(label='Runlist', max_length=40, required=False)

