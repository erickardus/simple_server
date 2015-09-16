from django import forms


class Server(forms.Form):

    image_choices = (
        ('ami-d5c5d1e5', 'Amazon Linux AMI 2015.03.1 (HVM), SSD Volume Type'),
        ('ami-4dbf9e7d', 'Red Hat Enterprise Linux 7.1 (HVM), SSD Volume Type'),
        ('ami-d7450be7', 'SUSE Linux Enterprise Server 12 (HVM), SSD Volume Type'),
        ('ami-5189a661', 'Ubuntu Server 14.04 LTS (HVM), SSD Volume Type'),
    )

    flavor_choices = (
        ('t2.micro', 't2.micro'),
        ('t2.small', 't2.small'),
        ('t2.medium', 't2.medium'),
        ('t2.large', 't2.large'),
    )

    name = forms.CharField(label='Name', max_length=25, required=True)
    #image = forms.CharField(label='Image Id', max_length=12, required=True, initial='ami-d5c5d1e5')
    image = forms.ChoiceField(choices=image_choices, required=True, label='Image Id')
    #flavor = forms.CharField(label='Flavor', max_length=12, required=True, initial='t2.micro')
    flavor = forms.ChoiceField(choices=flavor_choices, required=True, label='Flavor')

class Software(forms.Form):

    name = forms.CharField(label='Name', max_length=25, required=True)
    image = forms.CharField(label='Image Id', max_length=25, required=True)
    flavor = forms.CharField(label='Flavor', max_length=25, required=True)
    runlist = forms.CharField(label='Runlist', max_length=25, required=True)