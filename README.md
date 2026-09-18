# Lane Detection System

A Computer Vision pipeline that detects road lane markings in images and video
using OpenCV and NumPy. The system applies grayscale conversion, Gaussian
blurring, Canny edge detection, region-of-interest masking, and a probabilistic
Hough Line Transform to compute and overlay the left and right lane boundaries
on each frame.

---

## Overview

Given a road photo or a dashcam video, the pipeline finds the two lines that
mark the edges of the current lane and draws them back onto the frame in
green. It works frame-by-frame, so the same core logic (`pipeline.py`) handles
both a single image and every frame of a video.

---

## Features

- **Edge-based lane detection** — grayscale → Gaussian blur → Canny edge
  detection to extract candidate boundary pixels.
- **Region-of-interest masking** — restricts detection to the road area
  directly ahead of the camera, discarding sky, roadside clutter, and
  oncoming-traffic lanes.
- **Hough Line Transform + slope filtering** — `cv2.HoughLinesP` finds
  straight-line segments; near-horizontal segments are filtered out and the
  rest are split into a left group (negative slope) and a right group
  (positive slope).
- **Averaged lane boundaries** — each group's segments are averaged into a
  single left line and a single right line via `np.polyfit`, then overlaid on
  the original frame with `cv2.addWeighted`.
- **Image and video support** — one CLI (`main.py`) handles both. Images are
  processed in a single pass; videos are processed frame-by-frame with
  `cv2.VideoCapture` / `cv2.VideoWriter`.
- **Command-line interface** — run detection on any input file with a single
  command, no code changes required.

---

## Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3 | Implementation language |
| OpenCV (`opencv-python`) | Image/video I/O, Canny edge detection, Hough transform, drawing |
| NumPy | Line-fitting math (`polyfit`), array operations |
| `argparse` | Command-line argument parsing |

Dependencies are pinned in `requirements.txt`:

```text
opencv-python>=4.8.0
numpy>=1.24.0
```

---

## Repository Structure

```text
.
├── main.py            # Command-line interface (image/video dispatch)
├── pipeline.py         # Core lane detection logic (edges, ROI, Hough, overlay)
├── requirements.txt    # Project dependencies
├── readme.md           # Project documentation (this file)
├── sample1.jpg … sample6.jpg   # Sample road images for testing
├── samplevideo.mp4      # Sample dashcam video for testing
└── challenge.mp4        # Harder dashcam video (shadows/curves) for testing
```

> Note: output files are not stored in the repo — the CLI writes them
> wherever you point `--output`, and the folder is created automatically if
> it doesn't exist.

---

## Installation

**Prerequisites:** Python 3.8+ and `pip`.

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd <your-repository-folder>

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Steps to Install & Run

Run the CLI with an `--input` file and an `--output` path. The file type is
detected automatically from the extension.

**Process an image:**

```bash
python main.py --input sample1.jpg --output output/result.jpg
```

**Process a video:**

```bash
python main.py --input samplevideo.mp4 --output output/result.mp4
```

**Try the harder clip (shadows, curves, worn markings):**

```bash
python main.py --input challenge.mp4 --output output/challenge_result.mp4
```

Console output on success:

```text
Saved result to output/result.jpg
```
or, for video:
```text
Processing video...
Processing complete: output/result.mp4
```

---

## Instructions for Testing

The repository includes six sample images (`sample1.jpg` – `sample6.jpg`) and
two sample videos (`samplevideo.mp4`, `challenge.mp4`) specifically for
verifying the pipeline. To test:

1. Run the image command above on each `sampleN.jpg` and open the output to
   confirm the green lane overlay follows the road markings.
2. Run the video command on `samplevideo.mp4` (clear conditions) and
   `challenge.mp4` (shadows/curves) and inspect the output videos for
   consistent lane tracking.
3. Check the console for errors — a missing/corrupt input raises a
   `FileNotFoundError` with the offending path.

There is no automated test suite in this version; testing is done by visual
inspection of the annotated output against the input.

---

## Screenshots

Below is an example result on `sample1.jpg`: the two detected lane boundaries
are drawn in green over the original road photo.

*(See `output/result.jpg` after running the image command above for a live
example — a sample result is also included in the project submission.)*

---

## Author

Submitted for the **VITyarthi — Build Your Own Project** evaluation.
