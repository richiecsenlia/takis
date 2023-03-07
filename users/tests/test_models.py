from django.test import TestCase
from users.models import UserProfile

class TestUsersModels(TestCase):

    """Test user add profile with valid input"""
    def test_add_user_profile(self):
        user_profile1 = UserProfile.objects.create(
          nama_lengkap = "Ilma Ainur Rohma",
          jenis_kontrak = "Part Time",
          status_kemahasiswaan = "Lulus S1",
          program_studi = "Ilmu Komputer",
        )

        user_profile2 = UserProfile.objects.create(
          nama_lengkap = "Immanuel Nadeak",
          jenis_kontrak = "Part Time",
          status_kemahasiswaan = "Lulus S1",
          program_studi = "Ilmu Komputer",
        )

        users_profile = UserProfile.objects.all()

        self.assertEquals(users_profile.count(), 2)