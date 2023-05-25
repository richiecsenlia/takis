from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import MataKuliah, TeachingAssistantProfile
from periode.models import Periode, PeriodeSekarang

URL_FILL_PROFIL = "accounts:fill_profile"
URL_VIEW_PROFIL = "accounts:profile"
URL_EDIT_PROFIL = "accounts:edit_profile"
URL_DAFTAR_LOG_TA = "pengisianLog:daftar_log_ta"

NAMA = 'Muhammad Hafidz'
KONTRAK = "Part Time"
STATUS = "Lulus S2 MTI"
PRODI = "Teknologi Informasi"
MATKUL = "SDA"
BULAN = 'SEP'
BULAN_ALT = 'DES'

fill_profile_context = {
    'nama': NAMA,
    'kontrak': KONTRAK,
    'status': STATUS,
    'prodi': PRODI,
}

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

        self.ta_user_3 = User.objects.create_user(
            username = 'testta3',
            password = 'ta333',
            email = 'testta3@example.com'
        )
        self.ta_user_3.role.role = 'TA'
        self.ta_user_3.role.save()

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
        self.matkul_2 = MataKuliah.objects.create(nama='Jaringan Komunikasi Data')
        self.matkul_3 = MataKuliah.objects.create(nama='Struktur Data Algoritma')

        self.ta_profile_1 = TeachingAssistantProfile.objects.create(
            user = self.ta_user_1,
            nama = 'Immanuel Nadeak',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Ilmu Komputer'
        )
        self.ta_profile_1.daftar_matkul.add(self.matkul_1)
        self.ta_profile_1.save()

        self.ta_profile_2 = TeachingAssistantProfile.objects.create(
            user = self.ta_user_2,
            nama = 'Virdian Harun',
            kontrak = 'Full Time',
            status = 'Lulus S2',
            prodi = 'Sistem Informasi'
        )
        self.ta_profile_2.daftar_matkul.add(self.matkul_2)
        self.ta_profile_2.save()

        self.periode = Periode(
            tahun_ajaran = "2022/2023",
            semester = "ganjil"
        )
        self.periode.save()

        self.periode_sekarang = PeriodeSekarang(periode = self.periode)
        self.periode_sekarang.save()
        
    def test_create_matakuliah(self):
        all_matkul = MataKuliah.objects.all()
        expected_matkul = "Proyek Perangkat Lunak"

        self.assertEquals(all_matkul.count(), 3)
        self.assertEquals(all_matkul[0].nama, expected_matkul)

    def test_create_ta_profile(self):
        all_ta_profile = TeachingAssistantProfile.objects.all()
        expected_ta_1_name = "Immanuel Nadeak"
        expected_ta_2_name = "Virdian Harun"

        self.assertEquals(all_ta_profile.count(), 2)
        self.assertEquals(str(all_ta_profile.get(id=1)), expected_ta_1_name)
        self.assertEquals(str(all_ta_profile.get(id=2)), expected_ta_2_name)

    def test_display_fill_profile_if_user_has_no_profile(self):
        self.client.force_login(user=self.ta_user_3)
        response = self.client.get(reverse(URL_FILL_PROFIL))

        self.assertTemplateUsed(response, 'accounts/fill_profile.html')

    def test_fill_profile_as_new_ta(self):
        self.client.force_login(user=self.ta_user_3)
        response = self.client.post(reverse(URL_FILL_PROFIL), fill_profile_context)

        all_ta_profile = TeachingAssistantProfile.objects.all()

        self.assertEquals(all_ta_profile.count(), 2)

    def test_display_profile_as_ta(self):
        self.client.force_login(user=self.ta_user_1)
        response = self.client.get(reverse(URL_VIEW_PROFIL, args=[self.ta_user_1.id]))
        profile = response.context['profile']

        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.nama, 'Immanuel Nadeak')

    def test_display_profile_as_evaluator(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(URL_VIEW_PROFIL, args=[self.ta_user_2.id]))
        profile = response.context['profile']

        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(profile.nama, 'Virdian Harun')

    def test_display_profile_as_not_assigned_user(self):
        self.client.force_login(user=self.na_user)
        response = self.client.get(reverse(URL_VIEW_PROFIL, args=[self.ta_user_1.id]))

        self.assertEqual(response.status_code, 302)

    def test_display_edit_profile_as_ta(self):
        self.client.force_login(user=self.ta_user_1)
        response = self.client.get(reverse(URL_EDIT_PROFIL, kwargs={'id':1}))
        profile = response.context['profile']

        self.assertTemplateUsed(response, 'accounts/edit_profile.html')
        self.assertEqual(profile.nama, 'Immanuel Nadeak')

    def test_dashboard(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse("accounts:dashboard_eval"),{"kontrak":'Part Time','status':'Lulus S1','prodi':'Ilmu Komputer'})
        self.assertEquals(response.templates[0].name,'accounts/dashboard_eval.html')

    def test_dashboard_bulan(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse("accounts:dashboard_eval"),{"kontrak":'Part Time','status':'Lulus S1','prodi':'Ilmu Komputer','bulan':'JAN'})
        self.assertEquals(response.templates[0].name,'accounts/dashboard_eval.html')
