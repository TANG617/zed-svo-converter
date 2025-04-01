import sys
import pyzed.sl as sl
import re
import argparse

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

def main():
    parser = argparse.ArgumentParser(description='Convert SVO file to PLY files')
    parser.add_argument('svo_file', help='Path to the SVO file')
    parser.add_argument('--frame-interval', type=int, default=60,
                        help='Interval between frames to save (default: 60)')
    args = parser.parse_args()

    init_params = sl.InitParameters()
    init_params.set_from_svo_file(args.svo_file)
    init_params.coordinate_units = sl.UNIT.METER
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA

    zed = sl.Camera()
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(f"Failed to open SVO: {status}")
        exit()

    runtime_parameters = sl.RuntimeParameters()
    point_cloud = sl.Mat()

    frame_count = 0
    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            frame_count += 1
            if(frame_count % args.frame_interval != 0):
                continue
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            
            filename = f"pointcloud_frame_{frame_count:04d}.ply"
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

if __name__ == "__main__":
    main()