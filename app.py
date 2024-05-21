from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from mysql_util import MysqlUtil
import sys
app = Flask(__name__)
app.secret_key = 'mrsoft12345678'  # 设置秘钥

# 数据可视化相关路由
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
    industry_type_list = df['industry_type']
    industry_type_value_list = df['industry_type_value']

    industry_type_list = industry_type_list.tolist()
    industry_type_value_list = industry_type_value_list.tolist()
    re_data = {
        'industry_type': industry_type_list,
        'industry_type_value': industry_type_value_list,
    }
    print(re_data)
    return jsonify(re_data)

# 商品管理相关路由
def get_products():
    db = MysqlUtil()
    sql = "SELECT id, pname, images, new_price, old_price FROM products"
    products = db.fetchall(sql)
    return products

def get_product_by_id(product_id):
    db = MysqlUtil()
    sql = "SELECT id, pname, images, new_price, old_price, description FROM products WHERE id = %s"
    params = (product_id,)
    try:
        product = db.fetchone(sql, params)
        return product
    except Exception as e:
        print(f"查询失败: {e}")
        return None

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        pname = request.form['pname']
        new_price = request.form['new_price']
        old_price = request.form['old_price']

        db = MysqlUtil()
        sql = "INSERT INTO products2 (pname,new_price, old_price) VALUES (%s, %s, %s)"
        params = (pname, new_price, old_price)
        db.insert(sql, params)
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
    sql = "DELETE FROM products2 WHERE id = %s"
    params = (product_id,)
    db.execute(sql, params)
    return redirect(url_for('manage_products'))

@app.route('/search_product', methods=['GET'])
def search_product():
    search_query = request.args.get('search_query')
    db = MysqlUtil()
    sql = "SELECT id, pname, new_price FROM products2 WHERE pname LIKE %s"
    params = ('%' + search_query + '%',)
    products = db.fetchall(sql, params)
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

@app.route('/login')
def Login():
    return render_template("Login.html")

@app.route('/manage')
def Manage():
    return render_template("Manage_Login.html")

@app.route('/personal')
def Personal():
    return render_template("Personal_center.html")

@app.route('/ShoppingCar')
def ShoppingCar():
    return render_template("ShoppingCar.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        upet_name = request.form['pet_name']
        uphone = request.form['phone']
        upsw = request.form['password']
        db = MysqlUtil()
        sql = "INSERT INTO users(upet_name, uphone, upsw) VALUES (%s, %s, %s)"
        params = (upet_name, uphone, upsw)
        db.insert(sql, params)
        return redirect(url_for('index'))
    else:
        return render_template("Reg.html")

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        upet_name = request.form['login_username']
        password_candidate = request.form['login_password']
        db = MysqlUtil()
        sql = "SELECT * FROM users WHERE upet_name = %s"
        params = (upet_name,)
        result = db.fetchone(sql, params)
        if result:
            db_password = result['upsw']
            if password_candidate == db_password:
                session['logged_in'] = True
                session['login-username'] = upet_name
                return redirect(url_for('index'))
            else:
                return render_template("Login.html", error="密码错误")
        else:
            return render_template("Login.html", error="用户不存在")
    else:
        return render_template("Login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
