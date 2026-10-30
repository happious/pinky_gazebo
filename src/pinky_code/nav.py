
import math
import rclpy

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped


# ==============================
# 목표 좌표 설정
# ==============================

GOAL_X = 0.66
GOAL_Y = 0.25
GOAL_YAW = 90.0  # degree


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

    # 현재 좌표 저장
    current_pose = {'x': None, 'y': None}

    def pose_callback(msg):
        current_pose['x'] = msg.pose.pose.position.x
        current_pose['y'] = msg.pose.pose.position.y

    sub_node = rclpy.create_node('nav_pose_monitor')

    sub_node.create_subscription(
        PoseWithCovarianceStamped,
        '/amcl_pose',
        pose_callback,
        10
    )

    try:
        # Nav2 활성화 확인
        nav.waitUntilNav2Active()

        # 목표 전송
        goal = create_goal(nav, GOAL_X, GOAL_Y, GOAL_YAW)
        nav.goToPose(goal)

        print(f"목표 좌표: ({GOAL_X}, {GOAL_Y}, {GOAL_YAW}°)")
        print("주행 시작")

        # ==============================
        # 주행 피드백
        # ==============================

        while not nav.isTaskComplete():
            rclpy.spin_once(sub_node, timeout_sec=0.5)

            feedback = nav.getFeedback()

            if feedback is not None:
                distance = feedback.distance_remaining
                elapsed = (
                    feedback.navigation_time.sec
                    + feedback.navigation_time.nanosec / 1e9
                )

                print("\n--- 주행 피드백 ---")
                print(f"남은 거리: {distance:.2f} m")
                print(f"경과 시간: {elapsed:.1f} 초")

                if current_pose['x'] is not None:
                    print(
                        f"현재 위치: "
                        f"({current_pose['x']:.3f}, "
                        f"{current_pose['y']:.3f})"
                    )

        # ==============================
        # 주행 결과
        # ==============================

        result = nav.getResult()

        print("\n--- 주행 결과 ---")

        if result == TaskResult.SUCCEEDED:
            print("Goal succeeded!")

        elif result == TaskResult.CANCELED:
            print("Goal was canceled!")

        elif result == TaskResult.FAILED:
            print("Goal failed!")

        else:
            print("Invalid return status!")

    except KeyboardInterrupt:
        print("\n사용자 중단")
        nav.cancelTask()

    finally:
        sub_node.destroy_node()
        nav.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
