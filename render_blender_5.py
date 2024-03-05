import os

from generalized_hotdog import render_mesh

blender_nums = {
    "hotdog": 40,
    "ship": 144,
    "mic": 144,
    "chair": 64,
    "materials": 152,  # 19
    "ficus": 136,  # 17
}

if __name__ == "__main__":
    dir_name = "cleaned_5_meshes"
    for file in os.listdir(dir_name):
        print(file)
        if not file.endswith(".ply"):
            continue  # .DS_Store
        algorithm, obj, cleaned = file.split(".")[0].split("_")
        # obj = file.split(".")[0]
        print(f"{algorithm=}{obj=}")
        if file.endswith(".ply"):
            render_mesh(
                filename=f"{dir_name}/{file}",
                blender_num=blender_nums[obj],
                # camera_angle_x=camera_angle_x
            )
