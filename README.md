# 汽车数据可视化与分析平台

本项目是一个基于 Web 的汽车数据看板，旨在采集、处理并可视化汽车销量与车型信息，帮助业务方（产品、销售、市场）快速获得决策依据。后端使用 Django（Python）负责数据存储与分析，前端使用 Vue.js 提供交互式可视化面板。

---

## 核心亮点
- 技术栈：**Django (Python 3.8)**、**Django ORM（SQLite/Postgres 可选）**、**Vue.js (SFC)**、**Axios**、**SCSS**、以及若干 UI/可视化组件（如 data-view、ECharts 等）。  
- 数据分析为核心：后端在 `myApp/utils/` 中实现排名、聚合、均价计算、能量类型占比等分析函数，然后通过 JSON 接口提供给前端渲染。  
- 业务价值：将原始车辆条目与销量数据转化为可操作的 KPI（热销车型、品牌分布、价格区间均值、能源类型占比、保修/上市周期等），支持业务监控与策略决策。

---

## 项目结构（概览）
- `myApp/` — Django 应用：
  - `models.py`：`CarInfo` 数据模型（字段示例：`brand`、`carName`、`carImg`、`saleVolume`、`price`、`manufacturer`、`rank`、`carModel`、`energyType`、`marketTime`、`insure`、`createTime`）。  
  - `views.py`：对外 JSON 接口（例如 `/myApp/center/`、`/myApp/centerRight/`、`/myApp/centerRightChange/<energyType>` 等）。  
  - `utils/`：数据处理与分析模块（`getCenterData.py`、`getCenterChangeData.py`、`getBottomLeftData.py` 等）。
- `big-screen-vue-datav-master/` — Vue 前端源码（SFC 存放于 `src/views/*.vue`），负责调用后端接口并展示图表与表格。

---

## 数据分析 / 关键计算
后端工具模块实现了主要的分析逻辑，包含但不限于：
- 排行榜与 Top-N：按 `saleVolume` 排序并生成前 N 名列表用于展示。  
- 能源类型聚合：统计不同 `energyType`（如“汽油”“纯电动”）的数量并计算占比。  
- 价格计算：解析 `price` 字段（项目中以 JSON 数组形式存储最低价/最高价）并计算平均价格。  
- 车型/品牌统计：对 `carModel`、`brand` 做频次统计，找出最常见的车型或品牌。  
- 趋势/时序数据：为图表准备时间序列或分段快照，便于在前端绘制折线/柱状等图形。

这些分析函数设计为易读、可扩展的 Python 代码，输出为前端可直接消费的 JSON 结构（减少前端二次处理）。

---

## 开发与实现步骤（简要）
1. 初始化 Django 项目与 `myApp` 应用，设计 `CarInfo` 模型并配置数据库。  
2. 准备数据接入（可通过脚本、导入或通过 Django admin 手动维护数据）。  
3. 在 `myApp/utils/` 实现用于构建各个看板面板的数据处理逻辑。  
4. 在 `myApp/views.py` 中暴露轻量 JSON 接口供前端调用。  
5. 使用 Vue.js 开发前端面板（单文件组件），通过 Axios 获取接口数据并用图表组件可视化。  
6. 迭代优化：增加模板的容错与安全访问（如对空数组的判断、给组件提供安全 key）、修复解析异常等。

---

## 本地运行（快速上手）
后端（Django）：
1. 进入项目目录并创建/激活虚拟环境：  
   Windows: `venv\\Scripts\\activate`  
2. 安装依赖（若无 `requirements.txt`，请自行包含 Django 等）：  
   `pip install -r requirements.txt`  
3. 迁移并启动服务：  
   `python manage.py migrate`  
   `python manage.py runserver 127.0.0.1:8000`

前端（Vue）：
1. 进入 `big-screen-vue-datav-master/`：  
   `npm install`  
   `npm run serve` （或项目对应的开发命令）  
2. 确认前端请求的 API 地址与后端一致（默认 `http://127.0.0.1:8000/`），或通过 Axios 的 baseURL 配置修改目标地址。

---

## 常用接口（示例）
- `GET /myApp/center/` — 返回面板基础数据（统计量、榜单、均价等）。  
- `GET /myApp/centerRight/` — 价格排序/展示数据。  
- `GET /myApp/centerRightChange/<int:energyType>` — 根据能源类型返回不同的 Top-N 列表（油车/电车）。  
- `GET /myApp/bottomRight` — 底部右侧面板数据。

（具体路由与返回字段请查看 `myApp/urls.py` 与 `myApp/views.py`）

---

## 业务价值与应用场景
- 快速洞察：通过排行榜与分布图，快速发现热销车型、品牌与价格区间，支持销售与产品策略调整。  
- 能源转型监测：通过能源类型占比（汽油/纯电）反映市场向新能源迁移的速度，支持战略规划。  
- 生命周期管理：保修期与上市时间等指标帮助判断产品生命周期与换代时机。  
- 报表与下游联动：可将聚合结果导出为 CSV/Excel，接入 BI/报表系统，实现更高级的数据分析与共享。

---

## 可扩展方向
- 增加历史数据存储与时序分析，用于趋势预测与模型训练（可接入时序数据库或将数据入库用于模型训练）。  
- 使用异步任务（Celery）或定时任务批量计算复杂分析，减轻在线计算压力。  
- 增加用户认证与权限管理，按角色展示定制化面板。  
- 对接更多数据源（经销商、第三方市场数据），提升覆盖面与分析深度。



