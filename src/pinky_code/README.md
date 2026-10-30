# Pinky Python 예제

Nav2 실행 및 RViz의 2D Pose Estimate 설정 후 사용합니다. 모든 터미널에서 워크스페이스를 source하고 같은 ROS_DOMAIN_ID를 사용하세요.

| 파일 | 설명 |
|---|---|
| [nav.py](nav.py) | 단일 목표점 주행. GOAL_X=0.66, GOAL_Y=0.25, GOAL_YAW=90.0 예제. goToPose 사용 |
| [mult_nav.py](mult_nav.py) | WAYPOINTS 목록의 여러 좌표를 followWaypoints로 순차 주행 |
| [current_pose.py](current_pose.py) | /amcl_pose 구독 후 현재 x/y와 yaw 출력 |
| [pinky_lcd](pinky_lcd) | 실물 LCD 이미지·GIF·카메라·텍스트 예제. Gazebo 주행과 별개 |

x/y는 map 기준 미터, yaw는 도 단위입니다. 자신의 지도에 맞춰 목표를 수정하세요. 초기 위치는 코드에서 설정하지 않으므로 RViz에서 먼저 지정합니다.

~~~bash
source ~/pinky_ws/install/setup.bash
export ROS_DOMAIN_ID=0
# 아래 중 하나씩 실행
python3 ~/pinky_ws/src/pinky_code/nav.py --ros-args -p use_sim_time:=true
python3 ~/pinky_ws/src/pinky_code/mult_nav.py --ros-args -p use_sim_time:=true
python3 ~/pinky_ws/src/pinky_code/current_pose.py --ros-args -p use_sim_time:=true
~~~

전체 설치와 실행 순서는 [최상위 README](../../README.md)를 참고하세요.
