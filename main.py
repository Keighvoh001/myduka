from flask import Flask,render_template,request,redirect,url_for,flash,session
from database import get_table,insert_products,insert_sales,total_sales,profits, \
    day_sales,profits_day,check_email,register_user,check_logins,total_profit,d_profit,\
        cumulative_sales,total_day_sales,display_product,edit_product,delete_product,cur,conn
# creating an instance



app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# create a route to homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# creating a route for products
@app.route('/products')
def products():
    if 'email' not in session:
        flash('Login to access this page')
        return redirect(url_for('login'))

    prods=get_table("products")
    return render_template('products.html',prods=prods)

# route for adding products
@app.route('/add_products',methods=['POST'])
def add_products():
    pname =request.form["product_name"]
    bprice =request.form["buying_price"]
    sprice =request.form["selling_price"]
    squantity =request.form["stock_quantity"]
    new_products = (pname,bprice,sprice,squantity)
    insert_products(new_products)
    return redirect(url_for('products'))

@app.route('/edit', methods=['post'])
def e_prod():
    new_product_name=request.form['n_product_name']
    new_buying_price=request.form['n_buying_price']
    new_selling_price=request.form['n_selling_price']
    new_stock_quanity=request.form['n_stock_quantity']
    new_product=(new_product_name,new_buying_price,new_selling_price,new_selling_price,new_stock_quanity)
    edit_product(new_product)
    return redirect(url_for('products'))

# deleting route
@app.route("/delete/<int:product_id>")
def delete_product_route(product_id):
    # Call the delete_product function
    result = delete_product(product_id, cur, conn)
    # Check the result and flash appropriate message
    if result:
        flash("Product deleted successfully", "success")
    else:
        flash("Failed to delete product", "error")

    # Redirect to the products page
    return redirect(url_for("products"))
    




    
# creating a route for sales
@app.route('/sales')
def sales():
    if 'email' not in session:
        flash('Login to access this page')
        return redirect(url_for('login'))
    sales=get_table('sales')
    products = get_table('products')
    return render_template('sales.html',sales=sales,products=products)

@app.route('/make_sale', methods=['POST','GET'])
def make_sale():
    pid = request.form['pid']
    quantity=request.form['quantity']
    values = (pid,quantity)
    insert_sales(values)
    d_sales= display_product(pid)
    for i in d_sales:
        sale=i
        flash(f'sales made successfuly for {quantity} {sale}','success')
    return redirect(url_for('sales'))

# route to display dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Login to access this page')
        return redirect(url_for('login'))
    
    pro_fits=profits()
    pro=[]
    fits=[]
    for i in pro_fits:
        pro.append(str(i[0]))
        fits.append(float(i[1]))
    # print(sales)
    sales = total_sales()
    names = []
    values = []
    for i in sales:
        # print(i)
        names.append(str(i[0]))
        values.append(float(i[1]))

    profit_per_day=total_profit()
    day_profit= d_profit()
    sales=total_sales()
    all_sales=cumulative_sales()
    all_day_sales=total_day_sales()



    # route to display sales per day
    d_sales = day_sales()
    sales_day = []
    s_day = []
    for i in d_sales:
        sales_day.append(str(i[0]))
        s_day.append(float(i[1]))

    # route to display profits per day
    profit = profits_day()
    pros = []
    fit = []
    for i in profit:
        pros.append(str(i[0]))
        fit.append(float(i[1]))
    return render_template('dashboard.html',sales=sales,names=names,values=values,pro=pro,
                           fits=fits,sales_day=sales_day,s_day=s_day,pros=pros,fit=fit,profit_per_day=profit_per_day,day_profit=day_profit,all_sales=all_sales,all_day_sales=all_day_sales)

    



@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=='POST':
        f_name=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
        user=(f_name,email,password)
        if not check_email(email):
           register_user(user)
           flash(f'{f_name} is registred successfully','success')
           return redirect(url_for('login'))
        else:
            flash('email exists use another email','danger' )
    return render_template("register.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=check_logins(email,password)
        if user:
            session['email']=email
            flash(f'access granted, welcome {user[1]}',"success")
            return redirect(url_for('dashboard'))
        elif check_email(email):
            flash("email doesn't exist, kindly register","danger")
            return redirect(url_for('register'))
        else:
            flash('access denied try again',"danger")
    return render_template("login.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    return redirect(url_for('home'))



app.run(debug=True)
