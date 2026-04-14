# 2libraAuto

这是一个用于 `2libra.com` 自动签到的轻量级 Python 项目。

项目通过读取本地保存的 Cookie，向签到接口发送请求，并根据接口返回内容判断签到是否成功。仓库同时提供了 Docker 运行方式和 `cron` 定时执行示例，适合部署在 Linux 服务器上做每日自动签到。

## 项目功能

- 使用本地 Cookie 发起签到请求
- 自动识别“签到成功”或“今日已签到”等返回结果
- 支持直接运行 Python 脚本
- 支持 Docker 容器运行
- 支持通过 `cron` 做定时任务

## 项目结构

```text
.
|-- 2libra_checkin.py     # 主程序，负责读取 Cookie 并执行签到
|-- 2libra_cookie.txt     # Cookie 文件，运行前需要自行填写
|-- Dockerfile            # Docker 镜像构建文件
|-- build.sh              # Docker 镜像构建脚本
|-- run.sh                # Docker 容器运行脚本
|-- crontab.example       # 定时任务示例
|-- .dockerignore         # Docker 构建忽略文件
```

## 运行原理

脚本默认会读取同目录下的 `2libra_cookie.txt`，将其中的 Cookie 放入请求头，然后向以下接口发送 `POST` 请求：

`https://2libra.com/api/sign`

程序会根据以下信息判断是否成功：

- 返回 JSON 中包含“签到成功”“已签到”等关键词
- 返回 JSON 中存在 `success=true`
- 返回 JSON 中 `code` 为 `0`、`200`、`201`
- 返回 HTTP 状态码为 `201`

## 环境要求

- Python 3.12 左右版本即可运行
- 依赖库：`requests`
- 如果使用容器方式，需要安装 Docker

## 使用方式

### 方式一：直接运行 Python 脚本

1. 安装依赖：

```bash
pip install requests
```

2. 编辑 `2libra_cookie.txt`，写入你浏览器中的站点 Cookie。

3. 执行脚本：

```bash
python 2libra_checkin.py
```

运行成功后，终端会输出日志，例如请求地址、HTTP 状态码、耗时以及签到结果。

## Cookie 文件说明

程序默认从当前项目目录读取 `2libra_cookie.txt`。

文件内容示例：

```text
name1=value1; name2=value2; name3=value3
```

注意事项：

- 文件内容必须是完整 Cookie 字符串
- 不要额外加引号
- 不要提交真实 Cookie 到公开仓库
- 如果签到失效，通常是 Cookie 过期，需要重新获取

## 环境变量

脚本支持通过环境变量覆盖默认配置：

- `TWO_LIBRA_SIGN_URL`：签到接口地址，默认值为 `https://2libra.com/api/sign`
- `TWO_LIBRA_TIMEOUT`：请求超时时间，单位秒，默认值为 `20`

示例：

```bash
TWO_LIBRA_TIMEOUT=30 python 2libra_checkin.py
```

## Docker 使用方式

### 构建镜像

项目内已提供 `Dockerfile` 和 `build.sh`。

直接构建：

```bash
docker build -t 2libra-checkin .
```

或者使用脚本：

```bash
sh build.sh
```

注意：当前 `build.sh` 中写死了项目目录为 `/root/code/2libra`，如果你的项目不在这个位置，需要先修改脚本中的 `PROJECT_DIR`。

### 运行容器

直接运行：

```bash
docker run --rm \
  --name 2libra-checkin-job \
  -v $(pwd)/2libra_cookie.txt:/app/2libra_cookie.txt:ro \
  2libra-checkin
```

或者使用脚本：

```bash
sh run.sh
```

同样需要注意，`run.sh` 中也写死了路径 `/root/code/2libra`，如果部署目录不同，需要自行调整：

- `PROJECT_DIR`
- `COOKIE_FILE`

## 定时执行

仓库提供了一个 `cron` 示例文件：`crontab.example`

内容如下：

```cron
0 10 * * * /bin/sh /root/code/2libra/run.sh >> /var/log/2libra-checkin.log 2>&1
```

含义是：

- 每天 `10:00`
- 执行 `run.sh`
- 将输出追加到 `/var/log/2libra-checkin.log`

使用前请根据你的实际部署路径修改脚本路径。

## 日志与退出码

程序使用标准日志输出结果。

退出码约定如下：

- `0`：签到成功
- `1`：请求失败或接口返回失败
- `2`：Cookie 文件不存在或为空

这对于 `cron`、容器健康检查或其他自动化脚本比较有用。

## 安全建议

- `2libra_cookie.txt` 已被 `.dockerignore` 忽略，避免打进镜像
- 建议同时将 Cookie 文件加入 `.gitignore`，避免误提交
- 不要在公共服务器或公共仓库中暴露真实 Cookie

## 当前项目特点

从代码实现来看，这个项目的特点是：

- 代码简单，只有一个核心脚本，维护成本低
- 逻辑清晰，适合放到服务器上长期跑
- 对接口返回做了多种成功判定，兼容性比只判断状态码更好
- Docker 化已经具备基础能力，适合配合 `cron` 使用

如果后续要继续完善，比较自然的方向包括：

- 增加 `requirements.txt`
- 增加 `.gitignore`
- 支持通过环境变量直接传 Cookie，而不依赖文件
- 增加失败通知能力，例如邮件、Telegram 或企业微信
