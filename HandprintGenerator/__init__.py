import os

#cloudinary global setup
import cloudinary
import cloudinary.uploader
import cloudinary.api
cloudinary.config( 
  cloud_name = os.environ['CLOUDINARY_NAME'], 
  api_key = os.environ['CLOUDINARY_KEY'], 
  api_secret = os.environ['CLOUDINARY_SECRET'] 
)