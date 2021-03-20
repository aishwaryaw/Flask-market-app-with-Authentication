from market import app, db
from market.models import Item, User
from flask import render_template, redirect, url_for, flash, request
from market.forms import LoginForm, RegisterForm, PurchaseForm, SellingForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    selling_form = SellingForm()
    if request.method == 'POST':
        # Purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations ! You have successfully purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        
        # Sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')

            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
        
        return redirect(url_for('market_page'))
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html', items=items, owned_items=owned_items,purchase_form=purchase_form, selling_form=selling_form)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form= RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, password=form.password1.data, email_address=form.email_address.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'User account created successfully ! You are now logged in with {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))

    # if there are validation errors
    if form.errors != {}: 
        for error_msg in form.errors.values():
            flash(f'There was an error while creating user : {error_msg}', category='danger')

    return render_template("register.html", form=form)



@app.route("/login",methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username= form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))

        else:
            flash('Username and password are not match ! Please try again', category='danger')

    
        
    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash('You have been logged out !', category='success')
    return redirect(url_for('login_page'))


