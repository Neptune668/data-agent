# 创建uv环境
-python -m venv venv	创建venv;或者直接uv sync创建
-.\venv\Scripts\Activate.ps1	激活环境

## 1.环境搭建

## 通过docker安装相关中断件并启动服务

- 启动window版本docker（docker desktop）
- 进入docker目录下执行：docker compose up -d

## 构建知识库

- 点击右键运行：build_meta_knowledge.py
- 或者执行命令：python -m app.scripts.build_meta_knowledge

## 运行后端项目

- 点击右键运行： main.py  （使用uvicorn.run）
- 或者执行命令：fastapi dev

## 运行前端项目

- 进入前端项目目录date-agent-frontend下
- 运行：npm install （已安装依赖）
- 运行：npm run dev

## 访问测试

- 浏览器上访问： http://127.0.0.1:5173/  或  http://localhost:5173/

- 搜索：相关问题

  - 统计华北地区销售总额

  - 统计2025年各地区销售总额

  - 统计2025年各个商品的销量

  - 统计各地区销量排名前三的商品

  - 统计1月销量最高的前三个产品

  - 统计3月销售总额最高的前三个产品

    

> 注意： 项目运行最好在非中文目录下