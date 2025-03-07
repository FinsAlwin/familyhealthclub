from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FamilyMember, Doctor, Procedure, Medication, Insurance, Treatment, LabTest, MedicalExpense, Prescription
from .forms import FamilyMemberForm, DoctorForm, ProcedureForm, LabTestForm
import requests
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login

def generate_report(request, family_member_id):
    family_member = FamilyMember.objects.get(id=family_member_id, user=request.user)
    procedures = Procedure.objects.filter(family_member=family_member)
    prompt = f"Medical history for {family_member.name}:\n"
    for p in procedures:
        prompt += f"- {p.name} on {p.date}: {p.description}\n"

    # Replace with actual API details
    api_url = "https://api.example.com/generate"
    response = requests.post(api_url, json={"prompt": prompt, "api_key": "YOUR_API_KEY"})
    report = response.json().get("report", "Report generation failed.")

    return render(request, 'report.html', {'report': report})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, 'This application is for educational purposes only. Commercial use is prohibited.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.warning(request, 'This application is for educational purposes only. Commercial use is prohibited.')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

class FamilyMemberListView(LoginRequiredMixin, ListView):
    model = FamilyMember
    template_name = 'family_list.html'
    context_object_name = 'family_members'

    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)

class FamilyMemberCreateView(LoginRequiredMixin, CreateView):
    model = FamilyMember
    form_class = FamilyMemberForm
    template_name = 'family_member_form.html'
    success_url = '/family/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FamilyMemberDetailView(LoginRequiredMixin, DetailView):
    model = FamilyMember
    template_name = 'family_member_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedures'] = Procedure.objects.filter(family_member=self.object)
        context['labtests'] = LabTest.objects.filter(family_member=self.object)
        return context

class ProcedureCreateView(LoginRequiredMixin, CreateView):
    model = Procedure
    form_class = ProcedureForm
    template_name = 'procedure_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        family_member = FamilyMember.objects.get(
            id=self.kwargs['family_member_id'],
            user=self.request.user
        )
        form.instance.family_member = family_member
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('family_detail', args=[self.kwargs['family_member_id']])

class FamilyMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = FamilyMember
    form_class = FamilyMemberForm
    template_name = 'family_member_form.html'
    success_url = '/family/'

class FamilyMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = FamilyMember
    template_name = 'family_member_confirm_delete.html'
    success_url = '/family/'

class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctor_list.html'

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor_form.html'
    success_url = '/doctors/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor_form.html'
    success_url = '/doctors/'

class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'doctor_confirm_delete.html'
    success_url = '/doctors/'

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'

class ProcedureUpdateView(LoginRequiredMixin, UpdateView):
    model = Procedure
    form_class = ProcedureForm
    template_name = 'procedure_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('family_detail', args=[self.object.family_member_id])

class ProcedureDeleteView(LoginRequiredMixin, DeleteView):
    model = Procedure
    template_name = 'procedure_confirm_delete.html'
    success_url = '/family/'

class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'medication_list.html'

    def get_queryset(self):
        return Medication.objects.filter(family_member__user=self.request.user)

class MedicationCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    template_name = 'medication_form.html'
    fields = ['family_member', 'name', 'dosage', 'frequency', 'start_date', 'end_date']
    success_url = '/medications/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['family_member'].queryset = FamilyMember.objects.filter(user=self.request.user)
        return form

class MedicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Medication
    template_name = 'medication_form.html'
    fields = ['family_member', 'name', 'dosage', 'frequency', 'start_date', 'end_date']
    success_url = '/medications/'

class MedicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Medication
    template_name = 'medication_confirm_delete.html'
    success_url = '/medications/'

class InsuranceListView(LoginRequiredMixin, ListView):
    model = Insurance
    template_name = 'insurance_list.html'

    def get_queryset(self):
        return Insurance.objects.filter(user=self.request.user)

