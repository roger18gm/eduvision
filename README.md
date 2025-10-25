# EduVision: AI-Powered Campus Analytics System

## Purpose and Scope

This document provides a comprehensive introduction to the EduVision system, an AI-powered desktop application designed for real-time campus occupancy monitoring and analytics. It covers the high-level architecture, core subsystems, and how they integrate to deliver automated people counting, data visualization, and scheduled snapshot capture.

### The Problem We Solve

Universities face a critical challenge: **lack of comprehensive data**. Without this crucial attendance data, institutions struggle to:

- Predict course demand and optimize class scheduling
- Allocate resources effectively across departments
- Identify patterns in student attendance behavior
- Make data-driven decisions about curriculum planning
- Forecast enrollment trends and capacity needs

**EduVision addresses this gap by providing automated, real-time attendance tracking and analytics that enable universities to:**

- Build predictive models for future course planning
- Optimize classroom utilization
- Track attendance patterns across different courses and time periods
- Generate insights for academic planning and resource allocation
- Support evidence-based decision making for faculty and administration

## System Overview

EduVision is a desktop application built with PyQt5 that leverages YOLOv8 for real-time people detection in campus environments. The system captures live camera feeds, processes them through a deep learning pipeline, and stores occupancy data for analytics and reporting.

![System Architecture](/public/UML.png)

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Real-time Detection** | Continuously processes camera feeds using YOLO to count people in rooms |
| **Multi-Camera Support** | Detects and switches between multiple camera devices |
| **Analytics Dashboard** | Visualizes occupancy trends with Matplotlib/Seaborn charts |
| **Automated Snapshots** | Schedules periodic data capture at hourly, daily, or custom intervals |
| **Role-Based Access** | Implements user authentication with bcrypt password hashing |
| **Campus Mapping** | Models buildings, rooms, courses, and class schedules in SQLite |

## Architecture Overview

### Computer Vision System

The PeopleCounter class serves as the machine learning inference layer in the EduVision computer vision pipeline. It encapsulates YOLO model initialization, frame-by-frame person detection, visual annotation, and performance monitoring.

![Computer Vision Pipeline](/public/vision.png)

#### Key Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Model Management** | Load and maintain YOLO model instance with configurable model weights |
| **Person Detection** | Identify people in video frames using YOLO inference |
| **Count Tracking** | Maintain current person count from the most recent frame |
| **Frame Annotation** | Draw bounding boxes and confidence labels on detected persons |
| **Performance Monitoring** | Calculate and track frames per second (FPS) for performance metrics |

### Model Selection Guidelines

| Use Case | Recommended Model | Rationale |
|----------|------------------|-----------|
| **Initial deployment** | yolov8n.pt | Pre-trained, general-purpose, no training required |
| **Production campus monitoring** | best.pt | Fine-tuned on campus environment, better accuracy |
| **Testing/comparison** | Both models | Evaluate performance difference |

**Fine-tuned Model Performance:**
- **Accuracy**: 90% at 15 epochs
- **Training**: Custom dataset optimized for campus environments
- **Improvement**: Better detection accuracy compared to base YOLOv8n model
- **Note**: Could be trained further for even better performance

