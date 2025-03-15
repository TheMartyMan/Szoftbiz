import unittest, os, stat, tempfile, shutil, glob
from matrix import getPerms, setRO, setRW, updateACLAddRead, getResources


class TestFilePermissions(unittest.TestCase):
    def setUp(self):
        # Isolate testcase in temp folder
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        with open("ACL.txt", "w") as f:
            f.write("alice;r;rw\n")
            f.write("bob;rw\n")
        
        # Dummy resource files
        self.file1 = os.path.join(self.test_dir, "File1.txt")
        self.file2 = os.path.join(self.test_dir, "File2.txt")
        with open(self.file1, "w") as f:
            f.write("dummy")
        with open(self.file2, "w") as f:
            f.write("dummy")
        
        # New file for ro/rw testing
        self.new_file = os.path.join(self.test_dir, "new_file.txt")
        with open(self.new_file, "w") as f:
            f.write("dummy")
        
        # A getResources() modification for testcase
        global getResources
        def patched_getResources():
            return glob.glob(os.path.join(os.getcwd(), "File*.txt"))
        getResources = patched_getResources

    def tearDown(self):
        os.chdir(self.old_cwd)
        for root, dirs, files in os.walk(self.test_dir):
            for fname in files:
                full_path = os.path.join(root, fname)
                os.chmod(full_path, stat.S_IWRITE)
        shutil.rmtree(self.test_dir)


    # Check if the permissions are correct for an existing user
    def test_getPerms_valid_user(self):
        
        perms = getPerms("alice")
        self.assertEqual(perms, ["r", "rw"])


    # Check if the program exits on a literally nonextintent user
    def test_getPerms_invalid_user(self):
        
        with self.assertRaises(SystemExit):
            getPerms("nonexistent")


    # Check RO permission
    def test_setRO(self):
        setRO(self.new_file)
        mode = os.stat(self.new_file).st_mode
        self.assertFalse(mode & stat.S_IWUSR, "The file must not have write permissions for the owner.")

    # Check RW permission
    def test_setRW(self):
        setRW(self.new_file)
        mode = os.stat(self.new_file).st_mode
        self.assertTrue(mode & stat.S_IWUSR, "The file must have write permissions for the owner.")


    # Check ACL update
    def test_updateACLAddRead(self):
        updateACLAddRead()
        with open("ACL.txt", "r") as f:
            lines = f.read().splitlines()
        self.assertIn("alice;r;rw;r", lines)
        self.assertIn("bob;rw;r", lines)

    def test_getResources(self):
        resources = getResources()
        expected = {self.file1, self.file2}
        self.assertEqual(set(resources), expected)

if __name__ == '__main__':
    unittest.main()
