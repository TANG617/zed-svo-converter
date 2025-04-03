import numpy as np
import matplotlib.pyplot as plt
import os
import math
import argparse

def rotate_points(points, rx=0, ry=0, rz=0):
    Rx = np.array([[1, 0, 0],
                   [0, math.cos(rx), -math.sin(rx)],
                   [0, math.sin(rx), math.cos(rx)]])
    
    Ry = np.array([[math.cos(ry), 0, math.sin(ry)],
                   [0, 1, 0],
                   [-math.sin(ry), 0, math.cos(ry)]])
    
    Rz = np.array([[math.cos(rz), -math.sin(rz), 0],
                   [math.sin(rz), math.cos(rz), 0],
                   [0, 0, 1]])
    
    R = Rz @ Ry @ Rx
    return points @ R.T

def read_ply(filename):
    points = []
    colors = []
    with open(filename, 'r') as f:
        line = f.readline()
        while not line.startswith('end_header'):
            line = f.readline()
        
        for line in f:
            x, y, z, r, g, b = map(float, line.split())
            points.append([x, y, z])
            colors.append([r, g, b])
    
    return np.array(points), np.array(colors)

def create_images(points, colors, width, height, fx, fy, rx=0, ry=0, rz=0):
    rotated_points = rotate_points(points, rx, ry, rz)
    
    depth_image = np.zeros((height, width), dtype=np.float32)
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    cx = width / 2
    cy = height / 2
    
    for i, point in enumerate(rotated_points):
        x, y, z = point
        if z > 0:
            u = int(fx * x / z + cx)
            v = int(fy * y / z + cy)
            
            if 0 <= u < width and 0 <= v < height:
                if depth_image[v, u] == 0 or z < depth_image[v, u]:
                    depth_image[v, u] = z
                    rgb_image[v, u] = colors[i]
    
    return depth_image, rgb_image

def main():
    parser = argparse.ArgumentParser(description='Convert PLY files to depth and RGB images')
    parser.add_argument('--input-dir', default='.',
                        help='Directory containing PLY files (default: current directory)')
    parser.add_argument('--width', type=int, default=640,
                        help='Output image width (default: 640)')
    parser.add_argument('--height', type=int, default=360,
                        help='Output image height (default: 360)')
    parser.add_argument('--fx', type=float, default=500,
                        help='Focal length in x direction (default: 500)')
    parser.add_argument('--fy', type=float, default=500,
                        help='Focal length in y direction (default: 500)')
    parser.add_argument('--rx', type=float, default=90,
                        help='Rotation angle around x-axis in degrees (default: 90)')
    parser.add_argument('--ry', type=float, default=0,
                        help='Rotation angle around y-axis in degrees (default: 0)')
    parser.add_argument('--rz', type=float, default=0,
                        help='Rotation angle around z-axis in degrees (default: 0)')
    args = parser.parse_args()

    ply_files = [f for f in os.listdir(args.input_dir) if f.endswith('.ply')]
    
    rx = math.radians(args.rx)
    ry = math.radians(args.ry)
    rz = math.radians(args.rz)
    
    for ply_file in ply_files:
        print(f"Processing {ply_file}...")
        
        points, colors = read_ply(ply_file)
        depth_image, rgb_image = create_images(points, colors, args.width, args.height, args.fx, args.fy, rx=rx, ry=ry, rz=rz)
        
        depth_normalized = ((depth_image - depth_image.min()) * 255 / 
                          (depth_image.max() - depth_image.min())).astype(np.uint8)
        
        depth_file = ply_file.replace('.ply', '_depth.png')
        plt.imsave(depth_file, depth_normalized, cmap='gray')
        print(f"Saved depth image: {depth_file}")
        
        rgb_file = ply_file.replace('.ply', '_rgb.png')
        plt.imsave(rgb_file, rgb_image)
        print(f"Saved RGB image: {rgb_file}")

if __name__ == "__main__":
    main()
