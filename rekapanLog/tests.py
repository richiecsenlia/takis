from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import User
from .views import *
from pengisianLog.models import LogTA
from django.urls import reverse

# Create your tests here.
class RekapanLogTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()

        self.ta_user_other = User.objects.create(username='ta2', password='ta', email='ta2@ta.com')
        self.ta_user_other.role.role = 'TA'
        self.ta_user_other.role.save()

        self.admin_user = User.objects.create(username='admin', password='admin', email='admin@admin.com')
        self.admin_user.role.role = 'admin'
        self.admin_user.role.save()

        LogTA.objects.create(
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
            jumlah_realisasi_kinerja = 4,
            satuan_realisasi_kinerja = "Tugas",
            konversi_jam_realisasi_kinerja = 1
        )

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Koreksi Tugas",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Mengoreksi PR",
            periode = "Semester Kuliah",
            bulan_pengerjaan = "APR",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 0.5,
            jumlah_realisasi_kinerja = 1,
            satuan_realisasi_kinerja = "Tugas",
            konversi_jam_realisasi_kinerja = 0.25
        )

        LogTA.objects.create(
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

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Pengembangan Institusi",
            jenis_pekerjaan = "Manajemen Lembaga Asisten",
            detail_kegiatan = "",
            pemberi_tugas = "",
            uraian = "Meeting Lembaga asisten",
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            jumlah_rencana_kinerja = 1,
            satuan_rencana_kinerja = "semester",
            konversi_jam_rencana_kinerja = 1,
            jumlah_realisasi_kinerja = 1,
            satuan_realisasi_kinerja = "semester",
            konversi_jam_realisasi_kinerja = 1
        )

        LogTA.objects.create(
            user = self.ta_user_other,
            kategori = "Persiapan Kuliah",
            jenis_pekerjaan = "Mempersiapkan Environment",
            detail_kegiatan = "",
            pemberi_tugas = "",
            uraian = "Rapat persiapan",
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 2,
            jumlah_realisasi_kinerja = 2,
            satuan_realisasi_kinerja = "",
            konversi_jam_realisasi_kinerja = 2
        )

    def test_get_average_all_rencana(self):
        rencanaAvg = get_all_rencana(self.ta_user)
        # penyelenggaraan harusnya 0.25, persiapan harusnya 0.33 (rata2)

        self.assertEquals(rencanaAvg['penyelenggaraan_plan'], 0.25)
        self.assertEquals(rencanaAvg['penyelenggaraan_real'], (1.25/6))
        self.assertEquals(rencanaAvg['persiapan_plan'], (1/3))
        self.assertEquals(rencanaAvg['persiapan_real'], 0)
        self.assertEquals(rencanaAvg['pengembangan_plan'], (1/6))
        self.assertEquals(rencanaAvg['pengembangan_real'], (1/6))

    def test_get_average_month_rencana(self):
        rencanaApr = get_month_rencana(self.ta_user, 'APR')
        rencanaSep = get_month_rencana(self.ta_user, 'SEP')
        # penyelenggaraan harusnya 0.25, persiapan harusnya 0.33 (rata2)

        self.assertEquals(rencanaApr['penyelenggaraan_plan'], 0.5)
        self.assertEquals(rencanaApr['penyelenggaraan_real'], 0.25)
        self.assertEquals(rencanaSep['persiapan_plan'], 2)
        self.assertEquals(rencanaSep['persiapan_real'], 0)
        self.assertEquals(rencanaSep['pengembangan_plan'], 1)
        self.assertEquals(rencanaSep['pengembangan_real'], 1)

    def test_display_rekap_LogTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("rekapanLog:rekapan_log", args=[self.ta_user.username]))

        rencanaAvg = get_all_rencana(self.ta_user)

        self.assertTemplateUsed(response, 'rekap_log.html')
        self.assertEquals(response.context['persiapan_plan'], rencanaAvg['persiapan_plan'])
        self.assertEquals(response.context['persiapan_real'], rencanaAvg['persiapan_real'])
        self.assertEquals(response.context['penyelenggaraan_plan'], rencanaAvg['penyelenggaraan_plan'])
        self.assertEquals(response.context['penyelenggaraan_plan'], rencanaAvg['penyelenggaraan_plan'])
        self.assertEquals(response.context['dukungan_plan'], rencanaAvg['dukungan_plan'])
        self.assertEquals(response.context['dukungan_real'], rencanaAvg['dukungan_real'])
        self.assertEquals(response.context['pengembangan_plan'], rencanaAvg['pengembangan_plan'])
        self.assertEquals(response.context['pengembangan_real'], rencanaAvg['pengembangan_real'])
        self.assertEquals(response.context['riset_plan'], rencanaAvg['riset_plan'])
        self.assertEquals(response.context['riset_real'], rencanaAvg['riset_real'])

        self.assertEquals(response.context['choice'], "Rata-rata")

    def test_display_rekap_LogTA_as_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse("rekapanLog:rekapan_log", args=[self.ta_user.username]))

        rencanaAvg = get_all_rencana(self.ta_user)

        self.assertTemplateUsed(response, 'rekap_log.html')
        self.assertEquals(response.context['persiapan_plan'], rencanaAvg['persiapan_plan'])
        self.assertEquals(response.context['persiapan_real'], rencanaAvg['persiapan_real'])
        self.assertEquals(response.context['penyelenggaraan_plan'], rencanaAvg['penyelenggaraan_plan'])
        self.assertEquals(response.context['penyelenggaraan_plan'], rencanaAvg['penyelenggaraan_plan'])
        self.assertEquals(response.context['dukungan_plan'], rencanaAvg['dukungan_plan'])
        self.assertEquals(response.context['dukungan_real'], rencanaAvg['dukungan_real'])
        self.assertEquals(response.context['pengembangan_plan'], rencanaAvg['pengembangan_plan'])
        self.assertEquals(response.context['pengembangan_real'], rencanaAvg['pengembangan_real'])
        self.assertEquals(response.context['riset_plan'], rencanaAvg['riset_plan'])
        self.assertEquals(response.context['riset_real'], rencanaAvg['riset_real'])

        self.assertEquals(response.context['choice'], "Rata-rata")
        
    def test_display_rekap_LogTA_with_choice(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.post(reverse("rekapanLog:rekapan_log", args=[self.ta_user.username]), {"bulan" : "APR"})

        rencanaApr = get_month_rencana(self.ta_user, 'APR')

        self.assertTemplateUsed(response, 'rekap_log.html')
        self.assertEquals(response.context['persiapan_plan'], rencanaApr['persiapan_plan'])
        self.assertEquals(response.context['persiapan_real'], rencanaApr['persiapan_real'])
        self.assertEquals(response.context['penyelenggaraan_plan'], rencanaApr['penyelenggaraan_plan'])
        self.assertEquals(response.context['penyelenggaraan_plan'], rencanaApr['penyelenggaraan_plan'])
        self.assertEquals(response.context['dukungan_plan'], rencanaApr['dukungan_plan'])
        self.assertEquals(response.context['dukungan_real'], rencanaApr['dukungan_real'])
        self.assertEquals(response.context['pengembangan_plan'], rencanaApr['pengembangan_plan'])
        self.assertEquals(response.context['pengembangan_real'], rencanaApr['pengembangan_real'])
        self.assertEquals(response.context['riset_plan'], rencanaApr['riset_plan'])
        self.assertEquals(response.context['riset_real'], rencanaApr['riset_real'])

        self.assertEquals(response.context['choice'], "APR")