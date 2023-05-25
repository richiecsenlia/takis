from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import User
from .views import *
from pengisianLog.models import LogTA
from periode.models import Periode, PeriodeSekarang
from django.urls import reverse
from accounts.models import MataKuliah
from periode.models import Periode, PeriodeSekarang

TAHUN_AJARAN = "2023/2024"
SEMESTER_TAHUN_AJARAN = "Genap"

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
            user = self.ta_user_other,
            nama = 'TA USER 2',
            kontrak = 'Full Time',
            status = 'Lulus S2',
            prodi = 'Sistem Informasi',
            bulan_mulai = 'JAN',
            bulan_selesai = 'MAR'
        )

        self.profile_user_2.daftar_matkul.add(self.matkul_2)
        self.profile_user_2.save()

        self.periode = Periode(
            tahun_ajaran = TAHUN_AJARAN,
            semester = SEMESTER_TAHUN_AJARAN,
            bulan_mulai = "JAN",
            bulan_selesai = "JUL"
        )
        self.periode.save()

        self.periode_sekarang = PeriodeSekarang(periode = self.periode)
        self.periode_sekarang.save()

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            matkul = self.matkul_1,
            periode = "Adhoc",
            bulan_pengerjaan = "FEB",
            jumlah_rencana_kinerja = 12,
            satuan_rencana_kinerja = "Tugas",
            bobot_jam_rencana_kinerja = 1,
            jam_kerja_rencana = 3.0,
            jumlah_realisasi_kinerja = 12,
            satuan_realisasi_kinerja = "Tugas",
            bobot_jam_realisasi_kinerja = 1,
            jam_kerja_realisasi = 3.0,
            periode_log = self.periode_sekarang.periode
        )

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Persiapan Kuliah",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            matkul = self.matkul_1,
            periode = "Semester Kuliah",
            bulan_pengerjaan = "Semester Kuliah",
            jumlah_rencana_kinerja = 7,
            satuan_rencana_kinerja = "Tugas",
            bobot_jam_rencana_kinerja = 7,
            jam_kerja_rencana = 0.25,
            jumlah_realisasi_kinerja = 7,
            satuan_realisasi_kinerja = "Tugas",
            bobot_jam_realisasi_kinerja = 1,
            jam_kerja_realisasi = 0.25,
            periode_log = self.periode_sekarang.periode
        )

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Pengembangan Institusi",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            matkul = self.matkul_1,
            periode = "Sepanjang Kontrak",
            bulan_pengerjaan = "Sepanjang Kontrak",
            jumlah_rencana_kinerja = 9,
            satuan_rencana_kinerja = "Tugas",
            bobot_jam_rencana_kinerja = 3,
            jam_kerja_rencana = 2.25,
            jumlah_realisasi_kinerja = 9,
            satuan_realisasi_kinerja = "Tugas",
            bobot_jam_realisasi_kinerja = 3,
            jam_kerja_realisasi = 2.25,
            periode_log = self.periode_sekarang.periode
        )

    def test_get_average_all_rencana(self):
        rekapan_total = get_all_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode)

        self.assertEquals(rekapan_total['total_plan'],3.5)
        self.assertEquals(rekapan_total['persiapan_plan'], 0.25)
        self.assertEquals(rekapan_total['persiapan_real'], 0.25)
        self.assertEquals(rekapan_total['penyelenggaraan_plan'], 1.0)
        self.assertEquals(rekapan_total['penyelenggaraan_real'], 1.0)
        self.assertEquals(rekapan_total['pengembangan_plan'], 2.25)
        self.assertEquals(rekapan_total['pengembangan_real'], 2.25)

    def test_get_average_month_rencana(self):
        rencana_jan = get_month_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode, 'JAN')
        rencana_feb = get_month_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode, 'FEB')

        self.assertEquals(rencana_jan['total_plan'], 2.5)
        self.assertEquals(rencana_jan['persiapan_plan'], 0.25)
        self.assertEquals(rencana_jan['pengembangan_plan'], 2.25)
        self.assertEquals(rencana_feb['total_plan'], 5.5)
        self.assertEquals(rencana_feb['persiapan_plan'], 0.25)
        self.assertEquals(rencana_feb['penyelenggaraan_plan'], 3.0)
        self.assertEquals(rencana_feb['pengembangan_plan'], 2.25)

    def test_display_rekap_LogTA_as_TA(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.get(reverse("rekapanLog:rekapan_log", args=[self.ta_user.username]))

        rencanaAvg = get_all_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode)

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

        rencanaAvg = get_all_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode)

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

        rencanaApr = get_month_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode, 'APR')

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
    
    def test_display_rekap_LogTA_with_choice_rata_rata(self):
        self.client.force_login(user=self.ta_user)
        response = self.client.post(reverse("rekapanLog:rekapan_log", args=[self.ta_user.username]), {"bulan" : "Rata-rata"})

        rencanaAvg = get_all_rencana(self.ta_user, self.profile_user_1, self.periode_sekarang.periode)

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