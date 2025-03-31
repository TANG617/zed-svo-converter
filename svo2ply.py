import sys
import pyzed.sl as sl
import re

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
    init_params = sl.InitParameters()
    init_params.set_from_svo_file("/home/timli/Downloads/svo2ply/HD720_SN37474702_10-34-07.svo")  
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
            if(frame_count % 60 != 0):
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