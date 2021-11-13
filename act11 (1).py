# -*- encoding: utf-8 -*-

#Daniel Ernesto Rangel Perez
#Esteban Osorio Rodriguez

import argparse
import requests
import os
from lxml import html
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def decode_gps_info(exif): #exif: Es la forma en que viene compactado los datos 
    gpsinfo = {}
    if 'GPSInfo' in exif:
        #Parse geo references.
        Nsec = exif['GPSInfo'][2][2]
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][3] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        lon = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : lat, "Lon" : lon}

def get_exif_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret

def saveMeta():
    ruta = "images"
    os.chdir(ruta)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            #print(os.path.join(root, name))
            print("[+] Metadata for file: %s " %(name))
            try:
                exifData = {}
                exif = get_exif_metadata(name)
                for metadata in exif: 
                    file = open(str(name)+"metadata.txt","a")
                    file.write(str(metadata) + ":" + str(exif[metadata]) + "\n")
                    file.close()
                print("\n")
            except:
                import sys, traceback
                traceback.print_exc(file = sys.stdout)

def scrapingImages():
    url = a
    print("\nObteniendo imagenes de la url:"+ url)
    
    try:
        response = requests.get(url)  
        parsed_body = html.fromstring(response.text)

        # expresion regular para obtener imagenes
        images = parsed_body.xpath('//img/@src')

        print ('Imagenes %s encontradas' % len(images))
    
        #crea la carpeta donde se guardan las imagenes
        os.system("mkdir images")
    
        for image in images:
            if image.startswith("http") == False:
                download = url + image
            else:
                download = image
            print(download)
            # descarga las imagenes en el directorio que se le dio antes
            r = requests.get(download)
            f = open('images/%s' % download.split('/')[-1], 'wb')
            f.write(r.content)
            f.close()
                
    except Exception as e:
            print(e)
            print ("Error conexion con " + url)
            pass

#argparse

description = """Script para ver metadata de imagenes en la web

                Ejemplos de uso:

            + py e11.py -link link.com"""

parser = argparse.ArgumentParser(description='scraping y metadata',

                                 epilog=description,

                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-link", metavar='link', dest='link', help="Link de busqueda",

                    required=True)

params = parser.parse_args()

a = (params.link)

scrapingImages()
saveMeta()
