from generalized_hotdog import render_mesh

todo_list = {
    "total_10": {
        "hotdog": 5,
        "ship": 18
    },
    "total_20": {
        "mic": 18,
        "chair": 8
    },
},

if __name__ == '__main__':
    # for each blender plies

    render_mesh(
        filename=filename,
        blender_num=blender_num,
        # camera_angle_x=camera_angle_x
    )
