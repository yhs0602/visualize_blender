import math

import numpy as np
import open3d as o3d


def render_mesh(
    filename: str, blender_num: int = 40, camera_angle_x=0.6911112070083618
):
    # Load your PLY file
    # r40
    mesh = o3d.io.read_triangle_mesh(filename)
    print("Loaded mesh")
    stepsize = 0.031415926535897934
    rotate_angle = math.pi - stepsize * blender_num * 2
    oscilation = (np.cos(math.radians(stepsize * blender_num)) + 1) / 2 * 0.7
    rotate_matrix = mesh.get_rotation_matrix_from_xyz((oscilation, 0, rotate_angle))
    print(rotate_matrix)

    # 가정: 카메라의 종횡비(aspect ratio)가 16:9라고 가정
    aspect_ratio = 9.0 / 9.0
    camera_angle_y = 2 * math.atan(math.tan(camera_angle_x / 2) / aspect_ratio)

    blender_to_open3d = np.array(
        [
            [1, 0, 0, 0],  # Keep X-axis the same
            [0, 0, 1, 0],  # Invert Z-axis
            [0, -1, 0, 0],  # Swap Y-axis with Z-axis
            [0, 0, 0, 1],  # Homogeneous coordinate
        ]
    )
    mesh = mesh.rotate(rotate_matrix, center=mesh.get_center())
    # transform_matrix = np.array(
    #     [
    #         [
    #             0.9297775030136108,
    #             0.1426766961812973,
    #             -0.339348167181015,
    #             -1.3679561614990234
    #         ],
    #         [
    #             -0.36812204122543335,
    #             0.36036309599876404,
    #             -0.8571024537086487,
    #             -3.4550905227661133
    #         ],
    #         [
    #             7.450580596923828e-09,
    #             0.9218361377716064,
    #             0.38757991790771484,
    #             1.5623846054077148
    #         ],
    #         [
    #             0.0,
    #             0.0,
    #             0.0,
    #             1.0
    #         ]
    #     ]
    # )
    mesh = mesh.transform(blender_to_open3d)  #
    # mesh = mesh.transform(transform_matrix)
    # mesh.paint_uniform_color([0.8, 0.8, 0.8])
    mesh.compute_vertex_normals()
    # Render the mesh
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=filename)
    vis.add_geometry(mesh)
    view_control = vis.get_view_control()
    view_control.change_field_of_view(camera_angle_y)
    vis.run()  # This will open a window to visualize the mesh
    vis.capture_screen_image(f"{filename}.png")
    vis.destroy_window()


if __name__ == "__main__":
    render_mesh(
        "cleaned_ply/uncert_neus-acc-frontier-dist-200k2k-precropW12-total20-mic_new_cleaned.ply",
        blender_num=144,
    )
