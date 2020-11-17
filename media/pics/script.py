import PIL
from PIL import Image
import os
dir = os.getcwd()
print(dir)

for file in os.listdir(dir):
  filestatus = os.stat(file)
  if filestatus.st_size > 300000:
    print(file+'\n')
    try:
      basewidth = 300
      img = Image.open(file)
      fileformat = img.format
      wpercent = (basewidth / float(img.size[0]))
      hsize = int((float(img.size[1]) * float (wpercent)))
      img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
      img.save(file,format=fileformat)
    except:
      print('--------------------------------------error: ' +file+'\n')
