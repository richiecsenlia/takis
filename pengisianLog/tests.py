from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import LogTA
from accounts.models import TeachingAssistantProfile
from periode.models import Periode, PeriodeSekarang
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from accounts.models import MataKuliah, TeachingAssistantProfile
from periode.models import Periode, PeriodeSekarang

# Create your tests here.

PENYELENGGARAN_KULIAH = "Penyelengggaraan Kuliah"
MEMBUAT_SOAL = "Membuat Soal"
ESSAY_DAN_PILGAN = "Essay dan Pilgan"
IBU_IKA_ALFINA = "Ibu Ika Alfina"
MEMBUAT_SOAL_PR = "Membuat soal PR"
BASIS_DATA = "Basis Data"
DUKUNGAN_KULIAH_KAKAK_ASUH = "Dukungan Kuliah Kakak Asuh"
PERSIAPAN_KULIAH = "Persiapan Kuliah"
SEMESTER_KULIAH = "Semester Kuliah"
SEPANJANG_KONTRAK = "Sepanjang Kontrak"
RISET_DAN_PUSILKOM = "Riset dan Pusilkom"
URL_MENGISI_LOG = "pengisianLog:mengisi_log"
URL_DAFTAR_LOG_TA = "pengisianLog:daftar_log_ta"
URL_EDIT_LOG_TA = "pengisianLog:edit_log"
TAHUN_AJARAN = "2022/2023"
TAHUN_AJARAN_ALT = "2023/2024"
SEMESTER = 'Ganjil'
URL_DAFTAR_LOG_EVALUATOR = 'pengisianLog:daftar_log_evaluator'
URL_HISTORY_LOG = "pengisianLog:history_log"
URL_DASHBOARD_ADMIN = "accounts:dashboard_eval"
TAHUN_AJARAN = "2023/2024"
SEMESTER_TAHUN_AJARAN = "Genap"

context_dict_1 = {
            'kategori' : PENYELENGGARAN_KULIAH,
            'pekerjaan' : MEMBUAT_SOAL,
            'detail_kegiatan' : ESSAY_DAN_PILGAN,
            'pemberi_tugas' : IBU_IKA_ALFINA,
            'uraian' : MEMBUAT_SOAL_PR,
            'matkul' : BASIS_DATA,
            'periode' : SEMESTER_KULIAH,
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "4",
            'satuan_kinerja' : "Tugas",
            'bobot_kinerja' : "4",
            'jumlah_realisasi_kinerja' : "",
            'satuan_realisasi_kinerja' : "Tugas",
            'bobot_realisasi_kinerja' : ""
        }

context_dict_2 = {
            'kategori' : DUKUNGAN_KULIAH_KAKAK_ASUH,
            'pekerjaan' : "Mentorring",
            'detail_kegiatan' : "Zoom",
            'pemberi_tugas' : "Ibu Ara",
            'uraian' : "Melakukan mentorring kepada mentee",
            'matkul' : BASIS_DATA,
            'periode' : "Adhoc",
            'bulan_pengerjaan' : "JAN",
            'jumlah_kinerja' : "3",
            'satuan_kinerja' : "Jam",
            'bobot_kinerja' : "3",
            'jumlah_realisasi_kinerja' : "2",
            'satuan_realisasi_kinerja' : "Jam",
            'bobot_realisasi_kinerja' : "2"
        }

context_dict_3 = {
            'kategori' : DUKUNGAN_KULIAH_KAKAK_ASUH,
            'pekerjaan' : "Mentorring",
            'detail_kegiatan' : "Zoom",
            'pemberi_tugas' : "Ibu Ara",
            'uraian' : "Melakukan mentorring kepada mentee",
            'matkul' : BASIS_DATA,
            'periode' : SEPANJANG_KONTRAK,
            'bulan_pengerjaan' : "FEB",
            'jumlah_kinerja' : "5",
            'satuan_kinerja' : "tugas",
            'bobot_kinerja' : "2",
            'jumlah_realisasi_kinerja' : "6",
            'satuan_realisasi_kinerja' : "tugas",
            'bobot_realisasi_kinerja' : "1"
        }

