from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-super-secret-key'  # 使用固定的密钥

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# 管理员验证装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    # 获取所有未隐藏的主留言（使用 is 代替 eq）
    messages = supabase.table('messages')\
        .select("*")\
        .is_('parent_id', 'null')\
        .eq('is_hidden', False)\
        .order('created_at', desc=True)\
        .execute()
    
    # 获取每个留言的回复
    for msg in messages.data:
        replies = supabase.table('messages')\
            .select("*")\
            .eq('parent_id', msg['id'])\
            .eq('is_hidden', False)\
            .order('created_at')\
            .execute()
        msg['replies'] = replies.data
    
    return render_template('index.html', messages=messages.data)

@app.route('/post', methods=['POST'])
def post_message():
    name = request.form.get('name')
    content = request.form.get('content')
    parent_id = request.form.get('parent_id')
    
    data = {
        "name": name,
        "content": content,
        "is_admin_reply": False
    }
    
    if parent_id and parent_id.strip():
        data["parent_id"] = int(parent_id)
    
    supabase.table('messages').insert(data).execute()
    return redirect(url_for('index'))

# 管理员路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 简单的明文密码验证
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
        
        return jsonify({'success': False, 'error': '用户名或密码错误'})
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # 这里也做相同的修改
    messages = supabase.table('messages')\
        .select("*")\
        .is_('parent_id', 'null')\
        .order('created_at', desc=True)\
        .execute()
    
    for msg in messages.data:
        replies = supabase.table('messages')\
            .select("*")\
            .eq('parent_id', msg['id'])\
            .order('created_at')\
            .execute()
        msg['replies'] = replies.data
    
    return render_template('admin_dashboard.html', messages=messages.data)

@app.route('/admin/reply', methods=['POST'])
@admin_required
def admin_reply():
    parent_id = request.form.get('parent_id')
    content = request.form.get('content')
    
    data = {
        "name": "管理员",
        "content": content,
        "is_admin_reply": True
    }
    
    if parent_id and parent_id.strip():
        data["parent_id"] = int(parent_id)
    
    supabase.table('messages').insert(data).execute()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/toggle_visibility/<int:message_id>')
@admin_required
def toggle_visibility(message_id):
    message = supabase.table('messages')\
        .select("is_hidden")\
        .eq('id', message_id)\
        .execute()
    
    current_status = message.data[0]['is_hidden']
    
    supabase.table('messages')\
        .update({"is_hidden": not current_status})\
        .eq('id', message_id)\
        .execute()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:message_id>')
@admin_required
def delete_message(message_id):
    # 首先删除所有回复
    supabase.table('messages')\
        .delete()\
        .eq('parent_id', message_id)\
        .execute()
    
    # 然后删除主留言
    supabase.table('messages')\
        .delete()\
        .eq('id', message_id)\
        .execute()
    
    return redirect(url_for('admin_dashboard'))

# 在现有路由后添加退出路由
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True) 