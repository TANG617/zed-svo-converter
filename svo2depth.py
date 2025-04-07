import sys
import pyzed.sl as sl
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import glob

def process_svo_file(svo_file, frame_interval, output_dir):
    init_params = sl.InitParameters()
    init_params.set_from_svo_file(svo_file)
    init_params.coordinate_units = sl.UNIT.METER
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL_PLUS

    zed = sl.Camera()
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(f"Failed to open SVO: {status}")
        return

    runtime_parameters = sl.RuntimeParameters()
    depth_map = sl.Mat()
    image = sl.Mat()

    frame_count = 0
    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            frame_count += 1
            if(frame_count % frame_interval != 0):
                continue

            zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH)
            zed.retrieve_image(image, sl.VIEW.RIGHT)

            depth_array = depth_map.get_data()
            image_array = image.get_data()

            min_depth = 0.3
            max_depth = 13.0
            
            depth_array[depth_array == 0] = min_depth
            depth_array[depth_array == np.inf] = min_depth
            depth_array[depth_array == -np.inf] = min_depth
            
            depth_array = np.clip(depth_array, min_depth, max_depth)
            
            depth_array = max_depth - depth_array
            
            depth_normalized = 255 - ( (depth_array - min_depth) * 255 / 
                              (max_depth - min_depth)).astype(np.uint8)

            depth_file = os.path.join(output_dir + "/depth", f"depth_{frame_count:04d}.png")
            plt.imsave(depth_file, depth_normalized, cmap='gray')
            print(f"Saved depth image: {depth_file}")

            rgb_file = os.path.join(output_dir + "/rgb", f"rgb_{frame_count:04d}.png")
            plt.imsave(rgb_file, image_array)
            print(f"Saved RGB image: {rgb_file}")

        else:
            print("End of SVO or error.")
            break

    zed.close()

def main():
    parser = argparse.ArgumentParser(description='Convert SVO file to depth images')
    parser.add_argument('--svo_file', help='Path to the SVO file')
    parser.add_argument('--svo_dir', help='Directory containing SVO files', default="./")
    parser.add_argument('--frame-interval', type=int, default=600,
                        help='Interval between frames to save (default: 600)')
    parser.add_argument('--output-dir', help='Output directory for images (default: SVO filename without extension)')
    args = parser.parse_args()

    if args.svo_file is None and args.svo_dir is None:
        print("Error: Either --svo_file or --svo_dir must be specified")
        return

    if args.svo_file:
        svo_files = [args.svo_file]
    else:
        svo_files = glob.glob(os.path.join(args.svo_dir, "*.svo"))

    for svo_file in svo_files:
        print(f"\nProcessing {svo_file}...")
        
        if args.output_dir is None:
            output_dir = os.path.splitext(os.path.basename(svo_file))[0] + str("_interval" + str(args.frame_interval))
        else:
            output_dir = os.path.join(args.output_dir, os.path.splitext(os.path.basename(svo_file))[0] + str("_interval" + str(args.frame_interval)))
        
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(output_dir + "/depth", exist_ok=True)
        os.makedirs(output_dir + "/rgb", exist_ok=True)
        
        process_svo_file(svo_file, args.frame_interval, output_dir)

if __name__ == "__main__":
    main() 