from PIL import Image


# Define the path format for the images
def get_image_path(object_name, index):
    return f"./{object_name}_{index}.png"


# Define the dictionary of input images' indices
indices_dict = {"mic": [1, 2, 7], "ship": [2, 5, 7], "hotdog": [3, 5, 9]}


def main():
    # Calculate the number of rows and the size of the final image
    num_rows = len(indices_dict)
    num_columns = 3
    image_size = (256, 256)  # Assuming each image is 256x256 pixels

    # Create a new image with white background
    final_image_width = image_size[0] * num_columns
    final_image_height = image_size[1] * num_rows
    final_image = Image.new(
        "RGB", (final_image_width, final_image_height), color="white"
    )

    # Load images and paste them into the final image
    for row, (object_name, indices) in enumerate(indices_dict.items()):
        for col, index in enumerate(indices):
            try:
                # Load the image
                img_path = get_image_path(object_name, index)
                with Image.open(img_path) as img:
                    # Resize image if it's not the expected size
                    if img.size != image_size:
                        img = img.resize(image_size)

                    # Compute the position where to paste the image in the final image
                    position = (col * image_size[0], row * image_size[1])
                    final_image.paste(img, position)
            except FileNotFoundError:
                print(f"File {img_path} not found. Skipping.")

    # Save the final image
    final_image_path = "/mnt/data/compiled_figure.png"
    final_image.save(final_image_path)


if __name__ == "__main__":
    main()
