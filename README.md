# SVO to PLY and Depth Image Converter

这个工具集包含两个Python脚本，用于将ZED相机的SVO录制文件转换为PLY点云文件，并进一步将PLY文件转换为深度图和RGB图像。

## 依赖安装

```bash
pip install numpy matplotlib pyzed-sdk
```

## 使用说明

### 1. SVO转PLY (svo2ply.py)

将SVO文件转换为PLY点云文件。

```bash
python svo2ply.py <svo文件路径> [--frame-interval <帧间隔>]
```

参数说明：
- `svo文件路径`：必需参数，指定SVO文件的路径
- `--frame-interval`：可选参数，指定保存帧的间隔，默认为60（即每60帧保存一次）

示例：
```bash
python svo2ply.py ./recording.svo --frame-interval 30
```

### 2. PLY转深度图 (ply2depth.py)

将PLY点云文件转换为深度图和RGB图像。

```bash
python ply2depth.py [选项]
```

参数说明：
- `--input-dir`：PLY文件所在目录，默认为当前目录
- `--width`：输出图像宽度，默认为512
- `--height`：输出图像高度，默认为288
- `--fx`：x方向焦距，默认为200
- `--fy`：y方向焦距，默认为200
- `--rx`：绕x轴旋转角度（度），默认为90
- `--ry`：绕y轴旋转角度（度），默认为0
- `--rz`：绕z轴旋转角度（度），默认为0

示例：
```bash
python ply2depth.py --input-dir ./ply_files --width 640 --height 480 --fx 300 --fy 300 --rx 90 --ry 0 --rz 0
```

## 输出文件

- `svo2ply.py` 将生成格式为 `pointcloud_frame_XXXX.ply` 的PLY文件
- `ply2depth.py` 将为每个PLY文件生成对应的深度图（`*_depth.png`）和RGB图像（`*_rgb.png`）

## 注意事项

- 确保系统已正确安装ZED SDK
- 调整FOV参数（fx/fy）时，建议根据实际相机参数设置
- 旋转角度参数（rx/ry/rz）可用于调整点云的视角