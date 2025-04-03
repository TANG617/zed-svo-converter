import sys
import pyzed.sl as sl
import re
import argparse
import os
import glob

def modify_ply_header(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith('element vertex'):
            vertex_count = int(line.split()[-1])
            lines[i] = f'element vertex {vertex_count - 1}\n'
            break
    
    with open(filename, 'w') as f:
        f.writelines(lines)

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
    point_cloud = sl.Mat()

    frame_count = 0
    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            frame_count += 1
            if(frame_count % frame_interval != 0):
                continue
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            
            filename = os.path.join(output_dir, f"pointcloud_{frame_count:04d}.ply")
            status = point_cloud.write(filename)
            if status:
                print(f"Saved: {filename}")
                modify_ply_header(filename)
                print(f"Modified vertex count in: {filename}")
            else:
                print(f"Failed to save point cloud for frame {frame_count}")
            
        else:
            print("End of SVO or error.")
            break

    zed.close()

def main():
    parser = argparse.ArgumentParser(description='Convert SVO file to PLY files')
    parser.add_argument('--svo_file', help='Path to the SVO file')
    parser.add_argument('--svo_dir', help='Directory containing SVO files', default="./")
    parser.add_argument('--frame-interval', type=int, default=600,
                        help='Interval between frames to save (default: 600)')
    parser.add_argument('--output-dir', help='Output directory for PLY files (default: SVO filename without extension)')
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
            output_dir = os.path.splitext(os.path.basename(svo_file))[0] + str("_ply_interval" + str(args.frame_interval))
        else:
            output_dir = os.path.join(args.output_dir, os.path.splitext(os.path.basename(svo_file))[0] + str("_ply_interval" + str(args.frame_interval)))
        
        os.makedirs(output_dir, exist_ok=True)
        process_svo_file(svo_file, args.frame_interval, output_dir)

if __name__ == "__main__":
    main()