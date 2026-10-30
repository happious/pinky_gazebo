# Pinky Pro Gazebo · Multi Room

![Gazebo Harmonic](https://img.shields.io/badge/Gazebo-Harmonic%20%28Sim%208%29-orange)
![ROS 2 Jazzy](https://img.shields.io/badge/ROS%202-Jazzy-blue)
![Ubuntu 24.04](https://img.shields.io/badge/Ubuntu-24.04%20LTS-E95420?logo=ubuntu&logoColor=white)


Ubuntu 24.04 / ROS 2 Jazzy / Gazebo Harmonic에서 Pinky Pro를 실행하고, SLAM으로 지도를 만든 뒤 Nav2로 자율주행하는 예제입니다. 이 저장소는 로컬에서 사용한 소스와 예제 맵을 함께 제공합니다.

기본 실습 월드는 **Multi Room**입니다. World Collection은 비교 실험용으로 포함하며, SC1_square_loop에서는 바퀴가 돌아도 본체가 움직이지 않는 문제가 기록되어 있습니다.

## 구성

| 경로 | 내용 |
|---|---|
| [src/pinky_pro](src/pinky_pro) | Pinky Pro ROS 2 패키지. 외부 월드와 스폰 좌표를 전달하는 로컬 수정 포함 |
| [src/pinky_code](src/pinky_code/README.md) | 단일 목표점, 다중 waypoint 주행 및 현재 위치 출력 예제 |
| [oomwoo_gazebo](oomwoo_gazebo) | Multi Room 월드와 관련 리소스 |
| [world-collection](world-collection) | 외부 월드 모음, 실험용 |
| [maps](maps/README.md) | multi_room 및 pinky_map 예제 지도 |
| [docs/설치_실행_상세가이드.md](docs/설치_실행_상세가이드.md) | 기존 작업 기록, Launch 수정 내용, 오류 해결 상세 |

## 1. 설치 및 빌드

ROS 2 Jazzy가 설치되어 있다고 가정합니다. 이 저장소를 내려받은 폴더 자체를 워크스페이스로 사용합니다. 아래 명령은 경로를 ~/pinky_ws로 가정하므로 기존 작업 폴더가 있다면 다른 경로를 쓰고 이후 명령도 함께 바꾸세요.

새 컴퓨터에서 내려받기:

~~~bash
git clone https://github.com/happious/pinky_gazebo.git ~/pinky_ws
cd ~/pinky_ws
~~~

이미 ~/pinky_ws가 있다면 다른 빈 경로를 선택하고 이 문서의 경로도 함께 바꾸세요.

GitHub 저장소에서 내려받은 소스에는 필요한 폴더가 포함되어 있으므로 Pinky Pro와 Multi Room을 다시 clone하거나 상세가이드의 Launch 전체 교체를 반복할 필요가 없습니다.

~~~bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install -y git python3-colcon-common-extensions python3-rosdep \
  ros-jazzy-ros-gz ros-jazzy-teleop-twist-keyboard \
  ros-jazzy-slam-toolbox ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  ros-jazzy-nav2-simple-commander

# rosdep를 처음 설정하는 경우만 실행
sudo rosdep init
rosdep update

cd ~/pinky_ws
rosdep install --from-paths src/pinky_pro --ignore-src -r -y
colcon build --symlink-install --base-paths src/pinky_pro
source install/setup.bash
~~~

이미 rosdep가 초기화되어 있다면 sudo rosdep init은 생략합니다. gz sim --help가 정상 동작한다면 Gazebo 자체는 설치된 상태입니다. 의존성 설치나 빌드 오류가 나면 해당 오류를 해결한 뒤 다음 단계로 진행하세요.

## 2. 모든 터미널의 공통 설정

새 터미널마다 아래를 실행합니다. ROS_DOMAIN_ID는 모든 터미널에서 같은 값이어야 합니다.

~~~bash
source /opt/ros/jazzy/setup.bash
source ~/pinky_ws/install/setup.bash
export ROS_DOMAIN_ID=0
~~~

## 3. Gazebo + Multi Room + Pinky 실행

터미널 1:

~~~bash
ros2 launch pinky_bringup bringup_sim.launch.xml \
  sim:=gz world:=$HOME/pinky_ws/oomwoo_gazebo/worlds/multi_room.sdf
~~~

sim의 기본값은 mujoco이므로 Gazebo는 sim:=gz를 지정합니다. Multi Room은 별도 ROS 패키지로 빌드하지 않고 SDF를 사용합니다.

기본 스폰 위치는 x=-0.971979, y=0.028805, z=0.1m, yaw=-3.130950rad입니다. 다른 위치가 필요하면 위 명령 끝에 x:=1.0 y:=2.0 z:=0.1 yaw:=1.57을 추가합니다. 월드마다 바닥과 벽을 피해 위치를 지정하세요.

Pinky 기본 맵 월드:

~~~bash
ros2 launch pinky_bringup bringup_sim.launch.xml sim:=gz world_name:=pinky_map.world
~~~

터미널 2 — 키보드 조종:

~~~bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
~~~

i는 전진, 쉼표는 후진, j/l은 좌우 회전, k는 정지입니다. q/z/w/x/e/c는 속도 조절키입니다. 조종할 때 해당 터미널에 포커스를 두세요.

## 4. SLAM 지도 생성 및 저장

Gazebo와 키보드 조종은 유지합니다. 다음 두 명령은 각각 별도 터미널에서 실행합니다.

~~~bash
# 터미널 3 — SLAM Toolbox
ros2 launch pinky_navigation gz_map_building.launch.xml
~~~

~~~bash
# 터미널 4 — SLAM RViz
ros2 launch pinky_navigation gz_map_view.launch.xml
~~~

키보드로 방과 복도를 천천히 이동하며 RViz에서 지도를 확인합니다. SLAM이 실행 중일 때 별도 터미널에서 저장합니다. 제공된 예제 맵을 보존하려면 새 이름을 사용하세요.

~~~bash
mkdir -p ~/pinky_ws/maps
ros2 run nav2_map_server map_saver_cli -f ~/pinky_ws/maps/my_multi_room \
  --ros-args -p use_sim_time:=true -p save_map_timeout:=10.0
~~~

my_multi_room.yaml과 my_multi_room.pgm이 생성됩니다. 두 파일을 함께 보관해야 합니다.

## 5. 저장한 지도에서 Nav2 주행

SLAM과 SLAM용 RViz를 종료하고 Gazebo는 유지합니다. 다음 명령은 포함된 예제 지도를 사용합니다. 직접 만든 지도라면 map 경로를 my_multi_room.yaml로 바꾸세요.

~~~bash
# 터미널 3 — Nav2
ros2 launch pinky_navigation gz_bringup_launch.xml \
  map:=$HOME/pinky_ws/maps/multi_room.yaml
~~~

~~~bash
# 터미널 4 — Nav2 RViz
ros2 launch pinky_navigation gz_nav2_view.launch.xml
~~~

RViz의 2D Pose Estimate로 실제 로봇 위치와 방향을 지정한 뒤 Nav2 Goal로 목적지를 선택합니다. Gazebo의 world 좌표와 AMCL의 map 좌표는 서로 다르므로 스폰 좌표를 초기 map 좌표로 그대로 쓰지 마세요.

~~~bash
ros2 lifecycle get /bt_navigator
ros2 topic echo /amcl_pose --once
~~~

bt_navigator가 active 상태인지 확인합니다. 예제 코드를 실행할 때는 키보드 조종과 RViz 목표 전송을 동시에 하지 마세요.

## 6. Python 주행 예제

Nav2를 먼저 실행하고 RViz에서 초기 위치를 설정합니다. 각 코드는 별도 터미널에서 하나씩 실행합니다.

| 파일 | 기능 | 수정할 값 |
|---|---|---|
| nav.py | goToPose로 한 목표점 이동, 남은 거리·시간·현재 위치 출력 | GOAL_X, GOAL_Y, GOAL_YAW |
| mult_nav.py | followWaypoints로 여러 waypoint 순차 주행 | WAYPOINTS 목록 |
| current_pose.py | /amcl_pose에서 현재 x, y, yaw 출력 | 별도 목표 설정 없음 |

~~~bash
python3 ~/pinky_ws/src/pinky_code/nav.py --ros-args -p use_sim_time:=true
~~~

~~~bash
python3 ~/pinky_ws/src/pinky_code/mult_nav.py --ros-args -p use_sim_time:=true
~~~

~~~bash
python3 ~/pinky_ws/src/pinky_code/current_pose.py --ros-args -p use_sim_time:=true
~~~

예제의 x/y는 map 기준 미터, yaw는 도(degree)입니다. Launch의 yaw는 라디안이므로 단위가 다릅니다. 하드코딩된 목표 좌표는 자신의 지도에서 이동 가능한 위치로 바꾸세요. current_pose.py로 현재 좌표를 확인할 수 있습니다. LCD 예제는 실제 하드웨어용이며 Gazebo 주행에는 필요하지 않습니다.

## 7. 주의사항 및 문제 해결

| 증상 | 확인 및 대응 |
|---|---|
| Package 'pinky_bringup' not found | 빌드 성공 여부와 install/setup.bash source 확인 |
| 로봇이 없거나 아래로 떨어짐 | world 경로와 바닥 유무 확인. gz model --list 및 gz model -m pinky -p로 확인 |
| cmd_vel이 있지만 움직이지 않음 | 키보드 입력키, 일시정지 여부, 바닥 collision 점검. SC1 월드의 주행 실패 이력 참고 |
| launch configuration 'x' does not exist | 상위와 하위 Launch의 x/y/z/yaw 인자 전달 확인 |
| XML 선언 오류 | XML 첫 줄 앞 공백·빈 줄 제거 |
| 지도 저장 Failed to spin map subscription | 모든 터미널의 ROS_DOMAIN_ID와 /map 발행 확인. 일치시켜 노드 재실행 |
| 목표 도달 전 성공으로 표시됨 | AMCL 위치와 Nav2 Goal Tolerance 확인 |
| TF/timestamp 경고 | use_sim_time과 /clock 확인. Gazebo 재시작 시 Nav2와 RViz도 순서대로 재시작 |
| gz_frame_id 경고 | 기존 기록에서는 경고와 별개로 SLAM/주행이 가능했음. 센서 토픽도 확인 |

기존 기록의 costmap은 inflation_radius=0.15m, resolution=0.05m, footprint=0.12×0.12m이며 goal tolerance는 거리 0.25m, 방향 0.25rad입니다. 최종 적용값은 실행 중 노드에서 확인하세요.

~~~bash
ros2 topic list
ros2 topic echo /scan --once
ros2 topic info /cmd_vel -v
ros2 topic info /map -v
ros2 param get /local_costmap/local_costmap inflation_layer.inflation_radius
ros2 service call /global_costmap/clear_entirely_global_costmap nav2_msgs/srv/ClearEntireCostmap '{}'
ros2 service call /local_costmap/clear_entirely_local_costmap nav2_msgs/srv/ClearEntireCostmap '{}'
~~~

SLAM과 Nav2 localization을 동시에 실행하지 마세요. ros2 daemon 재시작은 그래프 발견 관련 조치이며 TF 캐시를 직접 초기화하지 않습니다. Classic Small House는 모델 경로·관성 문제로 정상 동작을 확인하지 못했으므로 기본 실습에서 제외했습니다.

## 출처와 라이선스

- Pinky Pro: https://github.com/pinklab-art/pinky_pro — src/pinky_pro/LICENSE 참조
- Multi Room: https://github.com/makerspet/oomwoo_gazebo — oomwoo_gazebo/LICENSE 참조
- World Collection: https://github.com/mertgulerx/world-collection — world-collection/LICENSE 및 CITATION.cff 참조

각 외부 소스와 모델은 해당 라이선스를 따릅니다. 이 묶음에 단일 라이선스를 새로 부여하지 않았습니다. 원본의 라이선스·출처 파일을 유지했습니다. 기존 상세가이드의 clone/Launch 교체 절은 과거 설치 기록이고, 이 저장소를 사용하는 절차는 본 README가 기준입니다.

이 README는 포함된 로컬 파일과 기존 실행 기록을 대조해 작성했습니다. 배포용 사본을 새 환경에서 빌드하고 Gazebo로 재실행하는 검증은 아직 수행하지 않았습니다.
