# Mug & Book Object Detection System

![Demo Preview](static/preview.gif)

A Flask-based web application that detects mugs and books in images using YOLOv8 object detection, containerized with Docker.

## Features
- Upload images via web interface
- Real-time object detection
- Visual bounding box annotations
- Dockerized for easy deployment

## Setup Instructions

### Prerequisites
- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))

### Run Locally
```bash
# Clone repository
git clone https://github.com/your-username/mug-book-detector.git
cd mug-book-detector

# Build Docker image
docker build -t mugbook-detector .

# Run container
docker run -p 5000:5000 mugbook-detector
```

Access the application at: http://localhost:5000

## Usage Guide
1. Go to the application URL
2. Click "Choose File" to select an image
3. Click "Detect Objects"
4. View detected objects with bounding boxes

## Known Limitations
- Only processes JPG/PNG images
- Maximum image size: 5MB
- Detection accuracy may vary with:
  - Low-light images
  - Occluded objects
  - Unusual angles
- Not optimized for mobile devices

## Deployment
Deployed on Render: [Live Demo](https://your-render-link.onrender.com)

## Contributing
Pull requests welcome! For major changes, please open an issue first.

## License
[MIT](LICENSE)
