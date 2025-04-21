from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from mysql_util import MysqlUtil
from dotenv import load_dotenv
from spark_ws import SparkChat
import pandas as pd
from mysql_util import MysqlUtil
from dotenv import load_dotenv
import requests  # 新增requests库用于调用DeepSeek API
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'mrsoft12345678'  # 设置秘钥

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from mysql_util import MysqlUtil
from dotenv import load_dotenv
import requests
import os
import time

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'mrsoft12345678')

# 加载环境变量
load_dotenv()

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv('sk-24de632373044cb399782f7cea7a7251')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-coder"



# 设置你的星火大模型 API 信息
appid = "8f79b10c"
api_secret = "YzI1OGRiZTBkZjQ5OTA0NWIzMmNjOTE4"
api_key = "6adc05b5734fd50f3debd7245796f889"
Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"
domain = "lite"


# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-24de632373044cb399782f7cea7a7251"  # 替换为你的DeepSeek API密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API端点

# 首页 & 商品展示
@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)

@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

@app.route('/ajax_get', methods=['GET', 'POST'])
def ajax_data():
    return "这个是来自flask的数据"

@app.route('/get_company', methods=['GET'])
def get_company():
    json = request.json
    print('recv:', json)
    re_data = {
        'company_num': 5896423,
        'job_num': 5001,
        'avg_salary': 50001,
    }
    return jsonify(re_data)

@app.route('/get_industry', methods=['GET'])
def get_industry():
    df = pd.read_csv('./csv/data3.csv', encoding="GB2312")
    industry_type_list = df['industry_type'].tolist()
    industry_type_value_list = df['industry_type_value'].tolist()
    re_data = {
        'industry_type': industry_type_list,
        'industry_type_value': industry_type_value_list,
    }
    print(re_data)
    return jsonify(re_data)

# 商品相关函数
def get_products():
    db = MysqlUtil()
    sql = "SELECT id, pname, images, new_price, old_price FROM products"
    return db.fetchall(sql)

def get_product_by_id(product_id):
    db = MysqlUtil()
    sql = "SELECT id, pname, images, new_price, old_price, description FROM products WHERE id = %s"
    params = (product_id,)
    try:
        return db.fetchone(sql, params)
    except Exception as e:
        print(f"查询失败: {e}")
        return None

# 商品管理路由
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # 确保上传目录存在
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        # 获取表单数据
        pname = request.form['pname']
        new_price = request.form['new_price']
        old_price = request.form['old_price']
        description = request.form.get('description', '')

        # 处理文件上传
        image_file = request.files.get('images')
        image_filename = None
        if image_file and image_file.filename:
            # 生成唯一文件名
            ext = os.path.splitext(image_file.filename)[1]
            image_filename = f"{pname}_{int(time.time())}{ext}"
            image_path = os.path.join(upload_folder, image_filename)
            image_file.save(image_path)

        # 保存到数据库
        db = MysqlUtil()
        sql = """INSERT INTO products2 
                 (pname, images, new_price, old_price, description) 
                 VALUES (%s, %s, %s, %s, %s)"""
        db.insert(sql, (pname, image_filename, new_price, old_price, description))
        
        return redirect(url_for('manage_products'))
    else:
        return render_template('add_product.html')

@app.route('/add_to_management/<int:product_id>', methods=['POST'])
def add_to_management(product_id):
    product = get_product_by_id(product_id)
    if product:
        db = MysqlUtil()
        sql = "INSERT INTO products2 (pname, images, new_price, old_price, description) VALUES (%s, %s, %s, %s, %s)"
        params = (product['pname'], product['images'], product['new_price'], product['old_price'], product['description'])
        db.insert(sql, params)
        return redirect(url_for('manage_products'))
    else:
        return "Product not found", 404

@app.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = request.form['product_id']
    db = MysqlUtil()
    db.execute("DELETE FROM products2 WHERE id = %s", (product_id,))
    return redirect(url_for('manage_products'))

@app.route('/price_prediction')
def price_prediction():
    return render_template('price_prediction.html')

@app.route('/search_product', methods=['GET'])
def search_product():
    search_query = request.args.get('search_query')
    db = MysqlUtil()
    sql = "SELECT id, pname, new_price FROM products2 WHERE pname LIKE %s"
    products = db.fetchall(sql, ('%' + search_query + '%',))
    return render_template('manage_products.html', products=products)

@app.route('/manage_products')
def manage_products():
    db = MysqlUtil()
    sql = "SELECT id, pname, images, new_price, old_price FROM products2"
    products = db.fetchall(sql)
    return render_template('manage_products.html', products=products)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    product = get_product_by_id(book_id)
    if product:
        return render_template("book_detail.html", product=product)
    else:
        return "Product not found", 404

