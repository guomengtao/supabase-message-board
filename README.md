# 留言板系统

一个使用 Flask 和 Supabase 构建的简单留言板系统。支持留言、回复、管理员后台等功能。

## 功能特点

- 前台功能
  - 发布留言
  - 回复留言
  - 查看留言列表
  - 管理员回复高亮显示

- 管理员后台
  - 管理员登录/退出
  - 回复留言
  - 隐藏/显示留言
  - 删除留言及其回复

## 技术栈

- 后端：Python Flask
- 数据库：Supabase
- 前端：HTML/CSS/JavaScript
- 其他：python-dotenv, werkzeug.security

## 安装和运行

1. 克隆仓库
```bash
git clone https://github.com/guomengtao/message-board.git
cd message-board
```

2. 创建并激活虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip3 install flask supabase python-dotenv
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 Supabase 项目信息
```

5. 初始化数据库
- 在 Supabase 中创建新项目
- 复制 database_setup.sql 中的内容到 Supabase SQL 编辑器并执行

6. 运行应用
```bash
python3 app.py
```

访问 http://localhost:5000 查看应用

## 管理员访问

- 后台地址：http://localhost:5000/admin/login
- 默认账号：admin
- 默认密码：admin123

## 项目结构

```
message-board/
├── app.py              # 主应用文件
├── templates/          # HTML 模板
│   ├── index.html         # 前台页面
│   ├── admin_login.html   # 管理员登录
│   └── admin_dashboard.html# 管理后台
├── database_setup.sql  # 数据库初始化脚本
├── .env.example        # 环境变量示例
├── .gitignore         # Git 忽略文件
└── README.md          # 项目说明
```

## 安全说明

1. 生产环境部署前：
   - 修改默认管理员密码
   - 使用强密钥替换 app.secret_key
   - 确保 .env 文件安全且不被提交
   - 定期更新依赖包

2. 数据库安全：
   - 使用环境变量管理数据库凭据
   - 已启用 Row Level Security
   - 仅公开必要的数据库操作权限

## 开发说明

1. 代码风格遵循 PEP 8
2. 使用 Flask 内置的开发服务器
3. 支持热重载便于开发

## License

MIT