import subprocess
import os
import uuid

OUTPUT_DIR = "/tmp/lo"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_to_pdf(input_file):

    outname = str(uuid.uuid4()) + ".pdf"
    output = os.path.join(OUTPUT_DIR, outname)

    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        input_file,
        "--outdir",
        OUTPUT_DIR
    ]

    subprocess.run(cmd, check=True)

    return output