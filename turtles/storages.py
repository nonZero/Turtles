import os
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string


class RandomFilenameStorage(FileSystemStorage):
    def get_available_name(self, name):
        """
        Returns a semi random filename that's free on the target storage
        system, and available for new content to be written to.
        """
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        while True:
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s%s" % (
            get_random_string(), file_ext))
            if not self.exists(name):
                break

        return name
