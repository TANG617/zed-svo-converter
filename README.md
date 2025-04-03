# SVO to PLY and Depth Image Converter

这个工具集包含两个Python脚本，用于将ZED相机的SVO录制文件转换为PLY点云文件，并进一步将PLY文件转换为深度图和RGB图像。

## 环境要求

### 1. ZED SDK 安装

1. 下载 ZED SDK 5.0：
   - [Windows 版本](https://download.stereolabs.com/zedsdk/5.0/win)
   - [Ubuntu 版本](https://download.stereolabs.com/zedsdk/5.0/ubuntu22)
   - [其他版本](https://www.stereolabs.com/developers/release/)

2. 安装步骤：
   - Windows: 运行下载的安装程序，按照向导完成安装
   - Ubuntu: 
     ```bash
     chmod +x ZED_SDK_Ubuntu22_v5.0.0.run
     ./ZED_SDK_Ubuntu22_v5.0.0.run
     ```

3. 安装 Python API：
   ```bash
   pip install pyzed-sdk
   ```

### 2. CUDA 环境（可选）

如果要使用 NEURAL_PLUS 深度模式，需要：
1. 安装 CUDA 11.8 或更高版本
2. 安装 cuDNN 8.6 或更高版本
3. 下载并安装 ZED 深度模型：
   ```bash
   # 在 ZED SDK 安装目录下运行
   ./tools/ZED_Depth_Viewer
   # 在设置中选择下载深度模型
   ```

## 依赖安装

```bash
pip install numpy matplotlib pyzed-sdk
```

## 使用说明

### 1. SVO转PLY (svo2ply.py)

将SVO文件转换为PLY点云文件。

```bash
python svo2ply.py [选项]
```

参数说明：
- `--svo_file`：指定单个SVO文件的路径
- `--svo_dir`：指定包含多个SVO文件的目录，默认为当前目录
- `--frame-interval`：指定保存帧的间隔，默认为600（即每600帧保存一次）
- `--output-dir`：指定输出目录，默认为SVO文件名（不含扩展名）+ "_ply_interval" + 帧间隔

示例：
```bash
# 处理单个SVO文件
python svo2ply.py --svo_file ./recording.svo --frame-interval 300

# 处理目录中的所有SVO文件
python svo2ply.py --svo_dir ./recordings --frame-interval 600

# 指定输出目录
python svo2ply.py --svo_dir ./recordings --output-dir ./output
```

### 2. SVO转深度图 (svo2depth.py)

直接将SVO文件转换为深度图和RGB图像。

```bash
python svo2depth.py [选项]
```

参数说明：
- `--svo_file`：指定单个SVO文件的路径
- `--svo_dir`：指定包含多个SVO文件的目录，默认为当前目录
- `--frame-interval`：指定保存帧的间隔，默认为600（即每600帧保存一次）
- `--output-dir`：指定输出目录，默认为SVO文件名（不含扩展名）+ "_interval" + 帧间隔

示例：
```bash
# 处理单个SVO文件
python svo2depth.py --svo_file ./recording.svo --frame-interval 300

# 处理目录中的所有SVO文件
python svo2depth.py --svo_dir ./recordings --frame-interval 600

# 指定输出目录
python svo2depth.py --svo_dir ./recordings --output-dir ./output
```

### 3. PLY转深度图 (ply2depth.py)

将PLY点云文件转换为深度图和RGB图像。

```bash
python ply2depth.py [选项]
```

参数说明：
- `--input-dir`：PLY文件所在目录，默认为当前目录
- `--width`：输出图像宽度，默认为640
- `--height`：输出图像高度，默认为360
- `--fx`：x方向焦距，默认为500
- `--fy`：y方向焦距，默认为500
- `--rx`：绕x轴旋转角度（度），默认为90
- `--ry`：绕y轴旋转角度（度），默认为0
- `--rz`：绕z轴旋转角度（度），默认为0

示例：
```bash
# 使用默认参数
python ply2depth.py --input-dir ./ply_files

# 自定义分辨率和FOV
python ply2depth.py --input-dir ./ply_files --width 1280 --height 720 --fx 500 --fy 500
```

## 输出文件

- `svo2ply.py` 将生成格式为 `pointcloud_XXXX.ply` 的PLY文件，保存在以SVO文件名命名的文件夹中
- `svo2depth.py` 将为每个SVO文件生成深度图（`depth_XXXX.png`）和RGB图像（`rgb_XXXX.png`），分别保存在depth和rgb子文件夹中
- `ply2depth.py` 将为每个PLY文件生成对应的深度图（`*_depth.png`）和RGB图像（`*_rgb.png`）

## 注意事项

- 确保系统已正确安装ZED SDK
- 深度模式选择：
  - 如果已安装CUDA和深度模型，默认使用NEURAL_PLUS模式
  - 否则会自动切换到ULTRA模式
- 调整FOV参数（fx/fy）时，建议根据实际相机参数设置
- 旋转角度参数（rx/ry/rz）可用于调整点云的视角
- 深度图处理时，深度值范围被限制在0.3米到10.0米之间
- 无效的深度值（0或无穷大）会被设置为最大深度值