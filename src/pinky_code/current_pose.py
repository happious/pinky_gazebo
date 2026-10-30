
import math
import rclpy

from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped


class CurrentPose(Node):
    def __init__(self):
        super().__init__('current_pose')

        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg):
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation

        # Quaternion -> Yaw (degree)
        yaw = math.atan2(
            2.0 * (ori.w * ori.z + ori.x * ori.y),
            1.0 - 2.0 * (ori.y**2 + ori.z**2)
        )
        yaw_deg = math.degrees(yaw)

        print(
            f"현재 위치 | "
            f"x: {pos.x:.3f}, "
            f"y: {pos.y:.3f}, "
            f"yaw: {yaw_deg:.1f}°"
        )


def main():
    rclpy.init()
    node = CurrentPose()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
