import os

from generalized_hotdog import render_mesh

todo_list = (
    {
        "total_10": {"hotdog": 5, "ship": 18},
        "total_20": {"mic": 18, "chair": 8},
    },
)
blender_nums = {
    "hotdog": 40,
    "ship": 144,
    "mic": 144,
    "chair": 64,
    "materials": 152,
}

if __name__ == "__main__":
    # render_mesh(
    #     "blender_ply/materials.ply",
    #     blender_num=blender_nums["materials"],
    # )
    # for each blender plies
    for file in os.listdir("new_blender_ply"):
        print(file)
        obj = file.split("-")[-1].split("_")[0]
        # obj = file.split(".")[0]
        print(obj)
        if file.endswith(".ply"):
            render_mesh(
                filename=f"new_blender_ply/{file}",
                blender_num=blender_nums[obj],
                # camera_angle_x=camera_angle_x
            )
