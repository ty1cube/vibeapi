from rest_framework import viewsets, status, exceptions, generics
from rest_framework.authtoken import views 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.utils.translation import ugettext_lazy as _
from .renderers import UserJSONRenderer,ProfileJSONRenderer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


from .models import (
        User,
        Profile,
        SignupCode,
        PasswordResetCode,
        UserDefaultMember,
        Member,
        VibespotMember,
    )


from .serializers import (
        MemberSerializer,
        UserSerializer,
        SignupSerializer,
        ProfileSerializer,
        PasswordResetSerializer,
        PasswordResetVerifiedSerializer,
        PasswordChangeSerializer,
        UserDefaultMemberSerializer,
        ArtistMemberSerializer,
        RecordMemberSerializer,
        VibespotMemberSerializer,
        # CountrySerializer,
        # OrganisationSerializer,
    )



def send_notifation_email(template_prefix, template_ctxt, target_email):

    subject_file = 'vibespot/%s_subject.txt' % template_prefix
    txt_file = 'vibespot/%s.txt' % template_prefix
    html_file = 'vibespot/%s.html' % template_prefix

    subject = render_to_string(subject_file).strip()
    from_email = settings.DEFAULT_EMAIL_FROM
    to = target_email
    # bcc_email = settings.DEFAULT_EMAIL_BCC
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



class CustomAuthToken(views.ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_verified:
            return Response({
                    "errors": "Please check your inbox for verification link"
                }, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user' : {
                'user_id': user.pk,
                'username': user.username,
                'email': user.email
            }
        })

def signup_successful_email(request, user):
    ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')
    signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
    signup_code.send_signup_email()

