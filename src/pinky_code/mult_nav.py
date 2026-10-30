
import math
import rclpy

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped


# ==============================
# Waypoint 설정 (x, y, yaw)
# ==============================

WAYPOINTS = [
    (-0.8, 2.7, 0), # 첫번째 way point (x,y,yaw)
    (1.9,-0.34, 180), # 두번째 way point
    (-1.22, -2.46, 45) # 세번째 way point
]


def create_goal(nav, x, y, yaw):
    goal = PoseStamped()
    goal.header.frame_id = 'map'
    goal.header.stamp = nav.get_clock().now().to_msg()

    goal.pose.position.x = float(x)
    goal.pose.position.y = float(y)
    goal.pose.position.z = 0.0

    yaw_rad = math.radians(yaw)

    goal.pose.orientation.z = math.sin(yaw_rad / 2.0)
    goal.pose.orientation.w = math.cos(yaw_rad / 2.0)

    return goal


def main():
    rclpy.init()

    nav = BasicNavigator()

    try:
        # Nav2 활성화 확인
        nav.waitUntilNav2Active()

        # ==============================
        # Waypoint 리스트 생성
        # ==============================

        goal_pose_list = []

        for x, y, yaw in WAYPOINTS:
            goal = create_goal(nav, x, y, yaw)
            goal_pose_list.append(goal)

        print(f"총 Waypoint: {len(goal_pose_list)}개")

        for i, (x, y, yaw) in enumerate(WAYPOINTS):
            print(f"{i+1}번: x={x}, y={y}, yaw={yaw}°")

        # ==============================
        # Waypoint 주행 시작
        # ==============================

        nav.followWaypoints(goal_pose_list)

        print("\nWaypoint 주행 시작")

        # ==============================
        # 주행 피드백
        # ==============================

        last_waypoint = -1

        while not nav.isTaskComplete():
            feedback = nav.getFeedback()

            if feedback is not None:
                current = feedback.current_waypoint

                if current != last_waypoint:
                    print("\n--- Waypoint 피드백 ---")
                    print(
                        f"현재 Waypoint: "
                        f"{current + 1}/{len(WAYPOINTS)}"
                    )

                    if 0 <= current < len(WAYPOINTS):
                        x, y, yaw = WAYPOINTS[current]
                        print(
                            f"목표 좌표: "
                            f"x={x}, y={y}, yaw={yaw}°"
                        )

                    last_waypoint = current

        # ==============================
        # 주행 결과
        # ==============================

        result = nav.getResult()

        print("\n--- 주행 결과 ---")

        if result == TaskResult.SUCCEEDED:
            print("All Waypoints succeeded!")

        elif result == TaskResult.CANCELED:
            print("Waypoint navigation canceled!")

        elif result == TaskResult.FAILED:
            print("Waypoint navigation failed!")

        else:
            print("Invalid return status!")

    except KeyboardInterrupt:
        print("\n사용자 중단")
        nav.cancelTask()

    finally:
        nav.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
