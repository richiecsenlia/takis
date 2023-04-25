from django.http import HttpResponse
from django.test import TestCase

import json
from django_cas_ng.signals import cas_user_authenticated
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from authentication.views import admin_required, ta_required, ta_role_check, admin_role_check
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.test import RequestFactory
from django.contrib.auth.hashers import check_password
from accounts.models import TeachingAssistantProfile, MataKuliah

# Create your tests here.
class AuthTest(TestCase):
    
    DUMMY = {
        "nama":"richie senlia"
    }
    LOGIN_URL = reverse("authentication:login")
    REGISTER_URL = reverse("authentication:register")
    CHANGE_PASSWORD_URL = reverse("authentication:change_password")
    CHANGE_ROLE_URL = reverse("authentication:change_role")
    UPDATE_ROLE_URL = "authentication:update_role"
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='username', password='password', email='username@test.com'
        )
        self.factory = RequestFactory()

        self.admin_user = User.objects.create(username='admin', password='admin', email='admin@admin.com')
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        self.na_user = User.objects.create(username='na', password='na', email='na@na.com')
        self.na_user.role.role = 'not-assign'
        self.na_user.role.save()

        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()

    def test_sso_login_url_exist(self):
        response = self.client.get(reverse("authentication:ssologin"))
        self.assertEquals(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.CAS_SERVER_URL))
        
    
    def test_sso_logout_url_exist(self):
        response = self.client.get(reverse("authentication:ssologout"))
        self.assertEquals(response.status_code,302)
        self.assertTrue(response.url.startswith(settings.CAS_SERVER_URL))
    
    def test_get_login(self):
        response = self.client.get(self.LOGIN_URL)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.templates[0].name,"registration/login.html")
    
    def test_login_success(self):
        response = self.client.post(self.LOGIN_URL, {'username': 'username', 'password': 'password'})
        self.assertEquals(response.status_code,302)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response,reverse("main:homepage"))
    
    def test_login_unsuccessfull(self):
        response = self.client.post(self.LOGIN_URL, {'username': 'username', 'password': 'password2'})
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.templates[0].name,"registration/login.html")
    def test_login_authenticated_user(self):
        self.client.login(username="username",password="password")
        response = self.client.get(self.LOGIN_URL)
        self.assertRedirects(response,reverse('main:homepage'))
    
    def test_get_register(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.templates[0].name,"registration/register.html")

    def test_get_register_authenticated_user(self):
        self.client.login(username="username",password="password")
        response = self.client.get(self.REGISTER_URL)
        self.assertRedirects(response,reverse('main:homepage'))
    
    def test_register_success(self):
        response = self.client.post(self.REGISTER_URL, {'username': 'richie5', 'password1': 'senlia25','password2':'senlia25'})
        self.assertEquals(response.status_code,302)
        user = User.objects.filter(username="richie5")
        self.assertTrue(len(user)==1)
        self.assertRedirects(response,self.LOGIN_URL)
    
    def test_register_fail(self):
        response = self.client.post(self.REGISTER_URL,{'username':'richie','password1':'richie','password2':'richie'})
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.templates[0].name,"registration/register.html")
    
    def test_change_password_new_user(self):
        user = User.objects.create(username='richie',email='richie@gmail.com')
        self.client.force_login(user=user)
        response = self.client.get(self.CHANGE_PASSWORD_URL)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.templates[0].name,"registration/change_password.html")

    
    def test_change_password_post_success(self):
        user = User.objects.create(username='richie',email='richie@gmail.com')
        user.role.role = "TA"
        self.client.force_login(user=user)
        response = self.client.post(self.CHANGE_PASSWORD_URL,{'password1':"senlia25",'password2':'senlia25'})
        client_user = auth.get_user(self.client)
        self.assertTrue(check_password("senlia25",client_user.password))
        self.assertTrue(client_user.is_authenticated)
        self.assertRedirects(response,reverse("main:homepage"))

    def test_change_password_no_user(self):
        response = self.client.get(self.CHANGE_PASSWORD_URL,fetch_redirect_response=False)
        self.assertRedirects(response,self.LOGIN_URL,fetch_redirect_response=False)
    
    def test_change_role_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.CHANGE_ROLE_URL)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.templates[0].name,"registration/change_role.html")

    def test_change_role_ta_user(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(self.CHANGE_ROLE_URL)
        self.assertEquals(response.status_code,403)
    def test_update_role(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(self.UPDATE_ROLE_URL,kwargs={'id':1,'role':'TA'}))
        user = User.objects.get(id=1)
        self.assertEquals(user.role.role,'TA')
        self.assertRedirects(response,self.CHANGE_ROLE_URL)
    def test_update_role_user_not_found(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(self.UPDATE_ROLE_URL,kwargs={'id':10,'role':'TA'}))
        self.assertInHTML('user tidak ditemukan',response.content.decode())
    
    def test_update_role_ta_user(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(self.UPDATE_ROLE_URL,kwargs={'id':10,'role':'TA'}))
        self.assertEquals(response.status_code,403)
    
    def test_create_role(self):
        user = User.objects.create(username='username2', password='password2', email='username@test.com2')
        self.assertEquals(user.role.role,"not-assign")

    def test_user_can_save_data_from_cas(self):
        """Test if Profile model can save the attributes from CAS."""
        cas_user_authenticated.send(
            sender=self,
            user=self.user,
            created=False,
            attributes=AuthTest.DUMMY
        )
        self.assertEquals(self.user.email, f"{self.user.username}@ui.ac.id")
        self.assertEquals(self.user.first_name, "richie")
        self.assertEquals(self.user.last_name, "senlia")

    def test_ta_role_check_if_user_is_ta(self):
        res = ta_role_check(self.ta_user)
        self.assertTrue(res)

    def test_ta_role_check_if_user_is_not_ta(self):
        self.assertRaises(PermissionDenied, ta_role_check, user=self.admin_user)
        self.assertRaises(PermissionDenied, ta_role_check, user=self.na_user)

    def test_admin_role_check_if_user_is_admin(self):
        res = admin_role_check(self.admin_user)
        self.assertTrue(res)

    def test_admin_role_check_if_user_is_not_admin(self):
        self.assertRaises(PermissionDenied, admin_role_check, user=self.ta_user)
        self.assertRaises(PermissionDenied, admin_role_check, user=self.na_user)
    
    def test_ta_required_if_user_is_not_authenticated(self):
        @ta_required
        def dummy_view(request):
            return HttpResponse()
        
        request = self.factory.get('/foo')
        request.user = AnonymousUser()
        res = dummy_view(request)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse('authentication:login')+'?next=/foo')

    def test_ta_required_if_user_is_not_ta(self):
        @ta_required
        def dummy_view(request):
            return HttpResponse()
        
        request = self.factory.get('/foo')
        request.user = self.admin_user
        self.assertRaises(PermissionDenied, dummy_view, request=request)

    def test_ta_required_if_user_is_ta(self):
        @ta_required
        def dummy_view(request):
            return HttpResponse()
        
        request = self.factory.get('/foo')
        request.user = self.ta_user
        res = dummy_view(request)
        self.assertEqual(res.status_code, 200)

    def test_admin_required_if_user_is_not_authenticated(self):
        @admin_required
        def dummy_view(request):
            return HttpResponse()
        
        request = self.factory.get('/foo')
        request.user = AnonymousUser()
        res = dummy_view(request)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse('authentication:login')+'?next=/foo')

    def test_admin_required_if_user_is_not_admin(self):
        @admin_required
        def dummy_view(request):
            return HttpResponse()
        
        request = self.factory.get('/foo')
        request.user = self.ta_user
        self.assertRaises(PermissionDenied, dummy_view, request=request)

    def test_admin_required_if_user_is_admin(self):
        @admin_required
        def dummy_view(request):
            return HttpResponse()
        
        request = self.factory.get('/foo')
        request.user = self.admin_user
        res = dummy_view(request)
        self.assertEqual(res.status_code, 200)

    def test_filter_user_change_role(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('authentication:change_role'))
        self.assertEquals(response.context['kontrak_choices'], TeachingAssistantProfile.kontrak.field.choices)
        self.assertEquals(response.context['status_choices'], TeachingAssistantProfile.status.field.choices)
        self.assertEquals(response.context['prodi_choices'], TeachingAssistantProfile.prodi.field.choices)
