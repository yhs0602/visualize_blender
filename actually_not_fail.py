# Move cleaned_fvs_meshes to again_cleaned_fvs_meshes
# if name is in fail_list
import os
import shutil

from clean_again_fvs import fail_list


def move_actually_not_failed_files():
    for file in os.listdir("cleaned_fvs_meshes"):
        if file in fail_list:
            print(file)
            shutil.move(
                f"cleaned_fvs_meshes/{file}", f"again_cleaned_fvs_meshes/{file}"
            )


if __name__ == "__main__":
    move_actually_not_failed_files()
