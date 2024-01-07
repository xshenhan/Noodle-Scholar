# <img src="https://s11.ax1x.com/2023/12/26/pib9yEF.png" width=2.6%>oodle Scholar &ensp;
![Static Badge](https://img.shields.io/badge/simple-green?style=for-the-badge&logo=noodle&color=2e4e7e)
![Static Badge](https://img.shields.io/badge/elegant-green?style=for-the-badge&logo=noodle&color=177cb0)
![Static Badge](https://img.shields.io/badge/delicate-green?style=for-the-badge&logo=noodle&color=44cef6)
![Static Badge](https://img.shields.io/badge/search_engine_for_scholar-green?style=for-the-badge&logo=noodle&color=e3f9fd)


## Start
- **Recommended** Environment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Static Badge](https://img.shields.io/badge/npm-9.8.1-green?)
![Static Badge](https://img.shields.io/badge/node-v18.18.2-green?)
![Static Badge](https://img.shields.io/badge/Python-3.9.0-green?)

- 准备工作
  * 修改 `config.py`，将其中的配置修改成可用配置

- 前端构建
   ```bash
    cd frontend
    npm install
    npm run build
    cd ..
   ```
   会在 `frontend/` 中构建 `dist` 文件夹；根目录中的 `./dist` 将被链接到 `frontend/dist`

- 后端环境配置与运行
  ```bash
    pip install -r requirements.txt
    pip uninstall urllib3
    pip uninstall six
    pip install urllib3
    pip install six
    # 运行
    python server.py
    sanic server.app --port 8088 --host 0.0.0.0 --fast # port：端口 host：监听地址。其他参数含义详见sanic文档
  ```

- 网址
  * 在交大内网中的端口：`10.80.135.205:80`
- 如果你想做出修改：
  * clone 整个文件夹并进入 `git clone https://github.com/xshenhan/Noodle-Scholar.git && cd Noodle-Scholar`
  * 安装依赖 `npm install --no-fund`
  * 在测试端口的预览 `npm run dev`
  * 打开浏览器窗口预览结果

- 如果你想将修改提交
  * 在根目录运行 `npm run build` 将重新构建 `frontend/dist`

## Feature

### Display Build-in Tables in Detail

Provide accurate, completed, powerful table parsing and image parsing. We display on our website all the tables within paper in a detailed and informative way, from which you can copy the raw text.

<img src="https://s11.ax1x.com/2024/01/07/pizTCm8.png" width=60%>

### Everything to be clicked

Every displayed information on pages can be clicked, leading to new result page in which the info will be searched.

### Support Latex Render

<img src="https://s11.ax1x.com/2023/12/26/pib9DBT.png" width=60%>

### Sufficient Database

<img src="https://s11.ax1x.com/2024/01/07/pizohWR.jpg" width=60%>

2,000,000+ Arxiv parpers are search-available, covers numerous fields, such as CS, PHY, STAT, MATH, etc.

### Paper Summary

Support summary of the paper by GPT model, and further Q&A with any questions related to this paper. It’s limited to authorized users currently.

### Adapt Any Screen Size

Except for the visualization charts on the homepage, all pages support mobile access, which means they adapt to screens of any size

## Policy
<img src="https://s11.ax1x.com/2023/12/26/pib92C9.png" width=60%>

<br><br><br><br>
<div align=center><img src="https://s11.ax1x.com/2024/01/07/pizoBzq.png" width=20%></div>
