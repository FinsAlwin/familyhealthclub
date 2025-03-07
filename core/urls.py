from django.urls import path
from . import views
from django.views.generic import RedirectView
from .views import DoctorDetailView, ProcedureCreateView, ProcedureUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='family_list')),
    path('register/', views.register, name='register'),
    path('family/', views.FamilyMemberListView.as_view(), name='family_list'),
    path('family/add/', views.FamilyMemberCreateView.as_view(), name='family_add'),
    path('family/<int:pk>/edit/', views.FamilyMemberUpdateView.as_view(), name='family_edit'),
    path('family/<int:pk>/delete/', views.FamilyMemberDeleteView.as_view(), name='family_delete'),
    path('family/<int:pk>/', views.FamilyMemberDetailView.as_view(), name='family_detail'),
    path('family/<int:family_member_id>/procedures/add/', 
         ProcedureCreateView.as_view(), name='procedure_add'),
    path('family/<int:family_member_id>/report/', views.generate_report, name='generate_report'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/add/', views.DoctorCreateView.as_view(), name='doctor_add'),
    path('doctors/<int:pk>/edit/', views.DoctorUpdateView.as_view(), name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('procedures/<int:pk>/edit/', 
         ProcedureUpdateView.as_view(), name='procedure_edit'),
    path('procedures/<int:pk>/delete/', views.ProcedureDeleteView.as_view(), name='procedure_delete'),
    path('medications/', views.MedicationListView.as_view(), name='medication_list'),
    path('medications/add/<int:family_member_id>/', views.MedicationCreateView.as_view(), name='medication_add'),
    path('medications/<int:pk>/edit/', views.MedicationUpdateView.as_view(), name='medication_edit'),
    path('medications/<int:pk>/delete/', views.MedicationDeleteView.as_view(), name='medication_delete'),
    path('insurance/', views.InsuranceListView.as_view(), name='insurance_list'),
    path('insurance/add/', views.InsuranceCreateView.as_view(), name='insurance_add'),
    path('insurance/<int:pk>/edit/', views.InsuranceUpdateView.as_view(), name='insurance_edit'),
    path('insurance/<int:pk>/delete/', views.InsuranceDeleteView.as_view(), name='insurance_delete'),
    path('treatments/', views.TreatmentListView.as_view(), name='treatment_list'),
    path('treatments/add/', views.TreatmentCreateView.as_view(), name='treatment_add'),
    path('treatments/<int:pk>/edit/', views.TreatmentUpdateView.as_view(), name='treatment_edit'),
    path('treatments/<int:pk>/delete/', views.TreatmentDeleteView.as_view(), name='treatment_delete'),
    path('labtests/', views.LabTestListView.as_view(), name='labtest_list'),
    path('labtests/add/<int:family_member_id>/', views.LabTestCreateView.as_view(), name='labtest_add'),
    path('labtests/<int:pk>/edit/', views.LabTestUpdateView.as_view(), name='labtest_edit'),
    path('labtests/<int:pk>/delete/', views.LabTestDeleteView.as_view(), name='labtest_delete'),
    path('expenses/', views.MedicalExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', views.MedicalExpenseCreateView.as_view(), name='expense_add'),
    path('expenses/<int:pk>/edit/', views.MedicalExpenseUpdateView.as_view(), name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.MedicalExpenseDeleteView.as_view(), name='expense_delete'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/add/', views.PrescriptionCreateView.as_view(), name='prescription_add'),
    path('prescriptions/<int:pk>/edit/', views.PrescriptionUpdateView.as_view(), name='prescription_edit'),
    path('prescriptions/<int:pk>/delete/', views.PrescriptionDeleteView.as_view(), name='prescription_delete'),
    path('medicalexpenses/add/<int:family_member_id>/', views.MedicalExpenseCreateView.as_view(), name='medicalexpense_add'),
    path('logout/', LogoutView.as_view(), name='logout'),
]