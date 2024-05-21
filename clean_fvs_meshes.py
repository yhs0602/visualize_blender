import copy
import os

import numpy as np
import open3d as o3d


# 이 코드는 주어진 경로에 있는 메시(mesh) 파일을 불러와서, 여러 개의 분리된 객체들 중 가장 큰 객체를 유지하고 나머지를 제거합니다.
# 메시의 각 부분을 클러스터링하여 가장 큰 클러스터만 남기고 나머지는 삭제한 후, 정점의 노멀을 다시 계산하고 시각화합니다.
# 처리된 메시는 'cleaned_ablation_meshes' 디렉토리에 "_cleaned.ply" 형식의 이름으로 저장합니다.
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
    max_n_triangles = cluster_n_triangles.mean() * 1.3
    triangles_to_remove = cluster_n_triangles[triangle_clusters] < max_n_triangles
    mesh_0.remove_triangles_by_mask(triangles_to_remove)
    mesh_0.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh_0])

    # Save the largest object
    # get the output name

    o3d.io.write_triangle_mesh(f"cleaned_fvs_meshes/{out_ply_name}", mesh_0)

    print(
        f"Saved the object with the most vertices to cleaned_fvs_meshes/{out_ply_name}"
    )


def clean_folder(dir_name):
    for file in os.listdir(dir_name):
        print(file)
        splitted = file.split(".")[0].split("-")
        algorithm = splitted[0]
        scanxxx = splitted[-1]
        # obj = file.split(".")[0]
        print(f"{algorithm=}{scanxxx=}")
        if file.endswith(".ply"):
            clean_mesh(f"{dir_name}/{file}")


if __name__ == "__main__":
    dir1_name = "fvs_meshes/fvs10_meshes"
    dir2_name = "fvs_meshes/fvs20_meshes"
    out_dir = "cleaned_fvs_meshes"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    clean_folder(dir1_name)
    clean_folder(dir2_name)
