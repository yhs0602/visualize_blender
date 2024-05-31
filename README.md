# Visualize Blender

## center_crop.py
이미지를 900x900으로 중앙을 기준으로 crop합니다.

## clean_5_meshes.py
이 코드는 주어진 경로에 있는 메시(mesh) 파일을 불러와서, 여러 개의 분리된 객체들 중 가장 큰 객체를 유지하고 나머지를 제거합니다.
메시의 각 부분을 클러스터링하여 가장 큰 클러스터만 남기고 나머지는 삭제한 후, 정점의 노멀을 다시 계산하고 시각화합니다.
처리된 메시는 'cleaned_ablation_meshes' 디렉토리에 "_cleaned.ply" 형식의 이름으로 저장합니다.

## render_blender_5.py
Blender 각도를 계산해서 적절한 위치의 카메라에서 그림을 그려서 화면에 그려줍니다. 마우스로 드래그하여 각도를 맞추고 ESC를 누르면 저장됩니다
