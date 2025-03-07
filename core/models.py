from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Family Member Model
class FamilyMember(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    RELATIONSHIP_CHOICES = [
        ('Self', 'Self'),
        ('Spouse', 'Spouse'),
        ('Child', 'Child'),
        ('Parent', 'Parent'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    relationship = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES)

    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.name

# Doctor Model
class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

# Procedure Model
class Procedure(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name

# Treatment Model
class Treatment(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name

# Medication Model
class Medication(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

# Lab Test Model
class LabTest(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    result = models.TextField()

    def __str__(self):
        return self.name

# Insurance Model
class Insurance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage_details = models.TextField()

    def __str__(self):
        return self.provider

# Medical Expense Model
class MedicalExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    related_to = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description} - {self.amount}"

# Prescription Model
class Prescription(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='prescriptions/')

    def __str__(self):
        return f"Prescription for {self.family_member.name}"