#connect google sheets
from google.colab import auth
import gspread
from oauth2client.client import GoogleCredentials
import pandas as pd
import numpy as np
from google.colab import drive
from PIL import Image 

def generate_images():
  #mount google drive
  drive.mount('/content/drive')

  #authenticate sheets
  auth.authenticate_user()
  gc = gspread.authorize(GoogleCredentials.get_application_default())
  worksheet = gc.open('MEC').get_worksheet(2)

  #load in data sheet
  rows = worksheet.get_all_values()
  print(rows)

  #loading dataframe into df
  df = pd.DataFrame.from_records(rows)
  df = df.iloc[:,14:25]
  df.columns = np.arange(0, 11)
  df = df.astype(str)
  df.head()

  #Combine layers
  for i in range(2, len(df)):
    order = (df.iloc[[i]]).values.tolist()
    #background load in
    background = Image.open(f"/content/{order[0][0]}.png")
    for j in [1,2,3,4,5,6,7,8,9,10]:
      j = int(j)
      layerName = f"/content/{order[0][j]}.png"
      currImg = Image.open(layerName)
      background.paste(currImg, (0,0), currImg)
    
    background.save(f"/content/drive/My Drive/NFTs/NFT{i-1}.png")
    print(f"Image {i-1} complete")

  print(i + " images have been stored in your google drive!")
