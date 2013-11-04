from ..utils import TestCase
from capacity import GB

class FilesystemTest(TestCase):

    def setUp(self):
        super(FilesystemTest, self).setUp()
        self.fs_name = "fs1"
        self.fs = self.system.objects.filesystems.create(name=self.fs_name, quota=GB)

    def test_filesystem_get_set_quota(self):
        self.assertEquals(self.fs.get_quota(), GB)
        self.fs.update_quota(3*GB)

    def test_create_filesystem_with_quota_direct(self):
        fs = self.system.objects.filesystems.create(name="bla", quota_in_bytes=1000000000)
        self.assertEquals(fs.get_quota(), GB)

    def test_filesystem_get_set_name(self):
        self.assertEquals(self.fs.get_name(), self.fs_name)
        self.fs.update_name("new_name")

