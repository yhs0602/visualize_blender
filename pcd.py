import open3d as o3d
import numpy as np

print("Load a ply point cloud, print it, and render it")
ply_point_cloud = o3d.data.PLYPointCloud()
pcd = o3d.io.read_point_cloud(ply_point_cloud.path)
print(pcd)
print(np.asarray(pcd.points))
print("Downsample the point cloud with a voxel of 0.05")
downpcd = pcd.voxel_down_sample(voxel_size=0.05)
vis = o3d.visualization.Visualizer()
vis.create_window(visible=True)
opt = vis.get_render_option()
opt.background_color = [211, 211, 211]
vis.add_geometry(downpcd)
vis.run()
# o3d.visualization.draw_geometries([downpcd],
#                                  zoom=0.3412,
#                                  front=[0.4257, -0.2125, -0.8795],
#                                  lookat=[2.6172, 2.0475, 1.532],
#                                  up=[-0.0694, -0.9768, 0.2024])
