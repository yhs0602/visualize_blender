import copy

import numpy as np
import open3d as o3d
import math

from open3d.cpu.pybind.camera import PinholeCameraParameters

if __name__ == "__main__":
    # Load your PLY file
    # r40
    mesh = o3d.io.read_triangle_mesh(
        "uncert_neus-acc-frontier-dist-200k2k-precropW12-total20-hotdog_new.ply"
    )
    print("Loaded mesh")

    # # Assuming you have 4x4 numpy matrices for transformations
    # camtoworld_matrix = np.array(
    #     [
    #         [
    #             0.9702627062797546,
    #             -0.01474287174642086,
    #             -0.2416049838066101,
    #             0.4790847897529602
    #         ],
    #         [
    #             0.00747991306707263,
    #             0.9994929432868958,
    #             -0.03095099702477455,
    #             0.03457245975732803
    #         ],
    #         [
    #             0.2419387847185135,
    #             0.028223413974046707,
    #             0.9698809385299683,
    #             -1.8645597696304321
    #         ],
    #         [
    #             0.0,
    #             0.0,
    #             0.0,
    #             1.0
    #         ]
    #     ]
    # ).T
    # worldtogt_matrix = np.array(
    #     [
    #         [
    #             313.87957763671875,
    #             0.0,
    #             0.0,
    #             40.458553314208984
    #         ],
    #         [
    #             0.0,
    #             313.87957763671875,
    #             0.0,
    #             -12.011771202087402
    #         ],
    #         [
    #             0.0,
    #             0.0,
    #             313.87957763671875,
    #             609.5082397460938
    #         ],
    #         [
    #             0.0,
    #             0.0,
    #             0.0,
    #             1.0
    #         ]
    #     ]
    # ).T
    transform_matrix = np.array(
        [
            [
                0.8090174198150635,
                0.32844194769859314,
                -0.48745936155319214,
                -1.9650115966796875,
            ],
            [
                -0.5877846479415894,
                0.45206230878829956,
                -0.670931339263916,
                -2.704610824584961,
            ],
            [0.0, 0.829316258430481, 0.5587794184684753, 2.252511978149414],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    print(transform_matrix.T)
    # 가정: 카메라의 종횡비(aspect ratio)가 16:9라고 가정
    aspect_ratio = 16.0 / 9.0
    camera_angle_x = 0.6911112070083618  # Blender에서 가져온 값
    camera_angle_y = 2 * math.atan(math.tan(camera_angle_x / 2) / aspect_ratio)

    # invert y coordinates
    # transform_matrix = np.array(
    #     [
    #         [
    #             1,
    #             0,
    #             0,
    #             0
    #         ],
    #         [
    #             0,
    #             -1,
    #             0,
    #             0
    #         ],
    #         [
    #             0,
    #             0,
    #             1,
    #             0
    #         ],
    #         [
    #             0,
    #             0,
    #             0,
    #             1
    #         ]
    #     ]
    # )

    # The mesh appears to be flipped upside down. To correct this, we'll transform it by rotating it 180 degrees around the x-axis.
    pi = 3.141592653589793
    # transformation_matrix = mesh.get_rotation_matrix_from_xyz((0, 0, pi / 2))
    # mesh = mesh.rotate(transformation_matrix, center=mesh.get_center())
    # mesh = mesh.transform(transform_matrix)
    # mesh = mesh.transform(worldtogt_matrix)
    print("Computed mesh normals")
    blender_to_open3d = np.array(
        [
            [1, 0, 0, 0],  # Keep X-axis the same
            [0, 0, 1, 0],  # Invert Z-axis
            [0, -1, 0, 0],  # Swap Y-axis with Z-axis
            [0, 0, 0, 1],  # Homogeneous coordinate
        ]
    )

    mesh = mesh.transform(blender_to_open3d @ transform_matrix)
    # mesh = mesh.transform([[-1, 0, 0, 0],
    #                 [0, 1, 0, 0],
    #                 [0, 0, 1, 0],
    #                 [0, 0, 0, 1]])
    mesh.compute_vertex_normals()
    # Render the mesh

    # Define camera parameters
    camera_location = np.array([0, 4.0, 0.5])  # Camera position
    look_at_target = np.array([0, 0, 0])  # The point to look at (origin in this case)
    up_vector = np.array([0, 1, 0])  # 'UP_Y' in Blender
    view_matrix = o3d.geometry.get_rotation_matrix_from_xyz(camera_location)
    view_matrix = np.linalg.inv(view_matrix)
    # Inverting the matrix, as Open3D view matrix is the inverse of the model matrix

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    view_control = vis.get_view_control()
    view_control.change_field_of_view(camera_angle_y)
    parameter = PinholeCameraParameters()
    parameter.extrinsic = view_matrix
    view_control.convert_from_pinhole_camera_parameters(parameter)
    vis.add_geometry(mesh)
    # for i in range(8):
    #     for j in range(8):
    #         for k in range(8):
    #             # vis.update_geometry()
    #             vis.poll_events()
    #             vis.update_renderer()
    #             vis.capture_screen_image(f"temp_{i}-{j}-{k}.png")
    #             mesh = copy.deepcopy(original_mesh)
    #             vis.add_geometry(mesh)
    #             transformation_matrix = mesh.get_rotation_matrix_from_xyz((i * pi / 4, j * pi / 4, k * pi / 4))
    #             mesh = mesh.rotate(transformation_matrix, center=mesh.get_center())
    #             vis.update_geometry(mesh)
    #             vis.remove_geometry(mesh)

    vis.run()  # This will open a window to visualize the mesh
    vis.capture_screen_image("rendered_image.png")
    vis.destroy_window()
