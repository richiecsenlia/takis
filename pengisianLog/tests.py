from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import LogTA
from .views import *
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

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
            'jam_rencana_kinerja' : "4",
            'jumlah_realisasi_kinerja' : "4",
            'satuan_realisasi_kinerja' : "Tugas",
            'konversi_jam_realisasi_kinerja' : "4"
        }

context_dict_updated = {
            'kategori' : "Riset dan Pusilkom",
            'pekerjaan' : "Membuat Soal",
            'detail_kegiatan' : "Essay dan Pilgan",
            'pemberi_tugas' : "Ibu Ika Alfina",
            'uraian' : "Membuat soal PR",
            'periode' : "Semester Kuliah",
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "4",
            'satuan_kinerja' : "Tugas",
            'jam_rencana_kinerja' : "4",
            'jumlah_realisasi_kinerja' : "4",
            'satuan_realisasi_kinerja' : "Tugas",
            'konversi_jam_realisasi_kinerja' : "4"
        }

context_wrong = {
            'kategori' : "Penyelenggaraan Kuliah",
            'pekerjaan' : "Membuat Soal",
            'detail_kegiatan' : "Essay dan Pilgan",
            'pemberi_tugas' : "Ibu Ika Alfina",
            'uraian' : "Membuat soal PR",
            'periode' : "Semester Kuliah",
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "Empat",
            'satuan_kinerja' : "Tugas",
            'jam_rencana_kinerja' : "Empat",
            'jumlah_realisasi_kinerja' : "Empat",
            'satuan_realisasi_kinerja' : "Tugas",
            'konversi_jam_realisasi_kinerja' : "Empat"
        }

context_wrong_updated = {
            'kategori' : "Riset dan Pusilkom",
            'pekerjaan' : "Membuat Soal",
            'detail_kegiatan' : "Essay dan Pilgan",
            'pemberi_tugas' : "Ibu Ika Alfina",
            'uraian' : "Membuat soal PR",
            'periode' : "Semester Kuliah",
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "Empat",
            'satuan_kinerja' : "Tugas",
            'jam_rencana_kinerja' : "Empat",
            'jumlah_realisasi_kinerja' : "Empat",
            'satuan_realisasi_kinerja' : "Tugas",
            'konversi_jam_realisasi_kinerja' : "Empat"
        }

