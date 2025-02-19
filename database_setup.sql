-- 创建留言表
create table messages (
    id bigint generated by default as identity primary key,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    name text not null,
    content text not null,
    parent_id bigint references messages(id),
    is_hidden boolean default false,
    is_admin_reply boolean default false
);

-- 创建管理员表
create table admins (
    id bigint generated by default as identity primary key,
    username text unique not null,
    password_hash text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 设置留言表权限
alter table messages enable row level security;
create policy "Allow anonymous access" on messages for all using (true);

-- 设置管理员表权限
alter table admins enable row level security;
create policy "Allow anonymous access" on admins for select using (true);

-- 创建默认管理员账号（admin/admin123）
insert into admins (username, password_hash) 
values ('admin', 'pbkdf2:sha256:600000$5bpgXBqDEVxL5YAm$b44b62c3e0d39a3fff1d1d3955f43349468ea3655f7682bd95c4e21f6e49a7c3');

-- 表结构说明：
/*
messages 表字段说明：
- id: 主键，自增
- created_at: 创建时间
- name: 留言者名字
- content: 留言内容
- parent_id: 父留言ID（用于回复功能）
- is_hidden: 是否隐藏
- is_admin_reply: 是否为管理员回复

admins 表字段说明：
- id: 主键，自增
- username: 管理员用户名
- password_hash: 密码哈希值
- created_at: 创建时间

默认管理员账号：
用户名：admin
密码：admin123
*/ 