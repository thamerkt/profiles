from django.db import models

# Improvement: Remove unused imports and comments, use consistent naming, and improve field types and relationships.

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}, {self.postal_code}"


class DocumentType(models.Model):
    name = models.CharField(max_length=255)
    file_format = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)
    required_for = models.IntegerField()

    def __str__(self):
        return self.name


class Profil(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    # Improvement: Use OneToOneField for user relation, assuming integration with custom user model
    user_id = models.CharField(max_length=255, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_profil = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PhysicalProfil(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    # Improvement: Use OneToOneField for unique relation
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE, related_name="physical_profile", null=True, blank=True)

    def __str__(self):
        return f"{self.profil} - {self.get_gender_display() if self.gender else 'N/A'}"


class ProfilMoral(models.Model):
    raison_social = models.CharField(max_length=255)
    numero_immatriculation = models.CharField(max_length=255)
    matricule_fiscale = models.CharField(max_length=255)
    registre_commerce = models.CharField(max_length=255)
    contact_responsable = models.CharField(max_length=255)
    business_email = models.EmailField(max_length=255, null=True, blank=True)
    forme_juridique = models.CharField(max_length=255)
    secteur_activite = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    
    # Improvement: Use OneToOneField for unique relation
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE, related_name="moral_profile", null=True, blank=True)

    def __str__(self):
        return self.raison_social


class Document(models.Model):
    document_name = models.CharField(max_length=255)
    document_url = models.URLField(max_length=255)
    status = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.document_name
