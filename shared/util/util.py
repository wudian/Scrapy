import subprocess

def get_system_uuid():
    out, err = subprocess.Popen('dmidecode -s system-uuid'.split(), stdout=subprocess.PIPE).communicate()
    # out: '31AEB01B-7AE5-4481-AC5B-DCE9D7B6A5F5\n'
    return out[0:len(out)-1]
    # return 'AA9234B7-C004-457B-8CD3-E718DFC699E5'