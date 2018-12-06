# import uuid

# from django.db import models
# from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _

# # Create your models here.

# class BaseModel(models.Model):
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_on = models.DateTimeField(default=timezone.now, editable=False)
#     modified = models.DateTimeField(auto_now=True, blank=True, null=True)
#     creator = models.ForeignKey('vibe_user.User', on_delete=models.CASCADE, blank=True, null=True)

#     class Meta:
#         abstract = True


# class PersonalInfo(BaseModel):

#     member = models.ForeignKey("vibe_user.Member", on_delete=models.CASCADE, default="")
#     title = models.ForeignKey("vibe_user.Title", on_delete=models.CASCADE, blank=True, null=True)
#     first_name = models.CharField(_('first name'), max_length=50)
#     last_name = models.CharField(_('last name'), max_length=50)
#     other_names = models.CharField(
#         _("other names"), max_length=50, blank=True, null=True
#     )
#     date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
#     date_of_death = models.DateField(_('date of death'), blank=True, null=True)
#     birth_place = models.CharField(_('birth place'), max_length=50, blank=True, null=True)
#     birth_country = models.ForeignKey("vibe_user.Country", on_delete=models.CASCADE, blank=True, null=True)
#     eye_color = models.ForeignKey("vibe_user.EyeColor", on_delete=models.CASCADE, blank=True, null=True)
#     ethnic_group = models.ForeignKey("vibe_user.EthnicGroups", on_delete=models.CASCADE, blank=True, null=True)
#     religion = models.ForeignKey("vibe_user.Religion", on_delete=models.CASCADE, blank=True, null=True)
#     sex = models.ForeignKey("vibe_user.Sex", on_delete=models.CASCADE, blank=True, null=True)
#     marital_status = models.ForeignKey("vibe_user.MaritalStatus", on_delete=models.CASCADE, blank=True, null=True)
#     marit_st_last_change = models.DateField(blank=True, null=True)
#     height =models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) 
#     height_unit = models.ForeignKey("vibe_user.HeightUnit", on_delete=models.CASCADE, blank=True, null=True)

#     class Meta:
#         db_table = 'person'

#     def __str__(self):
#         return "{} {}".format(self.first_name, self.last_name)


# class RelationInfo(BaseModel):

#     person = models.ForeignKey('dashboard.PersonalInfo', on_delete=models.CASCADE)
#     member = models.ForeignKey("vibe_user.Member", on_delete=models.CASCADE, default="")
#     relation_to = models.ForeignKey('dashboard.PersonalInfo', on_delete=models.CASCADE, related_name='relation_to')
#     relation_part= models.ForeignKey("vibe_user.RelationPart", on_delete=models.CASCADE, blank=True, null=True)
#     valid_from = models.DateField()
#     valid_to = models.DateField()

#     class Meta:
#         db_table = 'relation'
#         unique_together = ("member", "relation_to", "relation_part")


# class AddressInfo(BaseModel):

#     resident = models.ForeignKey('dashboard.PersonalInfo', on_delete=models.CASCADE)
#     member = models.ForeignKey("vibe_user.Member", on_delete=models.CASCADE, default="")
#     country = models.ForeignKey("vibe_user.Country", on_delete=models.CASCADE, blank=True, null=True)
#     state = models.CharField(max_length=10)
#     city = models.CharField(max_length=50)
#     local_muncipality = models.CharField(max_length=50, blank=True, null=True)
#     post_area = models.CharField(max_length=20, blank=True, null=True)
#     address_type = models.ForeignKey("vibe_user.AddressType", on_delete=models.CASCADE, blank=True, null=True)
#     address_type_identifier = models.CharField(max_length=50, blank=True, null=True)
#     street_name = models.CharField(max_length=100, blank=True, null=True)
#     street_no = models.IntegerField(default=0, blank=True, null=True) 
#     street_no_suffix = models.CharField(max_length=20, blank=True, null=True)
#     building_name = models.CharField(max_length=50, null=True, blank=True)
#     street_direction = models.ForeignKey("vibe_user.StreetDirection", on_delete=models.CASCADE, blank=True, null=True)
#     principal_indicator = models.BooleanField(default=False)
#     valid_from = models.DateField(blank=True, null=True)
#     valid_to = models.DateField(blank=True, null=True)

#     class Meta:
#         db_table = 'address'


# class ContactInfo(BaseModel):

#     person = models.ForeignKey('dashboard.PersonalInfo', on_delete=models.CASCADE)
#     member = models.ForeignKey("vibe_user.Member", on_delete=models.CASCADE, default="")
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     tel_number = models.CharField(max_length=20,blank=True, null=True)
#     tel_area_code = models.CharField(max_length=10,blank=True, null=True)
#     tel_country_code = models.CharField(max_length=5,blank=True, null=True)
#     website = models.CharField(max_length=256, blank=True, null=True)
#     address = models.ForeignKey('dashboard.AddressInfo', on_delete=models.CASCADE, blank=True, null=True)
#     contact_type = models.ForeignKey("vibe_user.ContactType", on_delete=models.CASCADE, blank=True, null=True)
#     active = models.BooleanField(default = True)

#     class Meta:
#         db_table = 'contact'


# class Organisation(models.Model):
#     name = models.CharField(max_length=20, primary_key=True)
#     org_password = models.CharField(max_length=20, blank=True, null=True)
#     creator = models.ForeignKey('vibe_user.User', on_delete=models.CASCADE, blank=True, null=True, related_name='creator')
#     legal_form = models.ForeignKey("vibe_user.LegalForm",on_delete=models.CASCADE, blank=True, null=True) 
#     org_class = models.ForeignKey("vibe_user.OrganisationClass",on_delete=models.CASCADE, blank=True, null=True)
#     org_type = models.ForeignKey("vibe_user.OrganisationType",on_delete=models.CASCADE, blank=True, null=True)
#     org_size = models.ForeignKey("vibe_user.OrganisationSize",on_delete=models.CASCADE, blank=True, null=True)
#     charitable = models.BooleanField(default=False)
#     foundation = models.DateField(blank=True, null=True)
#     liquidation = models.DateField(blank=True, null=True)
#     # org_area = models.CharField(max_length=100, blank=True, null=True) 
#     org_country = models.ForeignKey("vibe_user.Country", on_delete=models.CASCADE, blank=True, null=True)
#     org_certificate   = models.FileField(upload_to="./certificate", blank=True, null=True)
#     created_on = models.DateTimeField(default=timezone.now, editable=False)
#     modified = models.DateTimeField(auto_now=True, blank=True, null=True)

#     class Meta:
#         db_table = 'organization'


# class Form(BaseModel):

#     issuing_member = models.ForeignKey("vibe_user.Member", on_delete=models.CASCADE, default="")
#     form_type = models.ForeignKey("vibe_user.FormType", on_delete=models.CASCADE, blank=True, null=True)
#     language = models.ForeignKey("vibe_user.Language", on_delete=models.CASCADE, blank=True, null=True)
#     description = models.TextField(blank=True)
#     own_sign = models.TextField(blank=True)
#     valid_from = models.DateField(blank=True, null=True)
#     valid_to = models.DateField(blank=True, null=True)
#     creation_date = models.DateField(auto_now=True)
#     status = models.CharField(max_length=1,blank=True) #R/D release or draft
#     pdf_file = models.FileField(upload_to="./form", blank=True, null=True)

#     class Meta:
#         db_table = 'form'

#     def __str__(self):
#         return self.form_category
