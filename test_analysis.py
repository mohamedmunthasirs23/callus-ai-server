# analysis/test_analysis.py
import unittest
import numpy as np
from unittest.mock import MagicMock
from movement_analyzer import calculate_angle, check_t_pose, analyze_video_movement

# Create a mock object that mimics a MediaPipe Landmark object
class MockLandmark:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Create a mock list of 33 landmarks
def create_mock_landmarks(pose_type='T-Pose'):
    landmarks = [MockLandmark(0, 0, 0)] * 33 # Initialize 33 landmarks

    if pose_type == 'T-Pose':
        # T-Pose: Arms horizontal and straight (Elbow angle 180, Y coords similar)
        
        # Left Arm (Horizontal)
        landmarks[11] = MockLandmark(0.4, 0.4, 0) # L_SHOULDER
        landmarks[13] = MockLandmark(0.3, 0.4, 0) # L_ELBOW (Straight arm - same Y)
        landmarks[15] = MockLandmark(0.2, 0.4, 0) # L_WRIST
        
        # Right Arm (Horizontal)
        landmarks[12] = MockLandmark(0.6, 0.4, 0) # R_SHOULDER
        landmarks[14] = MockLandmark(0.7, 0.4, 0) # R_ELBOW
        landmarks[16] = MockLandmark(0.8, 0.4, 0) # R_WRIST
        
    elif pose_type == 'Non-T-Pose':
        # Non-T-Pose: Arms bent and/or vertical
        
        # Left Arm (Bent)
        landmarks[11] = MockLandmark(0.4, 0.4, 0) # L_SHOULDER
        landmarks[13] = MockLandmark(0.3, 0.3, 0) # L_ELBOW (Bent arm - different Y)
        landmarks[15] = MockLandmark(0.2, 0.4, 0) # L_WRIST
        
    return landmarks

class TestMovementAnalysis(unittest.TestCase):

    def test_calculate_angle_straight(self):
        """Test angle calculation for a straight line (180 degrees)."""
        angle = calculate_angle((10, 0), (0, 0), (-10, 0))
        self.assertAlmostEqual(angle, 180.0, delta=0.1)

    def test_calculate_angle_right(self):
        """Test angle calculation for a right angle (90 degrees)."""
        angle = calculate_angle((0, 10), (0, 0), (10, 0))
        self.assertAlmostEqual(angle, 90.0, delta=0.1)

    def test_check_t_pose_correct(self):
        """Test detection with mocked T-Pose data."""
        landmarks = create_mock_landmarks('T-Pose')
        self.assertTrue(check_t_pose(landmarks), "Should detect a perfect T-Pose")

    def test_check_t_pose_incorrect(self):
        """Test detection with mocked Non-T-Pose (bent arm) data."""
        landmarks = create_mock_landmarks('Non-T-Pose')
        self.assertFalse(check_t_pose(landmarks), "Should NOT detect a T-Pose with bent arms")

    # NOTE: To test the full 'analyze_video_movement', you would need 
    # a mocked video capture or a simple utility video file.

if __name__ == '__main__':
    unittest.main()