class InsuranceCreateView(LoginRequiredMixin, CreateView):
    model = Insurance
    template_name = 'insurance_form.html'
    fields = ['provider', 'policy_number', 'coverage_details']
    success_url = '/insurance/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class InsuranceUpdateView(LoginRequiredMixin, UpdateView):
    model = Insurance
    template_name = 'insurance_form.html'
    fields = ['provider', 'policy_number', 'coverage_details']
    success_url = '/insurance/'

class InsuranceDeleteView(LoginRequiredMixin, DeleteView):
    model = Insurance
    template_name = 'insurance_confirm_delete.html'
    success_url = '/insurance/'

class TreatmentCreateView(LoginRequiredMixin, CreateView):
    model = Treatment
    fields = ['family_member', 'name', 'start_date', 'end_date', 'description']
    template_name = 'treatment_form.html'
    success_url = '/family/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['family_member'].queryset = FamilyMember.objects.filter(user=self.request.user)
        return form

class LabTestCreateView(LoginRequiredMixin, CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'labtest_form.html'

    def get_initial(self):
        initial = super().get_initial()
        family_member = FamilyMember.objects.get(id=self.kwargs['family_member_id'])
        initial['family_member'] = family_member
        return initial

    def get_success_url(self):
        return reverse('family_detail', kwargs={'pk': self.kwargs['family_member_id']})

class MedicalExpenseCreateView(LoginRequiredMixin, CreateView):
    model = MedicalExpense
    fields = ['date', 'amount', 'description', 'related_to']
    template_name = 'medicalexpense_form.html'
    success_url = '/expenses/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MedicalExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalExpense
    fields = ['date', 'amount', 'description', 'related_to']
    template_name = 'medicalexpense_form.html'
    success_url = '/expenses/'

class MedicalExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalExpense
    template_name = 'medicalexpense_confirm_delete.html'
    success_url = '/expenses/'

class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['family_member', 'file']
    template_name = 'prescription_form.html'
    success_url = '/family/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['family_member'].queryset = FamilyMember.objects.filter(user=self.request.user)
        return form

class PrescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescription
    fields = ['family_member', 'file']
    template_name = 'prescription_form.html'
    success_url = '/prescriptions/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['family_member'].queryset = FamilyMember.objects.filter(user=self.request.user)
        return form

class PrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescription
    template_name = 'prescription_confirm_delete.html'
    success_url = '/prescriptions/'

class TreatmentListView(LoginRequiredMixin, ListView):
    model = Treatment
    template_name = 'treatment_list.html'

    def get_queryset(self):
        return Treatment.objects.filter(family_member__user=self.request.user)

class LabTestListView(LoginRequiredMixin, ListView):
    model = LabTest
    template_name = 'labtest_list.html'

    def get_queryset(self):
        return LabTest.objects.filter(family_member__user=self.request.user)

class MedicalExpenseListView(LoginRequiredMixin, ListView):
    model = MedicalExpense
    template_name = 'medicalexpense_list.html'

    def get_queryset(self):
        return MedicalExpense.objects.filter(user=self.request.user)

class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'prescription_list.html'

    def get_queryset(self):
        return Prescription.objects.filter(family_member__user=self.request.user)

class TreatmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Treatment
    fields = ['family_member', 'name', 'start_date', 'end_date', 'description']
    template_name = 'treatment_form.html'
    success_url = '/treatments/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['family_member'].queryset = FamilyMember.objects.filter(user=self.request.user)
        return form

class TreatmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Treatment
    template_name = 'treatment_confirm_delete.html'
    success_url = '/treatments/'

class LabTestUpdateView(LoginRequiredMixin, UpdateView):
    model = LabTest
    fields = ['family_member', 'name', 'date', 'result']
    template_name = 'labtest_form.html'
    success_url = '/labtests/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['family_member'].queryset = FamilyMember.objects.filter(user=self.request.user)
        return form

class LabTestDeleteView(LoginRequiredMixin, DeleteView):
    model = LabTest
    template_name = 'labtest_confirm_delete.html'
    success_url = '/labtests/'
    