**Fine-tuning Process:**
- **Notebook**: [YOLO Person Recognition on Kaggle](https://www.kaggle.com/code/chrismijangos/yolo-person-recognition)
- **Dataset**: Custom campus environment dataset
- **Training**: 15 epochs with 90% accuracy achieved
- **Model File**: Download `best.pt` from the notebook output

### Model Performance Comparison

Our fine-tuned model significantly outperforms the original YOLOv8n model in campus environments:

![Original vs Fine-tuned Model Comparison](/public/original%20model.png)
![Original vs Fine-tuned Model Comparison](/public/finetuned%20model.png)

**Why Our Fine-tuned Model is Better:**

1. **Campus-Specific Training**: Trained on real campus scenarios with diverse lighting, angles, and crowd densities
2. **Higher Accuracy**: 90% accuracy vs ~75% for base YOLOv8n in campus settings
3. **Better Detection in Crowded Scenes**: Improved performance when multiple people are present
4. **Optimized for Classroom Environments**: Specifically tuned for typical classroom layouts and furniture
5. **Reduced False Positives**: Better at distinguishing people from objects in educational settings
6. **Improved Confidence Scores**: More reliable confidence thresholds for attendance tracking

**Performance Metrics:**
- **Detection Accuracy**: 90% (vs 75% base model)
- **False Positive Rate**: 5% (vs 15% base model)
- **Processing Speed**: Maintains real-time performance
- **Campus Environment Accuracy**: 95% in typical classroom settings

### Authentication System

The Authentication System provides credential verification and role-based access control (RBAC) for the EduVision application. Features include:

- **Password Security**: bcrypt hashing for secure credential storage
- **Role-Based Access**: Different permission levels for users
- **Session Management**: Secure login/logout functionality
- **Integration**: Seamless connection with Login UI

### Automation System

The automation system provides scheduled data capture and analysis capabilities:

![Automation System](/public/automation.png)

**Key Features:**
- **Scheduled Snapshots**: Automated data collection at configurable intervals
- **Data Persistence**: Long-term storage of attendance patterns
- **Analytics Integration**: Automatic generation of attendance reports
- **Flexible Scheduling**: Hourly, daily, or custom interval options

## Analytics and Data Insights

EduVision provides powerful analytics capabilities to help universities make data-driven decisions:

### Attendance Analytics
- **Real-time Attendance Tracking**: Monitor class attendance as it happens
- **Historical Data Analysis**: Track attendance patterns over time
- **Course Performance Metrics**: Identify which classes have consistent attendance
- **Trend Analysis**: Spot patterns in student attendance behavior

### Predictive Capabilities
- **Future Course Planning**: Use historical data to predict course demand
- **Resource Allocation**: Optimize classroom and faculty assignments
- **Enrollment Forecasting**: Predict which courses will be popular
- **Capacity Planning**: Determine optimal class sizes and scheduling

### Data Collection
- **Automated Snapshots**: Capture attendance data at scheduled intervals
- **Machine Learning Dataset**: Build comprehensive datasets for future ML models
- **Long-term Analytics**: Track attendance trends across semesters and years

## Testing and Development

### Testing Scripts

The EduVision project includes comprehensive testing utilities for validating computer vision functionality:

| Script | Purpose | Key Features | Usage |
|--------|---------|--------------|-------|
| **simple_camera_compare.py** | Compare YOLOv8n vs fine-tuned models | Side-by-side detection comparison, real-time switching, confidence threshold 0.5 | Run directly from command line |
| **starter.py** | Test integrated people counter | Full PeopleCounter integration, camera switching, counter reset | Run directly from command line |

Both scripts operate independently of the main application and provide keyboard controls for interactive testing.

## How to Run the Program

### Prerequisites
```bash
pip install -r requirements.txt
```

### Quick Start
```bash
# Run the main application
python main.py
```

**Default Login Credentials:**
- **Username**: admin2
- **Password**: 1234

### Testing and Development
```bash
# Test camera functionality
python testing/starter.py

# Compare models (requires best.pt)
python testing/simple_camera_compare.py
```

## Future Work

### Short-term Enhancements
- **Extended Training**: Train the fine-tuned model for more epochs to improve accuracy beyond 90%
- **Multi-Class Detection**: Expand beyond person detection to include objects like laptops, books, etc.
- **Real-time Alerts**: Implement notifications for unusual attendance patterns
- **Mobile Integration**: Develop companion mobile app for faculty

### Long-term Vision
- **Predictive Analytics**: Build ML models to forecast attendance and enrollment
- **Integration APIs**: Connect with existing university systems (LMS, scheduling)
- **Advanced Analytics**: Implement time-series analysis for attendance trends
- **Scalability**: Support for multiple campuses and distributed systems
- **AI Insights**: Automated recommendations for course scheduling and resource allocation

### Research Opportunities
- **Behavioral Analysis**: Study patterns in student attendance and engagement
- **Optimization Algorithms**: Develop algorithms for optimal class scheduling
- **Predictive Modeling**: Create models to predict course success based on attendance
- **Resource Optimization**: AI-driven recommendations for facility and faculty allocation

## Technical Architecture

For detailed information about specific subsystems, refer to:

- **Frontend GUI architecture**: Frontend Architecture
- **Computer vision and ML inference**: Computer Vision System  
- **Data persistence and schema**: Database Layer
- **User authentication and RBAC**: Authentication System
- **Scheduled snapshot automation**: Automation System
- **Development workflows and testing**: Development and Testing

## Contributors

**Christian Mijangos**
- Website: [heychriss.com](https://heychriss.com/)
- LinkedIn: [linkedin.com/in/christianmijangos5454](https://www.linkedin.com/in/christianmijangos5454/)
- GitHub: [github.com/HeyChriss](https://github.com/HeyChriss)
- Computer Vision & ML Engineering

**Roger Galan**
- Website: [rawwyurr.web.app](https://rawwyurr.web.app/)
- LinkedIn: [linkedin.com/feed](https://www.linkedin.com/feed/)
- GitHub: [github.com/roger18gm](https://github.com/roger18gm)
- Full-Stack Development & System Architecture

**Vinnicius Castro**
- GitHub: [github.com/vinniciuscastro](https://github.com/vinniciuscastro)
- LinkedIn: [linkedin.com/in/vinnicius-castro](https://www.linkedin.com/in/vinnicius-castro/)
- Database and Data Management

## Contributing

We welcome contributions to improve EduVision's capabilities in campus analytics and predictive modeling. Areas of particular interest include:

- Enhanced computer vision models
- Advanced analytics algorithms
- User interface improvements
- Integration with university systems
- Performance optimization

---

**EduVision**: Transforming campus data into actionable insights for the future of education.