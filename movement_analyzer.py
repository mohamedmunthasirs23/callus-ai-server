# movement_analyzer.py
import cv2
import mediapipe as mp
import numpy as np
import json

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """Calculates the angle (in degrees) between three 3D points (a, b, c)"""
    a = np.array(a)  # First point (e.g., shoulder)
    b = np.array(b)  # Mid point (e.g., elbow)
    c = np.array(c)  # End point (e.g., wrist)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle if angle < 180.0 else 360.0 - angle

def check_t_pose(landmarks):
    """Checks if the body is in a T-Pose using landmark coordinates."""
    # Simplified T-Pose criteria: Arms straight and horizontal

    # Keypoint indices (MediaPipe Pose)
    L_SHOULDER = mp_pose.PoseLandmark.LEFT_SHOULDER.value
    L_ELBOW = mp_pose.PoseLandmark.LEFT_ELBOW.value
    L_WRIST = mp_pose.PoseLandmark.LEFT_WRIST.value
    R_SHOULDER = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
    R_ELBOW = mp_pose.PoseLandmark.RIGHT_ELBOW.value
    R_WRIST = mp_pose.PoseLandmark.RIGHT_WRIST.value

    # Get coordinates (normalized to 0-1000 for easier calculation, ignoring Z)
    def get_coords(idx):
        lm = landmarks[idx]
        return (lm.x * 1000, lm.y * 1000, lm.z * 1000)

    # 1. Check Elbow Angles (Should be close to 180 degrees for straight arms)
    left_arm_angle = calculate_angle(get_coords(L_SHOULDER), get_coords(L_ELBOW), get_coords(L_WRIST))
    right_arm_angle = calculate_angle(get_coords(R_SHOULDER), get_coords(R_ELBOW), get_coords(R_WRIST))

    # 2. Check Shoulder-Elbow-Wrist vertical alignment (Should be close to 90 degrees 
    # if arms were straight up, but for T-pose, horizontal distance is key)
    
    # Simpler check: Vertical alignment of shoulder and elbow should be minimal
    L_shoulder_y = landmarks[L_SHOULDER].y
    L_elbow_y = landmarks[L_ELBOW].y
    L_wrist_y = landmarks[L_WRIST].y
    
    R_shoulder_y = landmarks[R_SHOULDER].y
    R_elbow_y = landmarks[R_ELBOW].y
    R_wrist_y = landmarks[R_WRIST].y

    # Tolerance for straight arm (180 degrees)
    elbow_tolerance = 40 # 180 +/- 20 degrees
    is_left_arm_straight = 180 - elbow_tolerance <= left_arm_angle <= 180 + elbow_tolerance
    is_right_arm_straight = 180 - elbow_tolerance <= right_arm_angle <= 180 + elbow_tolerance

    # Tolerance for horizontal arm (minimal vertical displacement)
    y_diff_threshold = 0.15 # 5% difference in Y-coordinate
    is_left_arm_horizontal = abs(L_shoulder_y - L_elbow_y) < y_diff_threshold and abs(L_elbow_y - L_wrist_y) < y_diff_threshold
    is_right_arm_horizontal = abs(R_shoulder_y - R_elbow_y) < y_diff_threshold and abs(R_elbow_y - R_wrist_y) < y_diff_threshold

    return (is_left_arm_straight and is_right_arm_straight and 
            is_left_arm_horizontal and is_right_arm_horizontal)

def analyze_video_movement(video_path: str) -> dict:
    """Analyzes a video for standard dance poses and generates a summary."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Could not open video file."}

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    pose_results = {"T-Pose": {"count": 0, "duration_frames": 0, "detected_frames": []}}
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_number = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
            
            # Convert the BGR image to RGB and process it with MediaPipe Pose.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                # Pose Detection Check
                is_t_pose = check_t_pose(landmarks)
                
                if is_t_pose:
                    pose_results["T-Pose"]["count"] += 1
                    pose_results["T-Pose"]["duration_frames"] += 1
                    pose_results["T-Pose"]["detected_frames"].append(frame_number)

            frame_number += 1
    
    cap.release()
    
    # Final Summary Generation
    summary = {
        "video_path": video_path.split('/')[-1],
        "total_frames": frame_count,
        "fps": fps,
        "poses_detected": [],
        "pose_details": {}
    }
    
    for pose_name, details in pose_results.items():
        if details["count"] > 0:
            summary["poses_detected"].append(pose_name)
            summary["pose_details"][pose_name] = {
                "total_seconds": details["duration_frames"] / fps,
                "duration_frames": details["duration_frames"],
                "frames": details["detected_frames"] # Include frame numbers for detailed view
            }

    return summary

if __name__ == '__main__':
    # Example usage for testing
    # Replace 'sample_video.mp4' with a video in your directory
    # analysis_summary = analyze_video_movement('sample_video.mp4') 
    # print(json.dumps(analysis_summary, indent=4))
    pass
