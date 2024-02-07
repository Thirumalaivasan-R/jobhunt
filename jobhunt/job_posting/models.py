from django.db import models
from PIL import Image,ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.

def resize_and_crop(image, size):
    img = Image.open(image)

    # Create a new blank image with a white background
    new_img = Image.new("RGB", size, "white")

    # If the image has an alpha channel (transparency), convert it to a white background
    if img.mode == 'RGBA':
        img = Image.alpha_composite(Image.new('RGBA', img.size, "white"), img)
        img = img.convert('RGB')

    # Resize the image while maintaining the aspect ratio
    img.thumbnail(size)

    # Calculate the positioning to center the image
    position = ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)

    # Paste the image onto the new blank image
    new_img.paste(img, position)

    # Save the image as JPEG
    output = BytesIO()
    new_img.save(output, format='JPEG', quality=75)
    output.seek(0)

    return InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}.jpg",
                                'image/jpeg', sys.getsizeof(output), None)
                                
class Job(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=250)
    image = models.ImageField(upload_to='job_images/')  # Assuming you want to upload job images
    published_at = models.DateTimeField(auto_now_add=True)
    about_company = models.TextField(default= 'none')
    company_name = models.CharField(max_length=100, default= 'none')
    company_website = models.URLField(default= 'none')
    job_role = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    job_type = models.TextField(default= 'none')
    experience = models.TextField(default= 'none')
    qualification = models.TextField(default= 'none')
    batch = models.TextField(default= 'none')
    package = models.TextField(default= 'none')
    job_details = models.TextField(default= 'none')
    apply_link = models.URLField(default='none')

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_and_crop(self.image, (500, 500))
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.title