# Supabase 数据库配置

## 1. 数据表结构

### messages 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键，自增 |
| created_at | timestamp | 创建时间 |
| name | text | 留言者名字 |
| content | text | 留言内容 |
| parent_id | bigint | 父留言ID |
| is_hidden | boolean | 是否隐藏 |
| is_admin_reply | boolean | 是否管理员回复 |

### admins 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键，自增 |
| username | text | 管理员用户名 |
| password_hash | text | 密码哈希值 |
| created_at | timestamp | 创建时间 |

## 2. SQL 命令

### 创建 messages 表
```sql
create