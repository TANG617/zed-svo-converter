import numpy as np
import matplotlib.pyplot as plt
import os
import math

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

def create_images(points, colors, width=512, height=288, rx=0, ry=0, rz=0):
    rotated_points = rotate_points(points, rx, ry, rz)
    
    depth_image = np.zeros((height, width), dtype=np.float32)
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    fx = 200
    fy = 200
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
    ply_files = [f for f in os.listdir('.') if f.endswith('.ply')]
    
    rx = math.radians(90)
    ry = math.radians(0)
    rz = math.radians(0)
    
    for ply_file in ply_files:
        print(f"Processing {ply_file}...")
        
        points, colors = read_ply(ply_file)
        depth_image, rgb_image = create_images(points, colors, rx=rx, ry=ry, rz=rz)
        
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
