from django import forms
from .models import FamilyMember, Doctor, Procedure, LabTest

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'date_of_birth', 'sex', 'relationship']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'contact_info']

class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['name', 'date', 'description', 'doctor']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['doctor'].queryset = Doctor.objects.filter(user=user)

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['family_member', 'name', 'date', 'result']