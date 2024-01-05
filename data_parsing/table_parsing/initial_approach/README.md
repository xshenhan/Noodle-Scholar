1. 准备环境
```
conda create -n table_extract python=3.9
conda activate table_extract

python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html

pip install pdfplumber camelot-py[base] pdf2image
conda install pytorch==1.10.0 torchvision==0.11.0 cpuonly -c pytorch
conda install poppler
```

2. 运行代码
```
# 请自行指定脚本中的输入输出路径
python extract.py
```

3. 示例
对 `20_good_pdfs` 文件夹里的PDF解析结束后每个PDF会得到一个同名文件夹，文件夹内是所有解析出来的表格
![每个PDF解析出来的目录](demo1.jpg)
![每个目录解析出来的表格](demo2.jpg)