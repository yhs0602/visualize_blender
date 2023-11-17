import os

from PIL import Image

if __name__ == "__main__":
    for file in os.listdir("done_cleaned"):
        if file.endswith(".png"):
            print(file)
            im = Image.open(f"done_cleaned/{file}")
            width, height = im.size
            print(width, height)
            # center crop by to 900 x 900
            left = int((width - 900) / 2)
            top = int((height - 900) / 2)
            right = int((width + 900) / 2)
            bottom = int((height + 900) / 2)
            im = im.crop((left, top, right, bottom))
            im.save(f"done_cleaned/{file}_cropped.png")

            # os.system(f"mv done_cleaned/{file} cleaned_ply/{file}")
