# 예제 맵

| 지도 | 용도 | 해상도 | 원점 (x, y, yaw) |
|---|---|---|---|
| multi_room.yaml + multi_room.pgm | Multi Room 실습 지도 | 0.05m/pixel | (-4.256, -3.969, 0) |
| pinky_map.yaml + pinky_map.pgm | Pinky 맵 예제 | 0.05m/pixel | (-1.046, -0.558, 0) |

YAML은 지도 설정, PGM은 점유격자 이미지입니다. YAML의 image는 같은 폴더의 PGM을 가리키므로 두 파일을 함께 이동하세요. 맵 원점은 로봇 스폰 위치나 AMCL 초기 위치가 아닙니다. 월드가 달라지거나 장애물을 수정했다면 새 지도를 만드는 것을 권장합니다.

~~~bash
ros2 launch pinky_navigation gz_bringup_launch.xml map:=$HOME/pinky_ws/maps/multi_room.yaml
~~~

RViz에서 2D Pose Estimate로 초기 위치를 지정합니다. SLAM 실행 중 새로운 이름으로 저장하면 제공 맵을 보존할 수 있습니다.

~~~bash
ros2 run nav2_map_server map_saver_cli -f ~/pinky_ws/maps/my_multi_room --ros-args -p use_sim_time:=true -p save_map_timeout:=10.0
~~~

저장이 실패하면 ROS_DOMAIN_ID 일치와 /map 발행 여부를 확인하세요. [전체 가이드](../README.md) 참고.