HISTORY_LOG_URL = "pengisianLog:history_log"

        
class PengisianLogTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()

        self.ta_user_2 = User.objects.create(username='ta2', password='ta2', email='ta2@ta2.com')
        self.ta_user_2.role.role = 'TA'
        self.ta_user_2.role.save()

        self.admin_user = User.objects.create(username='admin', password='admin', email='admin@admin.com')
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        self.na_user = User.objects.create(username='na', password='na', email='na@na.com')
        self.na_user.role.role = 'not-assign'
        self.na_user.role.save()

        self.logTA_1 = LogTA.objects.create(
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
            konversi_jam_rencana_kinerja = 1
        )

        self.logTA_2 = LogTA.objects.create(
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
            konversi_jam_rencana_kinerja = 2
        )

    # Test membuat log TA
    def test_create_LogTA(self):
        all_logTA = LogTA.objects.all()
        
        self.assertEquals(all_logTA.count(), 2)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertEquals(all_logTA[1].kategori, "Persiapan Kuliah")

    def test_create_LogTA_with_realisasi(self):
        self.logTA_1.jumlah_realisasi_kinerja = 8
        self.logTA_1.satuan_realisasi_kinerja = "Tugas"
        self.logTA_1.konversi_jam_realisasi_kinerja = 2
        self.logTA_1.save()

        self.logTA_2.jumlah_realisasi_kinerja = 2
        self.logTA_2.satuan_realisasi_kinerja = "Tugas"
        self.logTA_2.konversi_jam_realisasi_kinerja = 2
        self.logTA_2.save()

        all_logTA = LogTA.objects.all()
        
        self.assertEquals(all_logTA.count(), 2)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertEquals(all_logTA[1].kategori, "Persiapan Kuliah")

    def test_display_form_LogTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:mengisi_log"))

        self.assertTemplateUsed(response, 'form_log.html')
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_display_form_LogTA_unregistered(self):
        response = self.client.get(reverse("pengisianLog:mengisi_log"))

        self.assertEqual(response.status_code, 302)

    def test_post_form_logTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.post(reverse("pengisianLog:mengisi_log"), context_dict)

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 3)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertEquals(all_logTA[2].konversi_jam_rencana_kinerja, all_logTA[2].jumlah_rencana_kinerja / 4)
        self.assertEquals(all_logTA[2].konversi_jam_realisasi_kinerja, all_logTA[2].jumlah_realisasi_kinerja / 4)
        self.assertRedirects(response, reverse("pengisianLog:daftar_log_ta"))

    def test_post_form_logTA_as_TA_wrong_input(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.post(reverse("pengisianLog:mengisi_log"), context_wrong)

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 2)
        self.assertTemplateUsed(response, 'form_log.html')

    def test_post_form_logTA_as_unregistered(self):
        response = self.client.post(reverse("pengisianLog:mengisi_log"), context_dict)

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 2)
        self.assertEqual(response.status_code, 302)
    
    # Test melihat log TA
    def test_view_LogTA_response_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse('pengisianLog:daftar_log_ta'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftar_log.html')
    
    def test_view_LogTA_response_as_evaluator(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('pengisianLog:daftar_log_evaluator'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftar_log.html')
    

    def test_view_history_log_as_registered(self):
        self.client.force_login(user=self.admin_user)

        old_category = self.logTA_1.kategori
        new_category = "Dukungan Kuliah Kakak Asuh"
        self.logTA_1.kategori = new_category
        self.logTA_1.save()

        response = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':self.logTA_1.id}))
        histories_response = response.context['history']

        self.assertEqual(histories_response.count(), 2)
        self.assertEqual(histories_response[0].kategori, new_category)
        self.assertEqual(histories_response[1].kategori, old_category)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history_log.html')

    def test_view_history_log_history_user(self):
        self.client.force_login(user=self.ta_user)
        self.logTA_1.kategori = "Dukungan Kuliah Kakak Asuh"
        self.logTA_1._history_user = self.ta_user
        self.logTA_1.save()

        self.client.login(user=self.admin_user)
        self.logTA_1.kategori = "Riset dan Pusilkom"
        self.logTA_1._history_user = self.admin_user
        self.logTA_1.save()

        response = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':self.logTA_1.id}))
        histories_response = response.context['history']

        self.assertEqual(histories_response[1].history_user, self.ta_user)
        self.assertEqual(histories_response[0].history_user, self.admin_user)

    def test_view_history_log_as_unregistered(self):
        
        response = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 
                         reverse('authentication:login')+'?next='+reverse(HISTORY_LOG_URL, 
                                                                          kwargs={'id':self.logTA_1.id}))
        
    def test_view_history_missing_log(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':8000}))
        self.assertEqual(response.status_code, 404)
        
    def test_view_history_log_only_correspoinding_ta_or_admin(self):
        self.client.force_login(user=self.ta_user)
        self.logTA_1.save()

        response_ta_user = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response_ta_user.status_code, 200)

        self.client.force_login(user=self.ta_user_2)
        response_ta_user_2 = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response_ta_user_2.status_code, 403)

        self.client.force_login(user=self.admin_user)
        response_admin = self.client.get(reverse(HISTORY_LOG_URL, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response_admin.status_code, 200)

    def test_filter_LogTA_response_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse('pengisianLog:daftar_log_ta'))
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_filter_LogTA_response_as_evaluator(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('pengisianLog:daftar_log_evaluator'))
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_filter_LogTA_response_TA_context(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse('pengisianLog:daftar_log_ta'),{"bulan":"JAN","kategori":"Harian","periode":"Persiapan Kuliah"})
        self.assertEquals(response.context['filter_kategori'][0], "Harian")
        self.assertEquals(response.context['filter_periode'][0], "Persiapan Kuliah")
        self.assertEquals(response.context['filter_bulan'][0], "JAN")
        
    # Test edit log TA
    def test_display_form_edit_log_ta_as_ta(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:edit_log", kwargs={'id':1}))
        log = response.context["log"]

        self.assertTemplateUsed(response, 'edit_log.html')
        self.assertEquals(response.context['kategori_choice'], [kategori for kategori in LogTA.kategori.field.choices if log.kategori not in kategori])
        self.assertEquals(response.context['periode_choice'], [periode for periode in LogTA.periode.field.choices if log.periode not in periode])
        self.assertEquals(response.context['bulan_choice'], [bulan_pengerjaan for bulan_pengerjaan in LogTA.bulan_pengerjaan.field.choices if log.bulan_pengerjaan not in bulan_pengerjaan])

    def test_display_form_edit_log_ta_unregistered(self):
        response = self.client.get(reverse("pengisianLog:edit_log", kwargs={'id':1}))

        self.assertEqual(response.status_code, 302)

    def test_post_form_edit_log_ta_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:edit_log", kwargs={'id':1}))

        response = self.client.post(reverse("pengisianLog:edit_log", kwargs={'id':1}), context_dict_updated)
        response_updated = self.client.get(reverse("pengisianLog:edit_log", kwargs={'id':1}))

        updated_log = response_updated.context["log"]
        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 2)
        self.assertEquals(updated_log.kategori, "Riset dan Pusilkom")
        self.assertEquals(all_logTA[0].konversi_jam_rencana_kinerja, all_logTA[0].jumlah_rencana_kinerja / 4)
        self.assertEquals(all_logTA[0].konversi_jam_realisasi_kinerja, all_logTA[0].jumlah_realisasi_kinerja / 4)
        self.assertRedirects(response, reverse("pengisianLog:daftar_log_ta"))

    def test_post_form_edit_log_ta_as_ta_wrong_input(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:edit_log", kwargs={'id':1}))

        self.client.post(reverse("pengisianLog:edit_log", kwargs={'id':1}), context_dict_updated)
        response = self.client.get(reverse("pengisianLog:edit_log", kwargs={'id':1}))

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 2)
        self.assertTemplateUsed(response, 'edit_log.html')

    def test_post_form_edit_log_ta_as_unregistered(self):
        response = self.client.post(reverse("pengisianLog:edit_log", kwargs={'id':1}))

        all_logTA = LogTA.objects.all()

        self.assertEquals(all_logTA.count(), 2)
        self.assertEqual(response.status_code, 302)
    
    def test_delete_log_ta(self):
        self.client.force_login(user=self.ta_user)
        self.client.post(reverse("pengisianLog:delete_log", kwargs={'id':1}))

        all_logTA = LogTA.objects.all()
        self.assertEquals(all_logTA.count(), 1)
    
    def test_detail_log_ta_authorized(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:detail_log", kwargs={'id':1}))

        self.assertTemplateUsed(response, 'detail_log.html')

    def test_detail_log_ta_unauthorized(self):
        self.client.force_login(user=self.ta_user_2)
        response = self.client.get(reverse("pengisianLog:detail_log", kwargs={'id':1}))
        
        self.assertEqual(response.status_code, 403)

