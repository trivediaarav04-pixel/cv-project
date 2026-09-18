# Lane Detection System

A modular Computer Vision pipeline designed to detect road lane markings in images and video streams using OpenCV and NumPy. The system applies edge detection, region-of-interest masking, and Hough Line Transforms to compute and overlay linear lane boundaries.

---

## Repository Structure

```text
computer vision/
├── data/              # Input sample images and videos
├── output/            # Directory for processed output files
├── pipeline.py        # Core Computer Vision processing logic
├── main.py            # Command-Line Interface (CLI) application
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation