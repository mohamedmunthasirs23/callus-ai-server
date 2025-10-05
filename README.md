# callus-ai-server
**Callus Company Inc. Competency Assessment:** AI ML Server Engineer

**Project Title:** Containerized Dance Movement Analysis Server

This project deploys a basic, high-performance AI/ML server designed to analyze uploaded video files, specifically detecting and summarizing standard body poses (T-Pose) using computer vision. The system is built on a modern, containerized architecture ready for scalable cloud deployment.

**🌐 Live Public Endpoint URL**
The fully deployed server can be tested at the following public IP address: http://34.100.239.217/docs

The interactive documentation is available at: http://34.100.239.217/docs

**1. Alignment with Callus's Vision**

This project establishes the foundational ML service required for future AI-powered fitness, dance, or physical therapy products.

Project Component	Future Vision Impact
Accurate Pose Detection	Enables objective, automated feedback systems (e.g., "You held the T-Pose correctly for 4.75 seconds").

Video Processing Pipeline	Provides the core API endpoint necessary for a consumer application to upload data and receive instant, personalized results.

Containerization (Docker)	Ensures the service is portable and scalable, allowing Callus to deploy quickly across multiple cloud environments (AWS, GCP, etc.) or scale horizontally under heavy load.

**2. Technical Architecture and Tooling**

Component	Technology Used	Justification and Evaluation Criteria Core Analysis	MediaPipe Pose & OpenCV/Numpy	Selected for superior accuracy in keypoint detection and high performance, crucial for real-time applications. Numpy was essential for precise geometric angle calculations.

API Framework	FastAPI	Chosen for high performance (asynchronous nature) and automatic generation of Swagger UI documentation (which significantly aids API usage clarity).

Containerization	Docker (using python:3.11-slim-bullseye)	Ensures environment consistency and reproducibility from local development to cloud deployment. Using the bullseye base image resolved dependency path errors inherent in the older Debian versions.

Deployment	GCP Compute Engine	Demonstrated successful deployment and configuration of network security (Port 80) in a major cloud environment.

**3. Thought Process and Debugging Insight**

The core technical challenge was ensuring reliable pose detection and resolving persistent environment issues during containerization.

*A. T-Pose Detection Logic*

Approach: The T-Pose was defined not by pixel coordinates but by joint angles and vertical alignment. We calculated the angle formed by the shoulder, elbow, and wrist joints.

Tuning Tolerances: Initial unit tests passed, but real-world video analysis failed due to camera perspective and natural body movement. The solution required tuning the angle and Y-coordinate tolerances to be slightly more permissive (e.g., allowing a ∼30 deviation from a perfect 180 straight arm and a larger vertical displacement tolerance on the Y-axis) before successful detection was achieved.

**B. DevOps and Environment Resolution**

ModuleNotFoundError: The persistent module import and path issues during local Uvicorn startup were solved by initially flattening the file structure to resolve conflicts, then restoring the package structure for the final Docker image.

Missing Dependencies: Resolved a RuntimeError by explicitly adding python-multipart to requirements.txt, which is necessary for FastAPI to parse video file uploads.

Virtualization/Docker: Overcame the docker command not found and Virtualization support not detected errors by manually updating WSL 2 and ensuring VT-x/SVM was correctly enabled in the BIOS/UEFI.

**4. Setup and API Usage**
   
Prerequisites Docker Engine (running and stable).

Python 3.10+ and an activated Virtual Environment.

Local Run Instructions
Clone the Repository and navigate to the root directory.

Build the Image:
docker build -t callus-dance-server:latest .

Run the Container: (Maps container port 80 to host port 8000)

docker run -d -p 8000:80 --name callus_local_test callus-dance-server:latest

Test the API: Access http://127.0.0.1:8000/docs in your browser.

**API Endpoint Usage**
The application provides two endpoints:

Endpoint	Method	        Function	               Input                    	             Output
/health	  GET	    Confirms server is running	      None	                          {"status": "ok", ...}
/analyze	POST	  Processes the video file    T-pose dance-video.MP4	 JSON summary with poses_detected  ["T-Pose"] and frame details.
