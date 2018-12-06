# from rest_framework import viewsets, response, status, permissions
# from rest_framework.decorators import list_route
# # from rest_framework import authentication, permissions

# from dashboard import models, serializers
# from vibe_user.models import (
#             UserDefaultMember,
#         )


# class PersonalInfoViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.PersonalInfoSerializer
#     default_user_member = None 

#     def initial(self, request, *args, **kwargs):
#         self.default_user_member = UserDefaultMember.objects.get(user=self.request.user) 
#         super().initial(request, args, kwargs)
#         request.data.update({
#             "creator": str(self.request.user.pk),
#             "member": self.default_user_member.member.id
#         })

#     def get_queryset(self):
#         return models.PersonalInfo.objects.filter(member=self.default_user_member.member)

#     @list_route(methods=["POST"])
#     def bulk_delete(self, request, *args, **kwargs):
#         """
#         send a list of ids to delete with the format 
#         payload = {
#                     ids : [
#                     "069b8ec1-5030-4333-92a4-22c80050e08c",
#                     "229qwss1-5we0-4333-92a4-2eweeew0e08c"
#                     ]
#                 }
#         """
#         ids = request.data.get('ids')

#         models.PersonalInfo.objects.filter(id__in=ids).delete()

#         return response.Response(status=status.HTTP_202_ACCEPTED)


# class RelationInfoViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.RelationInfoSerializer
#     default_user_member = None 

#     def initial(self, request, *args, **kwargs):
#         super().initial(request, args, kwargs)
#         self.default_user_member = UserDefaultMember.objects.get(user=self.request.user) 
#         request.data.update({
#             "creator": str(self.request.user.pk),
#             "member": self.default_user_member.member.id
#         })

#     def get_queryset(self):
#         return models.RelationInfo.objects.filter(member=self.default_user_member.member)

#     @list_route(methods=["POST"])
#     def bulk_delete(self, request, *args, **kwargs):
#         """
#         send a list of ids to delete with the format 
#         payload = {
#                     ids : [
#                     "069b8ec1-5030-4333-92a4-22c80050e08c",
#                     "229qwss1-5we0-4333-92a4-2eweeew0e08c"
#                     ]
#                 }
#         """
#         ids = request.data.get('ids')

#         models.RelationInfo.objects.filter(id__in=ids).delete()

#         return response.Response(status=status.HTTP_202_ACCEPTED)


# class AddressInfoViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.AddressInfoSerializer
#     default_user_member = None 

#     def initial(self, request, *args, **kwargs):
#         super().initial(request, args, kwargs)
#         self.default_user_member = UserDefaultMember.objects.get(user=self.request.user) 
#         request.data.update({
#             "creator": str(self.request.user.pk),
#             "member": self.default_user_member.member.id
#         })

#     def get_queryset(self):
#         return models.AddressInfo.objects.filter(member=self.default_user_member.member)

#     @list_route(methods=["POST"])
#     def bulk_delete(self, request, *args, **kwargs):
#         """
#         send a list of ids to delete with the format 
#         payload = {
#                     ids : [
#                     "069b8ec1-5030-4333-92a4-22c80050e08c",
#                     "229qwss1-5we0-4333-92a4-2eweeew0e08c"
#                     ]
#                 }
#         """
#         ids = request.data.get('ids')

#         models.AddressInfo.objects.filter(id__in=ids).delete()

#         # models.AddressInfo.objects.
#         return response.Response(status=status.HTTP_202_ACCEPTED)


# class ContactInfoViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.ContactInfoSerializer
#     default_user_member = None 

#     def initial(self, request, *args, **kwargs):
#         super().initial(request, args, kwargs)
#         self.default_user_member = UserDefaultMember.objects.get(user=self.request.user) 
#         request.data.update({
#             "creator": str(self.request.user.pk),
#             "member": self.default_user_member.member.id
#         })

#     def get_queryset(self):
#         return models.ContactInfo.objects.filter(member=self.default_user_member.member)

#     @list_route(methods=["POST"])
#     def bulk_delete(self, request, *args, **kwargs):
#         """
#         send a list of ids to delete with the format
#         payload = {
#                     ids : [
#                     "069b8ec1-5030-4333-92a4-22c80050e08c",
#                     "229qwss1-5we0-4333-92a4-2eweeew0e08c"
#                     ]
#                 }
#         """
#         ids = request.data.get('ids')

#         models.ContactInfo.objects.filter(id__in=ids).delete()

#         return response.Response(status=status.HTTP_202_ACCEPTED)


# class OrganisationViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.OrganisationSerializer
#     queryset = models.Organisation.objects.all()

#     def initial(self, request, *args, **kwargs):
#         super().initial(request, args, kwargs)
#         self.default_user_member = UserDefaultMember.objects.get(user=self.request.user) 
#         request.data.update({
#             "creator": str(self.request.user.pk)
#         })


# class FormViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.FormSerializer
#     # queryset = models.Form.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     default_user_member = None 
    
#     def initial(self, request, *args, **kwargs):
#         super().initial(request, args, kwargs)
#         self.default_user_member = UserDefaultMember.objects.get(user=self.request.user) 
#         request.data.update({
#             "creator": str(self.request.user.pk),
#             "member": self.default_user_member.member.id
#         })


#     def get_queryset(self):
#         return models.Form.objects.filter(member=self.default_user_member.member)

#     # def perform_create(self, serializer):
#     #     serializer.save(
#     #         ) 

#         # import pdb; pdb.set_trace()