class CreateArtistMemberView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        data={}
        data.update({"member_type": "A"})
        data.update({"is_member_admin": True})
        data.update(request.data)

        signup_serializer = SignupSerializer(data=data)
        signup_serializer.is_valid(raise_exception=True)
        name = request.data.get("name")

        try:
            Member.objects.get(name=name, member_type="A")
            return Response(
                    {"errors": "Artist name already exist"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Member.DoesNotExist:
            pass

        signup_serializer.save()

        data.update({"creator": signup_serializer.data.get("id")})
        member_serializer = MemberSerializer(data=data)

        if not member_serializer.is_valid():
            User.objects.get(email=request.data.get("email")).delete()
            return Response(
                    member_serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        member_serializer.save()

        # data.update({"user": signup_serializer.data.get("id")})
        # data.update({"member": member_serializer.data.get("name")})

        # assignment_serializer = \
        #         VibespotMemberSerializer(data=data)

        # if not assignment_serializer.is_valid():
        #     User.objects.get(email=request.data.get("email")).delete()
        #     return Response(
        #             assignment_serializer.errors, 
        #             status=status.HTTP_400_BAD_REQUEST
        #             )

        # assignment_serializer.save()

        try:
            # signup_successful_email(request, User.objects.get(email=request.data.get("email")))
            pass
        except Exception:
            User.objects.get(email=request.data.get("email")).delete()
            return Response({
                'message': "Registration failed. Try again",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': "Sign up successful. Check your inbox for verification link",
            }, status=status.HTTP_201_CREATED)




class CreateRecordMemberView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        data={}
        data.update({"member_type": "R"})
        data.update({"is_member_admin": True})
        data.update(request.data)

        data.update({"name": request.data.get("name")})

        signup_serializer = SignupSerializer(data=data)
        signup_serializer.is_valid(raise_exception=True)

        name = request.data.get("name")
        # org_name = request.data.get("org_name")
        # org_password = request.data.get("org_password")

        try:
            Member.objects.get(name=name, space_type="R")
            return Response(
                    {"errors": "Record Manager name already exist"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Member.DoesNotExist:
            pass


        # organisation = None
        # try:
        #     organisation = Organisation.objects.get(name=org_name,
        #             org_password=org_password)
        # except Organisation.DoesNotExist:
        #     return Response(
        #             {"errors": "Organisation credentials provided is invalid"}, 
        #             status=status.HTTP_400_BAD_REQUEST
        #         )

        # data.update({"organisation": organisation.name})
        # signup_serializer = SignupSerializer(data=data)
        # signup_serializer.is_valid(raise_exception=True)
        # signup_serializer.save()


        # data.update({"creator": signup_serializer.data.get("id")})
        # data.update({"organisation": org_name})

        # space_serializer = SpaceSerializer(data=data)

        # if not space_serializer.is_valid():
        #     User.objects.get(email=request.data.get("email")).delete()
        #     return Response(
        #             space_serializer.errors, 
        #             status=status.HTTP_400_BAD_REQUEST
        #         )

        # space_serializer.save()



        # data.update({"user": signup_serializer.data.get("id")})
        # data.update({"space": space_serializer.data.get("name")})

        # assignment_serializer = \
        #         SpaceMemberSerializer(data=data)

        # if not assignment_serializer.is_valid():
        #     User.objects.get(email=request.data.get("email")).delete()
        #     return Response(
        #             assignment_serializer.errors, 
        #             status=status.HTTP_400_BAD_REQUEST
        #             )

        # assignment_serializer.save()

        try:
            # signup_successful_email(request, User.objects.get(email=request.data.get("email")))
            pass
        except Exception:
            User.objects.get(email=request.data.get("email")).delete()
            return Response({
                '}message': "Registration failed. Try again",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': "Sign up successful. Check your inbox for verification link",
            }, status=status.HTTP_201_CREATED)



   
# class JoinArtistMemberView(views.APIView):
#     permission_classes = (permissions.AllowAny,)
    
#     def post(self, request, name, *args, **kwargs):

#         data={}

#         data.update({"member_type": "A"})
#         data.update(request.data)

#         signup_serializer = SignupSerializer(data=data)
#         signup_serializer.is_valid(raise_exception=True)

#         member = None

#         try:
#             member = member.objects.get(
#                     name=name, member_type="A"
#                 )
#         except member.DoesNotExist:
#             return Response(
#                     {"errors": "personal space does not exist"}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         signup_serializer.save()


#         data.update({"user": signup_serializer.data.get("id")})
#         data.update({"member": member.name})

#         assignment_serializer = \
#                 VibespotMemberSerializer(data=data)

#         if not assignment_serializer.is_valid():
#             User.objects.get(email=request.data.get("email")).delete()
#             return Response(
#                     assignment_serializer.errors, 
#                     status=status.HTTP_400_BAD_REQUEST
#                     )

#         assignment_serializer.save()



#         try:
#             signup_successful_email(request, User.objects.get(email=request.data.get("email")))
#             ctxt = {
#                 'admin_username': member.creator.username,
#                 'member_username': request.data.get("username") 
#             }
#             send_notifation_email("join_space_email", ctxt, member.creator.email)
#         except Exception as e:
#             User.objects.get(email=request.data.get("email")).delete()
#             return Response({
#                 'message': "Registration failed. Try again",
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({
#             'message': "Sign up successful. Check your inbox for verification link",
#             }, status=status.HTTP_201_CREATED)



# class JoinRecordMemberView(views.APIView):
#     permission_classes = (permissions.AllowAny,)
    
#     def post(self, request, name, *args, **kwargs):

#         data={}

#         data.update({"member_type": "R"})
#         data.update(request.data)

#         signup_serializer = SignupSerializer(data=data)
#         signup_serializer.is_valid(raise_exception=True)

#         member = None

#         try:
#             member = member.objects.get(name=name, member_type="R")
#         except member.DoesNotExist:
#             return Response(
#                     {"errors": "organisation space does not exist"}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         signup_serializer.save()



#         # data.update({"user": signup_serializer.data.get("id")})
#         # data.update({"space": member.name})

#         # assignment_serializer = \
#         #         VibespotMemberSerializer(data=data)

#         # if not assignment_serializer.is_valid():
#         #     User.objects.get(email=request.data.get("email")).delete()
#         #     return Response(
#         #             assignment_serializer.errors, 
#         #             status=status.HTTP_400_BAD_REQUEST
#         #         )

#         # assignment_serializer.save()

#         try:
#             signup_successful_email(request, User.objects.get(email=request.data.get("email")))
#             ctxt = {
#                 'admin_username': member.creator.username,
#                 'member_username': request.data.get("username") 
#             }
#             send_notifation_email("join_space_email", ctxt, member.creator.email)
#         except Exception:
#             User.objects.get(email=request.data.get("email")).delete()
#             return Response({
#                 'message': "Registration failed. Try again",
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({
#             'message': "Sign up successful. Check your inbox for verification link",
#             }, status=status.HTTP_201_CREATED)


class UserDefaultMemberView(generics.RetrieveAPIView):
    serializer_class = UserDefaultMemberSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, user):
        try:
            return UserDefaultMember.objects.get(user=user)
        except UserDefaultMember.DoesNotExist:
            raise Http404
    
    def get(self, request, format=None):
        user_member = self.get_object(request.user)
        serializer = UserDefaultMemberSerializer(user_member)
        return Response(serializer.data) 


class GetUserArtistMemberView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArtistMemberSerializer

    def get_queryset(self):
        return VibespotMember.objects.filter(
                user=self.request.user, member_type="A"
            )


class GetUserRecordMemberView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RecordMemberSerializer

    def get_queryset(self):
        return VibespotMember.objects.filter(
                user=self.request.user, member_type="R"
            )


# class PersonalWorkspaceView(viewsets.ModelViewSet):
#     queryset   = PersonalWorkspace.objects.all()
#     serializer_class = PersonalWorkspaceSerializer
#
#
# class OrganisationWorkspaceView(viewsets.ModelViewSet):
#     queryset   = OrganisationWorkspace.objects.all()
#     serializer_class = OrganisationWorkspaceSerializer


class UserView(viewsets.ModelViewSet):
    queryset   = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(viewsets.ModelViewSet):
    queryset   = Profile.objects.all()
    serializer_class = ProfileSerializer


class SignupVerify(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        code = request.GET.get('code', '')
        verified = SignupCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=code)
                signup_code.delete()
            except SignupCode.DoesNotExist:
                pass
            content = {'success': _('User verified.')}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'detail': _('Unable to verify user.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class Logout(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Remove all auth tokens owned by request.user.
        """
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {'success': _('User logged out.')}
        return Response(content, status=status.HTTP_200_OK)


class PasswordReset(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = User.objects.get(email=email)
                if user.is_verified and user.is_active:
                    password_reset_code = \
                        PasswordResetCode.objects.create_reset_code(user)
                    password_reset_code.send_password_reset_email()
                    content = {'email': email}
                    return Response(content, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                pass

            # Since this is AllowAny, don't give away error.
            content = {'detail': _('Password reset not allowed.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerify(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        code = request.GET.get('code', '')

        try:
            password_reset_code = PasswordResetCode.objects.get(code=code)
            content = {'success': _('User verified.')}
            return Response(content, status=status.HTTP_200_OK)
        except PasswordResetCode.DoesNotExist:
            content = {'detail': _('Unable to verify user.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerified(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetVerifiedSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # code = serializer.data['code']
            # password = serializer.data['password']
            code = request.data.get("code")
            password = request.data.get("password")

            try:
                password_reset_code = PasswordResetCode.objects.get(code=code)
                password_reset_code.user.set_password(password)
                password_reset_code.user.save()
                content = {'success': _('Password reset.')}
                return Response(content, status=status.HTTP_200_OK)
            except PasswordResetCode.DoesNotExist:
                content = {'detail': _('Unable to verify user.')}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user

            password = serializer.data['password']
            user.set_password(password)
            user.save()

            content = {'success': _('Password changed.')}
            return Response(content, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
