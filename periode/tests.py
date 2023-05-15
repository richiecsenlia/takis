from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from .models import Periode, PeriodeSekarang

# Create your tests here.
TAHUN_AJARAN = "2022/2023"
TAHUN_AJARAN_ALT = "2023/2024"
TAHUN_AJARAN_WRONG_FORMAT = "2019-2020"
TAHUN_AJARAN_WRONG_TIME = "2019/2029"
SEMESTER = 'Ganjil'

BUAT_PERIODE_URL = "periode:buat_periode"
EDIT_PERIODE_SEKARANG_URL = "periode:edit_periode_sekarang"
URL_DAFTAR_TA_PER_PERIODE = "periode:daftar_ta"

create_context = {
    'tahun_ajaran' : TAHUN_AJARAN,
    'semester' : SEMESTER,
}

wrong_format_create_context = {
    'tahun_ajaran' : TAHUN_AJARAN_WRONG_FORMAT,
    'semester' : SEMESTER,
}

wrong_time_create_context = {
    'tahun_ajaran' : TAHUN_AJARAN_WRONG_TIME,
    'semester' : SEMESTER,
}


class PeriodeTestCase(TestCase):
    def setUp(self):
        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()

        self.admin_user = User.objects.create(username='admin', password='admin', email='admin@admin.com')
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        self.na_user = User.objects.create(username='na', password='na', email='na@na.com')
        self.na_user.role.role = 'not-assign'
        self.na_user.role.save()

        self.periode = Periode(
            tahun_ajaran = TAHUN_AJARAN,
            semester = SEMESTER,
        )

        self.periode_alt = Periode(
            tahun_ajaran = TAHUN_AJARAN_ALT,
            semester = SEMESTER,
        )


    def test_get_periode_form_as_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(BUAT_PERIODE_URL))

        self.assertTemplateUsed(response, 'buat_periode.html')
        self.assertContains(response, 'form', status_code=200)

    def test_get_periode_form_as_nonadmin(self):
        response = self.client.get(reverse(BUAT_PERIODE_URL))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 
                         reverse('authentication:login')+'?next='+reverse(BUAT_PERIODE_URL))

        self.client.force_login(user=self.ta_user)
        response_ta_user_2 = self.client.get(reverse(BUAT_PERIODE_URL))
        self.assertEqual(response_ta_user_2.status_code, 403)

    def test_create_periode(self):
        self.client.force_login(user=self.admin_user)
        self.client.post(reverse(BUAT_PERIODE_URL), create_context)
        all_periode = Periode.objects.all()

        self.assertEquals(all_periode.count(), 1)
        self.assertEquals(all_periode[0].tahun_ajaran, TAHUN_AJARAN)
        self.assertEquals(all_periode[0].semester, SEMESTER)

    def test_create_wrong_periode(self):
        self.client.force_login(user=self.admin_user)
        self.client.post(reverse(BUAT_PERIODE_URL), wrong_format_create_context)
        all_periode = Periode.objects.all()

        self.assertRaises(ValidationError)
        self.assertEquals(all_periode.count(), 0)

        self.client.post(reverse(BUAT_PERIODE_URL), wrong_time_create_context)
        all_periode = Periode.objects.all()

        self.assertRaises(ValidationError)
        self.assertEquals(all_periode.count(), 0)

    def test_get_edit_periode_sekarang_form_as_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(EDIT_PERIODE_SEKARANG_URL))

        self.assertTemplateUsed(response, 'edit_periode_sekarang.html')
        self.assertContains(response, 'form', status_code=200)

    def test_get_edit_periode_form_as_nonadmin(self):
        response = self.client.get(reverse(EDIT_PERIODE_SEKARANG_URL))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 
                         reverse('authentication:login')+'?next='+reverse(EDIT_PERIODE_SEKARANG_URL))

        self.client.force_login(user=self.ta_user)
        response_ta_user_2 = self.client.get(reverse(EDIT_PERIODE_SEKARANG_URL))
        self.assertEqual(response_ta_user_2.status_code, 403)

    def test_edit_periode_sekarang(self):
        self.periode.save()
        self.periode_alt.save()

        edit_context = {
            'periode' : self.periode.id
        }

        self.client.force_login(user=self.admin_user)
        self.client.post(reverse(EDIT_PERIODE_SEKARANG_URL), edit_context)
        periode_sekarang = PeriodeSekarang.objects.all()

        self.assertEquals(periode_sekarang.count(), 1)
        self.assertEquals(periode_sekarang[0].periode, self.periode)

        edit_context = {
            'periode' : self.periode_alt.id
        }

        self.client.post(reverse(EDIT_PERIODE_SEKARANG_URL), edit_context)
        periode_sekarang = PeriodeSekarang.objects.all()

        self.assertEquals(periode_sekarang.count(), 1)
        self.assertEquals(periode_sekarang[0].periode, self.periode_alt)

    # Tes melihat daftar TA per periode
    def test_view_list_response_evaluator(self):
        self.periode.save()
        periode_context = {
            'periode' : self.periode.id
        }

        self.client.force_login(user=self.admin_user)
        self.client.post(reverse(EDIT_PERIODE_SEKARANG_URL), periode_context)
        
        response = self.client.get(reverse(URL_DAFTAR_TA_PER_PERIODE))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftar_ta.html')
    
    def test_view_list_response_unauthorized(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_DAFTAR_TA_PER_PERIODE))
        self.assertEqual(response.status_code, 403)

    # Tes assign TA per periode
