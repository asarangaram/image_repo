import subprocess
import os
import json

class ExifTool(object):

    sentinel = b"{ready}\n"

    def __init__(self, executable="/usr/local/bin/exiftool"):
        self.executable = executable

    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, "-stay_open", "True",  "-@", "-"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return self

    def  __exit__(self, exc_type, exc_value, traceback):
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
        return json.loads( self.execute( "-g", "-j", "-n",  *filenames).decode('utf8').replace("'", '"'))

with ExifTool() as exiftool:
    print(json.dumps(exiftool.get_metadata("/home/anandas/work/projects/image_repo/IMG_3243.JPG"), indent=2))