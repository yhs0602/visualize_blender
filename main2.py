import math

import numpy as np
import open3d as o3d

if __name__ == "__main__":
    # Load your PLY file
    # r40
    mesh = o3d.io.read_triangle_mesh(
        "uncert_neus-acc-frontier-dist-200k2k-precropW12-total20-hotdog_new.ply"
    )
    print("Loaded mesh")
    stepsize = 0.031415926535897934
    rotate_angle = math.pi - stepsize * 40 * 2
    oscilation = (np.cos(math.radians(stepsize * 40)) + 1) / 2 * 0.7
    rotate_matrix = mesh.get_rotation_matrix_from_xyz((oscilation, 0, rotate_angle))
    print(rotate_matrix)

    # 가정: 카메라의 종횡비(aspect ratio)가 16:9라고 가정
    aspect_ratio = 9.0 / 9.0
    camera_angle_x = 0.6911112070083618  # Blender에서 가져온 값
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
    # mesh = mesh.transform(transform_matrix)
    mesh = mesh.transform(blender_to_open3d)  #
    mesh.compute_vertex_normals()
    # Render the mesh
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    view_control = vis.get_view_control()
    view_control.change_field_of_view(camera_angle_y)
    vis.run()  # This will open a window to visualize the mesh
    vis.capture_screen_image("rendered_image.png")
    vis.destroy_window()
