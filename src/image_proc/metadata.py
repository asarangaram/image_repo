import subprocess
import os
import json


class ExifTool(object):

    sentinel = b"{ready}\n"

    def __init__(self, executable="/usr/local/bin/exiftool"):
        self.executable = executable

    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, "-stay_open", "True", "-@", "-"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.process.stdin.write("-stay_open\nFalse\n".encode())
        self.process.stdin.flush()

    def execute(self, *args):
        args = args + ("-execute\n",)
        self.process.stdin.write(str.join("\n", args).encode())
        self.process.stdin.flush()
        output = bytearray()
        fd = self.process.stdout.fileno()
        while output[-len(self.sentinel):] != self.sentinel:
            output += os.read(fd, 4096)

            """

            print(output)

            if not output.endswith(self.sentinel):
                print("output not end with sentinel")
                print(output[-len(self.sentinel)-1:])
            return output[:-len(self.sentinel)]
            """
        return output[:-len(self.sentinel)]

    def get_metadata(self, *filenames):
        _metadata_list = json.loads(
            self.execute(
                "-g",
                "-j",
                "-n",
                "-b",
                *
                filenames).decode('utf8').replace(
                "'",
                '"'))
        for i, _metadata in enumerate(_metadata_list):
            _metadata.pop('SourceFile', None)
            # _metadata.pop('File', None)
            _metadata.pop('ExifTool', None)
            if "File" in _metadata:
                _metadata["File"].pop("Directory", None)
                _metadata["File"].pop("FilePermissions", None)
                _metadata["File"].pop("FileTypeExtension", None)

                _metadata["File"].pop("FileAccessDate", None)
                _metadata["File"].pop("FileModifyDate", None)
                _metadata["File"].pop("FilePermissions", None)
                _metadata["File"].pop("FileTypeExtension", None)

            if "EXIF" in _metadata:
                _metadata["EXIF"].pop("Padding", None)
                _metadata["EXIF"].pop("ThumbnailOffset", None)
                # We don't preserve thumbnail from EXIF
                _metadata["EXIF"].pop("ThumbnailImage", None)
                _metadata["EXIF"].pop("ThumbnailLength", None)

        return _metadata_list


if __name__ == '__main__':
    with ExifTool() as exiftool:
        print(
            json.dumps(
                exiftool.get_metadata("/home/anandas/work/projects/image_repo/IMG_3243.JPG"),
                indent=2))
"""
# Load the original image
original_image = Image.open("original_image.jpg")  # Replace with your image file path

# Resize the image to create a thumbnail
thumbnail_size = (100, 100)  # Change the size as per your requirements
thumbnail_image = original_image.copy()  # Create a copy of the original image
thumbnail_image.thumbnail(thumbnail_size)

# Convert the thumbnail image to a base64 encoded string
thumbnail_image_bytes = thumbnail_image.convert("RGB").tobytes()
base64_encoded_thumbnail = base64.b64encode(thumbnail_image_bytes).decode("utf-8")

print(base64_encoded_thumbnail)
 """
