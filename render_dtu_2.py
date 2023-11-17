import cv2
import numpy as np
import open3d as o3d
from open3d.cpu.pybind.camera import PinholeCameraParameters
from open3d.cpu.pybind.visualization import ViewControl

if __name__ == "__main__":
    # Load your PLY file
    # test_indices = [1, 9, 12, 15, 24, 27, 32, 35, 42, 46]
    # image_42

    mesh = o3d.io.read_triangle_mesh(
        "cleaned_ply/uncert_neus-acc-frontier-dist-120k2k-total20Mask-scan65_new_cleaned.ply"
    )
    print("Loaded mesh")
    pos_mat = np.array(
        [
            [-1068.551022, -2563.835042, 1152.472201, -204923.261624],
            [-479.238785, 1193.754837, 2653.531395, -1207831.122811],
            [-0.995146, 0.097946, 0.009509, 648.082116],
        ]
    )
    # pos_mat = np.array(
    #     [
    #         [-480.507214, -2683.730823, 1268.836186, -306480.177291],  # 1268.836186
    #         [-499.578500, 1159.506706, 2664.941803, -1214196.736115],
    #         [-0.992413, -0.088895, 0.084939, 598.230009],
    #     ]
    # )

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
    # mesh = mesh.transform(pos_mat)
    # mesh = mesh.transform(cam_to_world)
    mesh = mesh.transform(blender_to_open3d)  #
    mesh.compute_vertex_normals()
    # Render the mesh
    vis = o3d.visualization.Visualizer()
    # width = 384
    # height = 384
    # intrinsic_matrix = np.array(
    #     [
    #         [925.5454711914062, -0.00010295728134224191, 199.42562866210938, 0.0],
    #         [0.0, 922.6158447265625, 198.1027374267578, 0.0],
    #         [0.0, 0.0, 1.0, 0.0],
    #         [0.0, 0.0, 0.0, 1.0],
    #     ]
    # )
    camera_mat, rot_mat, t = cv2.decomposeProjectionMatrix(pos_mat)[:3]
    camera_mat = camera_mat / camera_mat[2, 2]
    R = rot_mat[:3, :3]
    t = t[:3]
    extrinsic_mat = np.eye(4)
    extrinsic_mat[:3, :3] = R
    extrinsic_mat[:3, 3:3] = t
    o3d_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
    width = int(camera_mat[0, 2]) * 2
    height = int(camera_mat[1, 2]) * 2
    o3d_camera_intrinsic.set_intrinsics(
        width=width,  # Assuming principal point is at the center
        height=height,
        fx=camera_mat[0, 0],
        fy=camera_mat[1, 1],
        cx=int(camera_mat[0, 2]) - 0.5,
        cy=int(camera_mat[1, 2]) - 0.5,
    )

    # fx = 925.5454711914062
    # fy = 922.6158447265625
    # cx = 199.42562866210938
    # cy = 198.1027374267578
    # intrinsic = PinholeCameraIntrinsic(1, 1, intrinsic_matrix=intrinsic_matrix[:3, :3].T)
    vis.create_window(width=width, height=height)  # width=width, height=height
    vis.add_geometry(mesh)
    view_control: ViewControl = vis.get_view_control()
    # view_control.change_field_of_view(camera_angle_y)
    # view_control: ViewControl = vis.get_view_control()
    pinhole_camera_parameters: PinholeCameraParameters = (
        view_control.convert_to_pinhole_camera_parameters()
    )
    pinhole_camera_parameters.intrinsic = o3d_camera_intrinsic
    pinhole_camera_parameters.extrinsic = extrinsic_mat
    # pinhole_camera_parameters.intrinsic = intrinsic
    view_control.convert_from_pinhole_camera_parameters(pinhole_camera_parameters)
    vis.run()  # This will open a window to visualize the mesh
    vis.capture_screen_image("rendered_image.png")
    vis.destroy_window()