# 聊天接口
@app.route('/chitchatting')
def chitchatting():
    return render_template('chitchatting.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')
#     if not user_input:
#         return jsonify({'error': 'No input'}), 400
#
#     spark = SparkChat(appid, api_secret, api_key, Spark_url, domain)
#     reply = spark.send(user_input)
#     return jsonify({'reply': reply})


# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')
#     if not user_input:
#         return jsonify({'error': 'No input'}), 400
#
#     headers = {
#         "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#         "Content-Type": "application/json"
#     }
#
#     payload = {
#         "model": "deepseek-coder",  # 使用DeepSeek Coder模型
#         "messages": [
#             {"role": "user", "content": user_input}
#         ],
#         "temperature": 0.7
#     }
#
#     try:
#         response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
#         response.raise_for_status()
#         reply = response.json()['choices'][0]['message']['content']
#         return jsonify({'reply': reply})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """处理用户聊天请求并调用DeepSeek API"""
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [{"role": "user", "content": user_input}],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=10
        )
        response.raise_for_status()

        reply = response.json()['choices'][0]['message']['content']
        return jsonify({
            'reply': reply,
            'usage': response.json().get('usage', {})
        })

    except requests.exceptions.RequestException as e:
        app.logger.error(f"API请求失败: {str(e)}")
        return jsonify({'error': '服务暂时不可用'}), 503
    except Exception as e:
        app.logger.error(f"处理聊天时出错: {str(e)}")
        return jsonify({'error': '内部服务器错误'}), 500

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        upet_name = request.form['pet_name']
        uphone = request.form['phone']
        upsw = request.form['password']
        db = MysqlUtil()
        sql = "INSERT INTO users(upet_name, uphone, upsw) VALUES (%s, %s, %s)"
        db.insert(sql, (upet_name, uphone, upsw))
        return redirect(url_for('index'))
    else:
        return render_template("Reg.html")

# 用户登录
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        upet_name = request.form['login_username']
        password_candidate = request.form['login_password']
        db = MysqlUtil()
        sql = "SELECT * FROM users WHERE upet_name = %s"
        result = db.fetchone(sql, (upet_name,))
        if result:
            if password_candidate == result['upsw']:
                session['logged_in'] = True
                session['login-username'] = upet_name
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('index'))
            else:
                return render_template("Login.html", error="密码错误")
        else:
            return render_template("Login.html", error="用户不存在")
    else:
        return render_template("Login.html")


@app.route('/api/books/statistics')
def book_statistics():
    conn = sqlite3.connect('database.db')  # 替换为你的数据库连接
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            SUM(CASE WHEN new_price < 20 THEN 1 ELSE 0 END) AS below_20,
            SUM(CASE WHEN new_price BETWEEN 20 AND 50 THEN 1 ELSE 0 END) AS between_20_50,
            SUM(CASE WHEN new_price > 50 THEN 1 ELSE 0 END) AS above_50,
            COUNT(*) AS total_books,
            ROUND(AVG(new_price), 2) AS avg_price
        FROM products;
    """)
    result = cur.fetchone()
    conn.close()

    return jsonify({
        'below_20': result[0],
        'between_20_50': result[1],
        'above_50': result[2],
        'total_books': result[3],
        'avg_price': result[4]
    })


@app.route('/api/price/predict', methods=['POST'])
def predict_price():
    data = request.json
    isbn = data.get('isbn')
    days = data.get('days')
    
    # 这里添加实际的价格预测和比价逻辑
    # 模拟数据示例：
    return jsonify({
        "history": {
            "dates": ["2023-01-01", "2023-01-02"],
            "prices": [45.8, 46.2]
        },
        "prediction": {
            "dates": ["2023-01-03", "2023-01-04"],
            "prices": [47.0, 47.5]
        },
        "current_price": 46.2,
        "trend": "up",
        "suggestion": "建议观望，价格可能继续上涨",
        "platform_prices": {
            "京东": 45.5,
            "当当": 46.8,
            "亚马逊": 47.2
        }
    })
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 其它页面
@app.route('/manage')
def Manage():
    return render_template("Manage_Login.html")

@app.route('/Personal')
def Personal():
    return render_template("Personal_center.html")

@app.route('/ShoppingCar')
def ShoppingCar():
    return render_template("ShoppingCar.html")

#图书管理员



# 启动服务
if __name__ == '__main__':
    app.run(debug=True)
