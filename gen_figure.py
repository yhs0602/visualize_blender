from PIL import Image


# 이 스크립트는 'indices_dict'에 정의된 객체 이름과 인덱스를 사용하여 여러 개의 이미지 파일을 로드하고, 이들을 하나의 큰 이미지에 그리드 형태로 병합합니다.
# 각각의 이미지는 256x256 픽셀 크기로 가정하며, 이 크기가 맞지 않는 경우 이미지는 해당 크기로 조정됩니다.
# 최종 이미지는 각 객체 별로 열에 배치되고, 'compiled_figure.png'라는 파일명으로 저장됩니다.
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
    final_image_path = "./compiled_figure.png"
    final_image.save(final_image_path)


if __name__ == "__main__":
    main()
