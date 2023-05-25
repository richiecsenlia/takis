from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import MataKuliah, TeachingAssistantProfile
from periode.models import Periode, PeriodeSekarang

URL_HOMEPAGE = "main:homepage"
URL_NOT_ASSIGNED = "/auth/not-assign/"
URL_ADMIN = "/dashboard/"
URL_TA_WITHOUT_PROFILE = "/getting-started/"
URL_TA_WITH_PROFILE = "/log/daftar-log/"

class AccountsTest(TestCase):
    
    def setUp(self):
        self.ta_user_1 = User.objects.create_user(
            username = 'testta1',
            password = 'ta111',
            email = 'testta1@example.com'
        )
        self.ta_user_1.role.role = 'TA'
        self.ta_user_1.role.save()

        self.ta_user_2 = User.objects.create_user(
            username = 'testta2',
            password = 'ta222',
            email = 'testta2@example.com'
        )
        self.ta_user_2.role.role = 'TA'
        self.ta_user_2.role.save()

        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        self.na_user = User.objects.create_user(
            username='testna',
            password='na123',
            email='testna@example.com'
        )
        self.na_user.role.role = 'not-assign'
        self.na_user.role.save()

        self.matkul_1 = MataKuliah.objects.create(nama='Proyek Perangkat Lunak')

        self.ta_profile_1 = TeachingAssistantProfile.objects.create(
            user = self.ta_user_1,
            nama = 'Immanuel Nadeak',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Ilmu Komputer'
        )
        self.ta_profile_1.daftar_matkul.add(self.matkul_1)
        self.ta_profile_1.save()

        self.periode = Periode(
            tahun_ajaran = "2022/2023",
            semester = "ganjil"
        )
        self.periode.save()

        self.periode_sekarang = PeriodeSekarang(periode = self.periode)
        self.periode_sekarang.save()

    def test_display_homepage_with_guest_user(self):
        response = self.client.get(reverse(URL_HOMEPAGE))

        self.assertEqual(response.status_code, 302)

    def test_display_homepage_with_notassigned_user(self):
        self.client.force_login(user=self.na_user)
        response = self.client.get(reverse(URL_HOMEPAGE))

        self.assertEqual(response.url, URL_NOT_ASSIGNED)

    def test_display_homepage_with_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(URL_HOMEPAGE))

        self.assertEqual(response.url, URL_ADMIN)

    def test_display_homepage_with_new_ta_user(self):
        self.client.force_login(user=self.ta_user_2)
        response = self.client.get(reverse(URL_HOMEPAGE))

        self.assertEqual(response.url, URL_TA_WITHOUT_PROFILE)

    def test_display_homepage_with_ta_user_has_profile(self):
        self.client.force_login(user=self.ta_user_1)
        response = self.client.get(reverse(URL_HOMEPAGE))

        self.assertEqual(response.url, URL_TA_WITH_PROFILE)