context_dict_1_updated = {
            'kategori' : PENYELENGGARAN_KULIAH,
            'pekerjaan' : MEMBUAT_SOAL,
            'detail_kegiatan' : ESSAY_DAN_PILGAN,
            'pemberi_tugas' : "Ibu Ani",
            'uraian' : "Membuat soal ujian",
            'matkul' : BASIS_DATA,
            'periode' : SEMESTER_KULIAH,
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "3",
            'satuan_kinerja' : "Soal",
            'bobot_kinerja' : "3",
            'jumlah_realisasi_kinerja' : "",
            'satuan_realisasi_kinerja' : "Tugas",
            'bobot_realisasi_kinerja' : ""
        }

context_dict_2_updated = {
            'kategori' : RISET_DAN_PUSILKOM,
            'pekerjaan' : MEMBUAT_SOAL,
            'detail_kegiatan' : ESSAY_DAN_PILGAN,
            'pemberi_tugas' : IBU_IKA_ALFINA,
            'uraian' : MEMBUAT_SOAL_PR,
            'matkul' : BASIS_DATA,
            'periode' : SEMESTER_KULIAH,
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "4",
            'satuan_kinerja' : "Tugas",
            'bobot_kinerja' : "4",
            'jumlah_realisasi_kinerja' : "4",
            'satuan_realisasi_kinerja' : "Tugas",
            'bobot_realisasi_kinerja' : "4"
        }

context_wrong = {
            'kategori' : PENYELENGGARAN_KULIAH,
            'pekerjaan' : MEMBUAT_SOAL,
            'detail_kegiatan' : ESSAY_DAN_PILGAN,
            'pemberi_tugas' : IBU_IKA_ALFINA,
            'uraian' : MEMBUAT_SOAL_PR,
            'matkul' : BASIS_DATA,
            'periode' : SEMESTER_KULIAH,
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "Empat",
            'satuan_kinerja' : "Tugas",
            'jam_rencana_kinerja' : "Empat",
            'jumlah_realisasi_kinerja' : "Empat",
            'satuan_realisasi_kinerja' : "Tugas",
            'bobot_realisasi_kinerja' : "Empat"
        }

context_wrong_updated = {
            'kategori' : RISET_DAN_PUSILKOM,
            'pekerjaan' : MEMBUAT_SOAL,
            'detail_kegiatan' : ESSAY_DAN_PILGAN,
            'pemberi_tugas' : IBU_IKA_ALFINA,
            'uraian' : MEMBUAT_SOAL_PR,
            'matkul' : BASIS_DATA,
            'periode' : SEMESTER_KULIAH,
            'bulan_pengerjaan' : "MAR",
            'jumlah_kinerja' : "Empat",
            'satuan_kinerja' : "Tugas",
            'jam_rencana_kinerja' : "Empat",
            'jumlah_realisasi_kinerja' : "Empat",
            'satuan_realisasi_kinerja' : "Tugas",
            'bobot_realisasi_kinerja' : "Empat"
        }
        
class PengisianLogTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()
        self.profile = TeachingAssistantProfile(user=self.ta_user,nama="richie",kontrak="Full Time",status="Lulus S1",prodi="Ilmu Komputer")
        self.profile.save()
        self.ta_user_2 = User.objects.create(username='ta2', password='ta2', email='ta2@ta2.com')
        self.ta_user_2.role.role = 'TA'
        self.ta_user_2.role.save()

        self.admin_user = User.objects.create(username='admin', password='admin', email='admin@admin.com')
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        self.na_user = User.objects.create(username='na', password='na', email='na@na.com')
        self.na_user.role.role = 'not-assign'
        self.na_user.role.save()

        self.matkul_1 = MataKuliah.objects.create(nama='Basis Data')
        self.matkul_2 = MataKuliah.objects.create(nama='Aljabar Linier')

        self.profile_user_1 = TeachingAssistantProfile.objects.create(
            user = self.ta_user,
            nama = 'TA USER 1',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Ilmu Komputer',
            bulan_mulai = 'JAN',
            bulan_selesai = 'MAR'
        )

        self.profile_user_1.daftar_matkul.add(self.matkul_1)
        self.profile_user_1.save()

        self.profile_user_2 = TeachingAssistantProfile.objects.create(
            user = self.ta_user_2,
            nama = 'TA USER 2',
            kontrak = 'Full Time',
            status = 'Lulus S2',
            prodi = 'Sistem Informasi',
            bulan_mulai = 'JAN',
            bulan_selesai = 'MAR'
        )

        self.profile_user_2.daftar_matkul.add(self.matkul_2)
        self.profile_user_2.save()

        self.logTA_1 = LogTA.objects.create(
            user = self.ta_user,
            kategori = PENYELENGGARAN_KULIAH,
            jenis_pekerjaan = MEMBUAT_SOAL,
            detail_kegiatan = ESSAY_DAN_PILGAN,
            pemberi_tugas = IBU_IKA_ALFINA,
            uraian = MEMBUAT_SOAL_PR,
            matkul = self.matkul_1,
            periode = SEMESTER_KULIAH,
            bulan_pengerjaan = "Semester Kuliah",
            jumlah_rencana_kinerja = 12,
            satuan_rencana_kinerja = "Tugas",
            bobot_jam_rencana_kinerja = 1,
            jam_kerja_rencana = 0.375
        )

        self.logTA_2 = LogTA.objects.create(
            user = self.ta_user,
            kategori = PERSIAPAN_KULIAH,
            jenis_pekerjaan = "Mempersiapkan Environment",
            detail_kegiatan = "SCELE",
            pemberi_tugas = "Ibu Putu",
            uraian = "Rapat persiapan",
            matkul = self.matkul_2,
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            bobot_jam_rencana_kinerja = 2,
            jam_kerja_rencana = 2.0
        )

        self.periode = Periode(
            tahun_ajaran = TAHUN_AJARAN,
            semester = SEMESTER_TAHUN_AJARAN,
        )
        self.periode.save()

        self.periode_sekarang = PeriodeSekarang(periode = self.periode)
        self.periode_sekarang.save()

    # Test membuat log TA
    def test_create_LogTA(self):
        all_log_ta = LogTA.objects.all()
        
        self.assertEquals(all_log_ta.count(), 2)
        self.assertEquals(all_log_ta[0].kategori, PENYELENGGARAN_KULIAH)
        self.assertEquals(all_log_ta[1].kategori, PERSIAPAN_KULIAH)

    def test_create_LogTA_with_realisasi(self):
        self.logTA_1.jumlah_realisasi_kinerja = 8
        self.logTA_1.satuan_realisasi_kinerja = "Tugas"
        self.logTA_1.bobot_jam_realisasi_kinerja = 2
        self.logTA_1.jam_kerja_realisasi = 0.5
        self.logTA_1.save()

        self.logTA_2.jumlah_realisasi_kinerja = 2
        self.logTA_2.satuan_realisasi_kinerja = "Tugas"
        self.logTA_2.bobot_jam_realisasi_kinerja = 2
        self.logTA_2.jam_kerja_realisasi = 1.0
        self.logTA_2.save()

        all_log_ta = LogTA.objects.all()
        
        self.assertEquals(all_log_ta.count(), 2)
        self.assertEquals(all_log_ta[0].kategori, PENYELENGGARAN_KULIAH)
        self.assertEquals(all_log_ta[1].kategori, PERSIAPAN_KULIAH)

    def test_display_form_LogTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_MENGISI_LOG))

        self.assertTemplateUsed(response, 'form_log.html')
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_display_form_LogTA_unregistered(self):
        response = self.client.get(reverse(URL_MENGISI_LOG))

        self.assertEqual(response.status_code, 302)

    def test_post_form_logTA_as_TA_without_realisasi(self):
        self.client.force_login(user=self.ta_user)
        context_dict_1['matkul'] = self.matkul_1
        response = self.client.post(reverse(URL_MENGISI_LOG), context_dict_1)

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 3)
        self.assertEquals(all_log_ta[0].kategori, PENYELENGGARAN_KULIAH)
        # self.assertEquals(all_log_ta[2].bobot_jam_rencana_kinerja, all_log_ta[2].jumlah_rencana_kinerja / 4)
        # self.assertEquals(all_log_ta[2].bobot_jam_realisasi_kinerja, all_log_ta[2].jumlah_realisasi_kinerja / 4)
        self.assertRedirects(response, reverse(URL_DAFTAR_LOG_TA))

    def test_post_form_logTA_as_TA_with_realisasi_semester_kuliah(self):
        self.client.force_login(user=self.ta_user)
        context_dict_2['matkul'] = self.matkul_2
        response = self.client.post(reverse(URL_MENGISI_LOG), context_dict_2)

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 3)
        self.assertEquals(all_log_ta[0].kategori, PENYELENGGARAN_KULIAH)
        new_var = URL_DAFTAR_LOG_TA
        self.assertRedirects(response, reverse(new_var))
    
    def test_post_form_logTA_as_TA_with_realisasi_sepanjang_kontrak(self):
        self.client.force_login(user=self.ta_user)
        context_dict_3['matkul'] = self.matkul_2
        response = self.client.post(reverse(URL_MENGISI_LOG), context_dict_3)

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 3)
        self.assertEquals(all_log_ta[0].kategori, PENYELENGGARAN_KULIAH)
        new_var = URL_DAFTAR_LOG_TA
        self.assertRedirects(response, reverse(new_var))

    def test_post_form_logTA_as_TA_wrong_input(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.post(reverse(URL_MENGISI_LOG), context_wrong)

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertTemplateUsed(response, 'form_log.html')

    def test_post_form_logTA_as_unregistered(self):
        context_dict_1['matkul'] = self.matkul_1
        response = self.client.post(reverse(URL_MENGISI_LOG), context_dict_1)

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertEqual(response.status_code, 302)
    
    # Test melihat log TA
    def test_view_LogTA_response_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_DAFTAR_LOG_TA))

        user = auth.get_user(self.client)
        logs = response.context['logs']

        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftar_log.html')
        self.assertEqual(len(logs), 1)
    
    def test_view_LogTA_response_as_evaluator(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(URL_DAFTAR_LOG_EVALUATOR,kwargs={'username':'ta'}))
        user = auth.get_user(self.client)
        logs = response.context['logs']

        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftar_log.html')
        self.assertEqual(len(logs), 1)
    

    def test_view_history_log_as_registered(self):
        self.client.force_login(user=self.admin_user)

        old_category = self.logTA_1.kategori
        new_category = DUKUNGAN_KULIAH_KAKAK_ASUH
        self.logTA_1.kategori = new_category
        self.logTA_1.save()

        response = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':self.logTA_1.id}))
        histories_response = response.context['history']

        self.assertEqual(histories_response.count(), 2)
        self.assertEqual(histories_response[0].kategori, new_category)
        self.assertEqual(histories_response[1].kategori, old_category)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history_log.html')

    def test_view_history_log_history_user(self):
        self.client.force_login(user=self.ta_user)
        self.logTA_1.kategori = DUKUNGAN_KULIAH_KAKAK_ASUH
        self.logTA_1._history_user = self.ta_user
        self.logTA_1.save()

        self.client.login(user=self.admin_user)
        self.logTA_1.kategori = RISET_DAN_PUSILKOM
        self.logTA_1._history_user = self.admin_user
        self.logTA_1.save()

        response = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':self.logTA_1.id}))
        histories_response = response.context['history']

        self.assertEqual(histories_response[1].history_user, self.ta_user)
        self.assertEqual(histories_response[0].history_user, self.admin_user)

    def test_view_history_log_as_unregistered(self):
        
        response = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 
                         reverse('authentication:login')+'?next='+reverse(URL_HISTORY_LOG, 
                                                                          kwargs={'id':self.logTA_1.id}))
        
    def test_view_history_missing_log(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':8000}))
        self.assertEqual(response.status_code, 404)
        
    def test_view_history_log_only_correspoinding_ta_or_admin(self):
        self.client.force_login(user=self.ta_user)
        self.logTA_1.save()

        response_ta_user = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response_ta_user.status_code, 200)

        self.client.force_login(user=self.ta_user_2)
        response_ta_user_2 = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response_ta_user_2.status_code, 403)

        self.client.force_login(user=self.admin_user)
        response_admin = self.client.get(reverse(URL_HISTORY_LOG, kwargs={'id':self.logTA_1.id}))
        self.assertEqual(response_admin.status_code, 200)

    def test_filter_LogTA_response_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_DAFTAR_LOG_TA))
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_filter_LogTA_response_as_evaluator(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(URL_DAFTAR_LOG_EVALUATOR,kwargs={'username':'ta'}))
        self.assertEquals(response.context['kategori_choice'], LogTA.kategori.field.choices)
        self.assertEquals(response.context['periode_choice'], LogTA.periode.field.choices)
        self.assertEquals(response.context['bulan_choice'], LogTA.bulan_pengerjaan.field.choices)

    def test_filter_LogTA_response_TA_context(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_DAFTAR_LOG_TA),{"bulan":"JAN","kategori":"Adhoc","periode":"Persiapan Kuliah"})
        self.assertEquals(response.context['filter_kategori'][0], "Adhoc")
        self.assertEquals(response.context['filter_periode'][0], "Persiapan Kuliah")
        self.assertEquals(response.context['filter_bulan'][0], "JAN")

    def test_filter_LogTA_response_Admin_context(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse(URL_DAFTAR_LOG_EVALUATOR,kwargs={'username':'ta'}),{"bulan":"JAN","kategori":"Harian","periode":PERSIAPAN_KULIAH})
        self.assertEquals(response.context['filter_kategori'][0], "Harian")
        self.assertEquals(response.context['filter_periode'][0], PERSIAPAN_KULIAH)
        self.assertEquals(response.context['filter_bulan'][0], "JAN")
        
    # Test edit log TA
    def test_display_form_edit_log_ta_as_ta(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))
        log = response.context["log"]

        self.assertTemplateUsed(response, 'edit_log.html')
        self.assertEquals(response.context['kategori_choice'], [kategori for kategori in LogTA.kategori.field.choices if log.kategori not in kategori])
        self.assertEquals(response.context['periode_choice'], [periode for periode in LogTA.periode.field.choices if log.periode not in periode])
        self.assertEquals(response.context['bulan_choice'], [bulan_pengerjaan for bulan_pengerjaan in LogTA.bulan_pengerjaan.field.choices if log.bulan_pengerjaan not in bulan_pengerjaan])

    def test_display_form_edit_log_ta_unregistered(self):

        response = self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        self.assertEqual(response.status_code, 302)

    def test_post_form_edit_log_ta_without_realisasi_as_TA(self):
        self.client.force_login(user=self.ta_user)
        self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        response = self.client.post(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}), context_dict_1_updated)
        response_updated = self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        updated_log = response_updated.context["log"]
        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertEquals(updated_log.kategori, PENYELENGGARAN_KULIAH)
        self.assertEquals(updated_log.jumlah_rencana_kinerja, 3)
        self.assertRedirects(response, reverse(URL_DAFTAR_LOG_TA))

    def test_post_form_edit_log_ta_with_realisasi_as_TA(self):
        self.client.force_login(user=self.ta_user)
        self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        response = self.client.post(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}), context_dict_2_updated)
        response_updated = self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        updated_log = response_updated.context["log"]
        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertEquals(updated_log.kategori, RISET_DAN_PUSILKOM)
        self.assertRedirects(response, reverse(URL_DAFTAR_LOG_TA))
    
    def test_post_form_edit_log_ta_with_realisasi_as_admin(self):
        self.client.force_login(user=self.admin_user)
        self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        response = self.client.post(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}), context_dict_2_updated)
        response_updated = self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        updated_log = response_updated.context["log"]
        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertEquals(updated_log.kategori, RISET_DAN_PUSILKOM)
        self.assertRedirects(response, reverse(URL_DASHBOARD_ADMIN))

    def test_post_form_edit_log_ta_as_ta_wrong_input(self):
        self.client.force_login(user=self.ta_user)
        self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        self.client.post(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}), context_wrong_updated)
        response = self.client.get(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertTemplateUsed(response, 'edit_log.html')

    def test_post_form_edit_log_ta_as_unregistered(self):
        response = self.client.post(reverse(URL_EDIT_LOG_TA, kwargs={'id':1}))

        all_log_ta = LogTA.objects.all()

        self.assertEquals(all_log_ta.count(), 2)
        self.assertEqual(response.status_code, 302)
    
    def test_delete_log_ta(self):
        self.client.force_login(user=self.ta_user)
        self.client.post(reverse("pengisianLog:delete_log", kwargs={'id':1}))

        all_log_ta = LogTA.objects.all()
        self.assertEquals(all_log_ta.count(), 1)
    
    def test_detail_log_ta_authorized(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("pengisianLog:detail_log", kwargs={'id':1}))

        self.assertTemplateUsed(response, 'detail_log.html')
    
    def test_delete_log_as_admin(self):
        self.client.force_login(user=self.admin_user)
        self.client.post(reverse("pengisianLog:delete_log", kwargs={'id':1}))

        all_log_ta = LogTA.objects.all()
        self.assertEquals(all_log_ta.count(), 1)

    def test_detail_log_ta_unauthorized(self):
        self.client.force_login(user=self.ta_user_2)
        response = self.client.get(reverse("pengisianLog:detail_log", kwargs={'id':1}))
        
        self.assertEqual(response.status_code, 403)

