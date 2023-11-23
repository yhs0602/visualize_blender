import copy
import os

import numpy as np
import open3d as o3d


def clean_mesh(path: str):
    # Load the mesh
    mesh = o3d.io.read_triangle_mesh(path)
    out_name = path.split("/")[-1].split(".")[0]
    out_name = (
        out_name.replace("uncert_neus-acc-frontier-", "")
        .replace("-100k1k-precrop6-Freq40k-total10-", "-")
        .replace("-60k1k-Freq30k-total10Mask-2Labsph-5e5-", "-")
        .replace("-60k1k-Freq30k-total10Mask-", "-")
    )
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
    max_n_triangles = cluster_n_triangles.mean() * 0.5
    triangles_to_remove = cluster_n_triangles[triangle_clusters] < max_n_triangles
    mesh_0.remove_triangles_by_mask(triangles_to_remove)
    mesh_0.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh_0])

    # Save the largest object
    # get the output name

    o3d.io.write_triangle_mesh(f"cleaned_ablation_meshes/{out_ply_name}", mesh_0)

    print(f"Saved the object with the most vertices to cleaned_ply/{out_ply_name}")


if __name__ == "__main__":
    for file in os.listdir("/Users/yanghyeonseo/ablation/meshes"):
        if file.endswith(".ply") and "material" in file:
            clean_mesh(f"/Users/yanghyeonseo/ablation/meshes/{file}")
