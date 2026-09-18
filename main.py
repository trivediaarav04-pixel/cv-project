import argparse
import os
import cv2
from pipeline import process_frame

def main():
    parser = argparse.ArgumentParser(description="Lane Detection CLI")
    parser.add_argument("--input", type=str, required=True, help="Input video/image path")
    parser.add_argument("--output", type=str, required=True, help="Output file path")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File not found: {args.input}")

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    ext = os.path.splitext(args.input)[1].lower()

    if ext in ['.jpg', '.jpeg', '.png']:
        img = cv2.imread(args.input)
        result = process_frame(img)
        cv2.imwrite(args.output, result)
        print(f"Saved result to {args.output}")

    elif ext in ['.mp4', '.avi', '.mov']:
        cap = cv2.VideoCapture(args.input)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        print("Processing video...")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(process_frame(frame))
        cap.release()
        out.release()
        print(f"Processing complete: {args.output}")

if __name__ == "__main__":
    main()