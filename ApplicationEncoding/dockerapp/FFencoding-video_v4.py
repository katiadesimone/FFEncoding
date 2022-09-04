from os import path, listdir, makedirs
from subprocess import call
import shutil
from prometheus_client import push_to_gateway, CollectorRegistry, Gauge
import subprocess
import os
import socket
import time
# -------------------------------------------------------------------------------
# CONFIGURABLE SETTINGS
# -------------------------------------------------------------------------------
# parametri variabili streaming
BITRATE = ['1M', '2M','3M','4M','6M']
QUALITY = ['15', '14', '13', '12']
RESOLUTION = ['640:480','1280:720','1920:1080','2048:1080']
# output video dimensions
EXTENSION = '.mp4'
# encoding speed:compression ratio
PRESET = ['ultrafast', 'superfast', 'veryfast', 'medium', 'slow']
# output file format
#RELATIVE_OUTPUT_DIRECTORY = '/home/katia/progetto/application_node/encoded/'
RELATIVE_OUTPUT_DIRECTORY = (os.getcwd()+'/encoded/')
# ffmpeg path
FFMPEG_PATH = subprocess.check_output("which ffmpeg", shell=True).strip()
# FFPROBE_PATH = '/usr/bin/ffprobe'
FFPROBE_PATH = subprocess.check_output("which ffprobe", shell=True).strip()
# input file name
INPUT_file_name = 'Jellyfish_1080_10s_1MB'
# input file extension
INPUT_file_extension = '.webm'
# creare il registro per una nuova metrica
registry = CollectorRegistry()
# creare la metrica ed aggiungerla al nuovo registro
bitrate_gauge = Gauge("bitrate", "python_push_to_gateway", registry=registry)
# trovare l'IP address di localhost
localIp = socket.gethostbyname(socket.gethostname())
#localIp = socket.gethostbyname(socket.gethostname())
print(localIp)

# -------------------------------------------------------------------------------
# FUNCTIONS
# -------------------------------------------------------------------------------


# example : ffmpeg -i i.mp4 -f mp4 -s 1920x1080 -b 6000k -r 30 -vcodec libx264 -preset veryslow -threads auto o.mp4
def encode_file(bv,crf ):
    clean_directory(RELATIVE_OUTPUT_DIRECTORY)
    call([
        FFMPEG_PATH,
        # '-v', 'error',
        '-y',
        '-i', 'Jellyfish_1080_10s_1MB.webm', 
        '-vcodec', 'libx264',
        '-b:v', bv,
        '-crf', crf,
        '-vf', setscale(bv),
        '-preset', 'medium',
        (RELATIVE_OUTPUT_DIRECTORY + INPUT_file_name + EXTENSION)
    ])
def setscale(br):
    match br:
        case "1M":
            return "scale=640:480"
        case "2M":
            return "scale=1280:720"
        case "3M":
            return "scale=1920:1080"
        case "4M":
            return "scale=2048:1080"
        case "6M":
            return "scale=4096:2160"

def print_bitrate():
    output = subprocess.run([
        FFPROBE_PATH,
        # '-v', 'error',
        (RELATIVE_OUTPUT_DIRECTORY + INPUT_file_name + EXTENSION),
        '-select_streams', 'v:0',
        '-show_entries', 'stream=bit_rate',
        '-print_format', 'default=noprint_wrappers=1:nokey=1',
    ], capture_output=True, text=True).stdout
    # path = (RELATIVE_OUTPUT_DIRECTORY + 'bitrate.txt')
    # data = linecache.getline(path, 1).strip()
    # print(data)
    # gauge.set(data)
    print(output)
    # gauge.set(output)
    bitrate_gauge.set(output)
    print(bitrate_gauge)

def clean_directory(path):
    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)


# -------------------------------------------------------------------------------
# SCRIPT
# -------------------------------------------------------------------------------
start_time = time.time()
clean_directory(RELATIVE_OUTPUT_DIRECTORY)
for bitrate in BITRATE:
    for quality in QUALITY:
        encode_file(bitrate,quality)
        # assegnamo il valore alla metrica
        print_bitrate()
        # inviamo la metrica al push gateway
        #push_to_gateway("http://192.168.49.2:32197/", job="Job A", registry=registry) -> minikube
        push_to_gateway("http://192.168.49.2:30911", job="metric_extraction", registry=registry)
        #push_to_gateway("http://localhost:9090/metrics", job="gateway", registry=registry)

print("--- %s seconds ---" % (time.time() - start_time))
