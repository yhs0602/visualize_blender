import os

from PIL import Image

# 이 스크립트는 주어진 디렉토리 내의 이미지들을 찾아서, 각 이미지의 오른쪽 절반을 잘라내어 새로운 파일로 저장하고 왼쪽 절반은 '_original' 접미사와 함께 저장합니다.
# 'img_list' 딕셔너리에 정의된 특정 이미지 번호를 기반으로, 'blender'와 'dtu' 디렉토리 내의 서브디렉토리를 탐색하여 해당 이미지를 찾습니다.
# 스크립트는 'base_dir' 경로 내의 'blender'와 'dtu' 디렉토리를 대상으로 이미지들을 찾아내고, 이미지 이름에서 특정 문자열을 제거하여 최종 출력 파일의 이름을 결정합니다.

img_list = {
    "blender": {
        "chair": 8,
        "materials": 19,
    },
    "dtu": {
        "scan63": 2,
        "scan65": 3,
    },
}


def crop_image(img_file, out_path):
    if ".DS_Store" in img_file:
        return
    print(f"{img_file} -> {out_path}")
    # use pil to crop image (divide width by 2 and take the right half)
    img = Image.open(img_file)
    width, height = img.size
    img_right = img.crop((int(width / 2), 0, width, height))
    img_right.save(out_path)
    # save left as _original
    img_left = img.crop((0, 0, int(width / 2), height))
    # determine the image name
    original_name = (
        out_path.replace("dist-", "").replace("no_surface-", "").replace("topk-", "")
    )
    img_left.save(original_name.replace(".png", "_original.png"))


def find_images(base_dir, replacement, key):
    for file in os.listdir(base_dir):
        # search for directories
        if os.path.isdir(os.path.join(base_dir, file)):
            exp_name = file.replace("uncert_neus-acc-frontier-", "")
            exp_name = exp_name.replace(replacement, "-")
            for d in os.listdir(os.path.join(base_dir, file)):
                if os.path.isdir(os.path.join(base_dir, file, d)):
                    for datetime_folder in os.listdir(os.path.join(base_dir, file, d)):
                        if os.path.isdir(
                            os.path.join(base_dir, file, d, datetime_folder)
                        ):
                            output_images_folder = os.path.join(
                                base_dir, file, d, datetime_folder, "output_images"
                            )
                            num = img_list[key][exp_name.split("-")[-1]]
                            img_file = os.path.join(
                                output_images_folder, f"img_{num}.png"
                            )
                            out_path = os.path.join("cropped_image", f"{exp_name}.png")
                            print(exp_name)
                            crop_image(img_file, out_path)


def main(base_dir):
    blender_dir = os.path.join(base_dir, "blender")
    dtu_dir = os.path.join(base_dir, "dtu")
    find_images(blender_dir, "-100k1k-precrop6-Freq40k-total10-", "blender")
    find_images(dtu_dir, "-60k1k-Freq30k-total10Mask-2Labsph-5e5-", "dtu")


if __name__ == "__main__":
    main("/Users/yanghyeonseo/ablation/")
