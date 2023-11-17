import math

import numpy as np
import open3d as o3d
from open3d.cpu.pybind.camera import PinholeCameraIntrinsic
from open3d.cpu.pybind.visualization import ViewControl

if __name__ == "__main__":
    # Load your PLY file
    # test_indices = [1, 9, 12, 15, 24, 27, 32, 35, 42, 46]
    # image_42

    mesh = o3d.io.read_triangle_mesh(
        "cleaned_ply/uncert_neus-acc-frontier-dist-120k2k-total20Mask-scan65_new_cleaned.ply"
    )
    print("Loaded mesh")

    # prepare world to gt
    world_to_gt = np.array(
        [
            [223.3332061767578, 0.0, 0.0, 43.391822814941406],
            [0.0, 223.3332061767578, 0.0, -18.58791732788086],
            [0.0, 0.0, 223.3332061767578, 613.8095703125],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    # prepare cam to world
    cam_to_world = np.array(
        [
            [
                0.11632565408945084,
                0.03981569781899452,
                -0.9924127459526062,
                2.705883502960205,
            ],
            [
                -0.90257728099823,
                0.42125049233436584,
                -0.08889497071504593,
                0.24161799252033234,
            ],
            [
                0.41451495885849,
                0.9060699343681335,
                0.08493898063898087,
                -0.2335568517446518,
            ],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    intrinsics = np.array(
        [
            [925.5454711914062, -0.00010295728134224191, 199.42562866210938, 0.0],
            [0.0, 922.6158447265625, 198.1027374267578, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    # # 가정: 카메라의 종횡비(aspect ratio)가 16:9라고 가정
    # aspect_ratio = 9.0 / 9.0
    # camera_angle_x = 0.6911112070083618  # Blender에서 가져온 값
    # camera_angle_y = 2 * math.atan(math.tan(camera_angle_x / 2) / aspect_ratio)

    blender_to_open3d = np.array(
        [
            [0, -1, 0, 0],  # Keep X-axis the same
            [0, 0, -1, 0],  # Invert Z-axis
            [1, 0, 0, 0],  # Swap Y-axis with Z-axis
            [0, 0, 0, 1],  # Homogeneous coordinate
        ]
    )
    mesh = mesh.transform(world_to_gt)
    mesh = mesh.transform(cam_to_world)
    # mesh = mesh.transform(blender_to_open3d)  #
    mesh.compute_vertex_normals()
    # Render the mesh
    vis = o3d.visualization.Visualizer()
    # width = 384
    # height = 384
    intrinsic_matrix = np.array(
        [
            [925.5454711914062, -0.00010295728134224191, 199.42562866210938, 0.0],
            [0.0, 922.6158447265625, 198.1027374267578, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    # fx = 925.5454711914062
    # fy = 922.6158447265625
    # cx = 199.42562866210938
    # cy = 198.1027374267578
    o3d_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
    width = int(intrinsic_matrix[0, 2]) * 2
    height = int(intrinsic_matrix[1, 2]) * 2
    o3d_camera_intrinsic.set_intrinsics(
        width=width,  # Assuming principal point is at the center
        height=height,
        fx=intrinsic_matrix[0, 0],
        fy=intrinsic_matrix[1, 1],
        cx=int(intrinsic_matrix[0, 2]) - 0.5,
        cy=int(intrinsic_matrix[1, 2]) - 0.5,
    )
    vis.create_window(width=width, height=height)
    vis.add_geometry(mesh)
    # view_control = vis.get_view_control()
    # view_control.change_field_of_view(camera_angle_y)
    # view_control: ViewControl = vis.get_view_control()
    # pinhole_camera_parameters = view_control.convert_to_pinhole_camera_parameters()
    # pinhole_camera_parameters.intrinsic = intrinsic
    # view_control.convert_from_pinhole_camera_parameters(pinhole_camera_parameters)
    vis.run()  # This will open a window to visualize the mesh
    vis.capture_screen_image("rendered_image.png")
    vis.destroy_window()
