from io import BytesIO
from random import randint
from app import app
from ftplib import FTP
import urllib.request
from flask import render_template
from PIL import Image
from base64 import b64encode
import re

BOM_SERVER = 'ftp.bom.gov.au'
RADAR_DIR = 'anon/gen/radar/'

ftp = FTP(BOM_SERVER)  # connect to host, default port
ftp.login()     

ftp.cwd(RADAR_DIR)

locations = { 
  "IDR98D": "Taroom, QLD",
  "IDR97D": "Mildura, VIC",
  "IDR96D": "Yeoval, NSW",
  "IDR95D": "Rainbow, VIC",
  "IDR94D": "Hillston, NSW",
  "IDR93D": "Brewarrina, NSW",
  "IDR79D": "Watheroo, WA",
  "IDR77D": "Warruwi, NT",
  "IDR76D": "Hobart, TAS",
  "IDR75D": "Mount Isa, QLD",
  "IDR74D": "Greenvale, QLD",
  "IDR71D": "Terrey Hills, NSW",
  "IDR70D": "Perth, WA",
  "IDR66D": "Mt Stapylton, QLD",
  "IDR64D": "Buckland Park, SA",
  "IDR58D": "South Doodlakine, WA",
  "IDR52D": "Takone, TAS",
  "IDR48D": "Kalgoorlie, WA",
  "IDR46D": "Adelaide, SA",
  "IDR40D": "Canberra, ACT",
  "IDR38D": "Newdegate, WA",
  "IDR33D": "Ceduna, SA",
  "IDR32D": "Esperance, WA",
  "IDR31D": "Albany, WA",
  "IDR17D": "Broome, WA",
  "IDR15D": "Dampier, WA",
  "IDR08D": "Gympie, QLD",
  "IDR06D": "Geraldton, WA",
  "IDR04D": "Newcastle, NSW",
  "IDR03D": "Wollongong, NSW",
  "IDR02D": "Melbourne, VIC",
  "IDR01D": "Broadmeadows, VIC",
}

@app.route('/')
def home():
  files = ftp.nlst()
  pngs = [ f for f in files if re.search("IDR[0-9]+D.T.[0-9]*.png", f)]
  png = pngs[randint(0, len(pngs))]
  loc = locations[png.split(".T")[0]]
  with urllib.request.urlopen(f'ftp://{BOM_SERVER}/{RADAR_DIR}/{png}') as f:
    img = Image.open(f)
    # crop out timestamp and banner
    img = img.crop((2, 20, img.width-2, img.height - 20))
    image_io = BytesIO()
    img.save(image_io, 'PNG')
    data = b64encode(image_io.getvalue()).decode('ascii')
    return render_template('home.html', src=data, loc=loc)