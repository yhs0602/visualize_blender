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
}

if __name__ == "__main__":
    # for each blender plies
    for file in os.listdir("cleaned_ply"):
        if file.endswith(".ply") and not file.startswith("zdtu"):
            print(file)
            obj = file.split("-")[-1].split("_")[0]
            print(obj)
            render_mesh(
                filename=f"cleaned_ply/{file}",
                blender_num=blender_nums[obj],
                # camera_angle_x=camera_angle_x
            )
