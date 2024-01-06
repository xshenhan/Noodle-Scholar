# <img src="https://s11.ax1x.com/2023/12/26/pib9yEF.png" width=7%>  Noodle Scholar

A simple, elegant, delicate search engine for scholar.

## 运行
- 推荐环境
  * npm: 9.8.1
  * node: v18.18.2
  * python: 3.12.0

- 准备工作
  * 修改config.py， 将其中的配置修改成可用配置

- 前端构建
   ```terminal
    cd frontend
    npm install
    npm run build
    cd ..
   ```
   此时会在`frontend/`中出现一个`dist`文件夹，根目录中也有有一个`dist`文件夹被link到`frontend/dist`

- 后端环境配置与运行
  ``` terminal
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
  * clone 整个文件夹
  * 在`./frontend`目录运行 `npm install --no-fund`
  * 在`./frontend`运行 `npm run dev`
  * 打开浏览器窗口预览结果
- 如果你想提交修改
  * 在根目录运行 `npm run build`

## Feature

### Display Build-in Tables in Detail

We display on our website all the tables within paper in a detailed and informative way, from which you can copy the raw text.

### Support Latex Render

<img src="https://s11.ax1x.com/2023/12/26/pib9DBT.png" width=60%>

### Sufficient Database
2,000,000+ papers search-available

## Policy
<img src="https://s11.ax1x.com/2023/12/26/pib92C9.png" width=60%>
