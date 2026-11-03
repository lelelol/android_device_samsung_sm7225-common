# extract-utils hook: run the lineage-22.2 binary patch on the extracted audio.primary.lito.so
import os, subprocess, sys

def blob_fixup(ctx, file, file_path, *args, **kwargs):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch_audio_primary_lito.py')
    subprocess.run([sys.executable, script, file_path], check=True)
