from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import LogTA
from .views import *
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser

# Create your tests here.

context_dict = {
            'kategori' : "Penyelenggaraan Kuliah",
            'pekerjaan' : "Membuat Soal",
            'detail_kegiatan' : "Essay dan Pilgan",
            'pemberi_tugas' : "Ibu Ika Alfina",
            'uraian' : "Membuat soal PR",
            'periode' : "Semester Kuliah",
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "4",
            'satuan_kinerja' : "Tugas",
            'jam_rencana_kinerja' : "4"
        }
class PengisianLogTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()

        self.admin_user = User.objects.create(username='admin', password='admin', email='admin@admin.com')
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        self.na_user = User.objects.create(username='na', password='na', email='na@na.com')
        self.na_user.role.role = 'not-assign'
        self.na_user.role.save()

    def test_create_LogTA(self):
        logTA_1 = LogTA.objects.create(
            user = self.ta_user,
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            periode = "Semester Kuliah",
            bulan_pengerjaan = "MAR",
            jumlah_rencana_kinerja = 4,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 1,
            jumlah_realisasi_kinerja = 0,
            satuan_realisasi_kinerja = "",
            konversi_jam_realisasi_kinerja = 0
        )

        logTA_2 = LogTA.objects.create(
            user = self.ta_user,
            kategori = "Persiapan Kuliah",
            jenis_pekerjaan = "Mempersiapkan Environment",
            detail_kegiatan = "SCELE",
            pemberi_tugas = "Ibu Putu",
            uraian = "Rapat persiapan",
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 2,
            jumlah_realisasi_kinerja = 0,
            satuan_realisasi_kinerja = "",
            konversi_jam_realisasi_kinerja = 0
        )

        all_logTA = LogTA.objects.all()
        
        self.assertEquals(all_logTA.count(), 2)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertEquals(all_logTA[1].kategori, "Persiapan Kuliah")

    def test_create_LogTA_with_realisasi(self):
        logTA_1 = LogTA.objects.create(
            user = self.ta_user,
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            periode = "Semester Kuliah",
            bulan_pengerjaan = "MAR",
            jumlah_rencana_kinerja = 4,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 1,
            jumlah_realisasi_kinerja = 8,
            satuan_realisasi_kinerja = "Tugas",
            konversi_jam_realisasi_kinerja = 2
        )

        logTA_2 = LogTA.objects.create(
            user = self.ta_user,
            kategori = "Persiapan Kuliah",
            jenis_pekerjaan = "Mempersiapkan Environment",
            detail_kegiatan = "SCELE",
            pemberi_tugas = "Ibu Putu",
            uraian = "Rapat persiapan",
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 2,
            jumlah_realisasi_kinerja = 2,
            satuan_realisasi_kinerja = "Tugas",
            konversi_jam_realisasi_kinerja = 2
        )

        all_logTA = LogTA.objects.all()
        
        self.assertEquals(all_logTA.count(), 2)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertEquals(all_logTA[1].kategori, "Persiapan Kuliah")

    def test_display_form_LogTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:form-log-kerja"))

        self.assertTemplateUsed(response, 'form_log.html')
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_display_form_LogTA_unregistered(self):
        response = self.client.get(reverse("pengisianLog:form-log-kerja"))

        self.assertEqual(response.status_code, 302)

    def test_post_form_logTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.post(reverse("pengisianLog:form-log-kerja"), context_dict)

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 1)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertTemplateUsed(response, 'daftarLogTA.html')

    def test_post_form_logTA_as_unregistered(self):
        response = self.client.post(reverse("pengisianLog:form-log-kerja"), context_dict)

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 0)
        self.assertEqual(response.status_code, 302)
    
    def test_view_LogTA_response_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse('pengisianLog:daftarLogTA'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftarLogTA.html')
    
    def test_view_LogTA_response_as_evaluator(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('pengisianLog:daftarLogEvaluator'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftarLogEvaluator.html')
