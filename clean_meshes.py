import copy
import os

import numpy as np
import open3d as o3d


def clean_mesh(path: str):
    # Load the mesh
    mesh = o3d.io.read_triangle_mesh(path)
    out_name = path.split("/")[-1].split(".")[0]
    out_ply_name = f"{out_name}_cleaned.ply"

    # Check if the mesh contains multiple disjoint objects

    # Cluster the mesh into disjoint subsets
    (
        triangle_clusters,
        cluster_n_triangles,
        cluster_area,
    ) = mesh.cluster_connected_triangles()
    triangle_clusters = np.asarray(triangle_clusters)
    cluster_n_triangles = np.asarray(cluster_n_triangles)
    cluster_area = np.asarray(cluster_area)
    mesh_0 = copy.deepcopy(mesh)
    print(f"{cluster_n_triangles=}")
    max_n_triangles = cluster_n_triangles.max()
    triangles_to_remove = cluster_n_triangles[triangle_clusters] < max_n_triangles
    mesh_0.remove_triangles_by_mask(triangles_to_remove)
    mesh_0.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh_0])

    # Save the largest object
    o3d.io.write_triangle_mesh(f"cleaned_ply/{out_ply_name}", mesh_0)

    print(f"Saved the object with the most vertices to cleaned_ply/{out_ply_name}")


if __name__ == '__main__':
    for file in os.listdir("done_ply"):
        if file.endswith(".ply"):
            clean_mesh(f"done_ply/{file}")
