from flask import render_template, request, redirect, url_for, flash
import mistune
from flask.ext.login import login_user, login_required, current_user, logout_user
from flask.ext.mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash


from exchange import app
from .database import session
from .models import User, Brew, Trade, Proposal, Holding, Comment


@app.route("/")
def market_overview():
    
    return render_template("market.html",
                          )

@app.route("/about")
def about():
        
    user = current_user
    
    users = session.query(User)
    
    user_count = 0
    for user in users:
        if user.active == True:
			user_count += 1
    
    brew_count = session.query(Brew).count()
    
    trades = session.query(Trade)
    
    trade_count = 0
    for trade in trades:
        if trade.active == True:
			trade_count += 1
    
    brews = session.query(Brew)
    
    market_volume = 0
    for brew in brews:
        market_volume = market_volume + brew.brew_count
	
    market_value = 0
    for brew in brews:
        market_value = market_value + (brew.brew_count * brew.brew_value)
    
    
    return render_template("about.html",
                          user=user,
                          user_count=user_count,
                          brew_count=brew_count,
                          trade_count=trade_count,
                          market_volume=market_volume,
                          market_value=market_value
                          )



@app.route("/users/<username_view>", methods=["GET"])
def user_profile_get(username_view):
    user = session.query(User).filter_by(username=username_view).first()
    username = username_view
    name = user.name
    picture = user.picture
    bio = user.bio
    city_state = user.city_state
   
    return render_template("view_profile.html",
                          city_state=city_state,
                          bio=bio,
                          picture=picture,
                          name=name,
                          username=username
                          )


@app.route("/users/<username_view>/edit", methods=["GET"])
@login_required
def user_profile_edit_get(username_view):
    user = session.query(User).filter_by(username=username_view).first()
    name = user.name
    picture = user.picture
    bio = user.bio
    zipcode = user.zipcode
    city_state = user.city_state
	
	
    if current_user.username == user.username:
        return render_template("edit_profile.html",
                              city_state=city_state,
                              zipcode=zipcode,
                              bio=bio,
                              picture=picture,
                              name=name,
                              username=username
                              )
    else:
        flash("Cannot modify other users' profiles", "danger")
        return redirect(url_for("market_overview"))
   
    return render_template("view_profile.html",
                          )
                          
                          

@app.route("/users/<username_view>/edit", methods=["POST"])
@login_required
def user_profile_edit_post(username_view):
    user = session.query(User).filter_by(username=username_view).first()
    user.name = request.form["your name"],
    user.bio = content=mistune.markdown(request.form["a little something about yourself"])
    user.zipcode = request.form["your zipcode"]
    user.city_state = request.form[" your city, state"]
    user.picture = request.form["a url for your profile image"]
    session.commit()
    flash("Your profile updated successfully", "info")
    return redirect(url_for("market_overview") + "users/" + username_view)

"""

@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    user = current_user
    post = session.query(Post).get(id)
    if user.id == post.author_id:
        return render_template("edit_post.html",
                          post=post
                          )
    else:
        flash("Cannot modify other users' posts", "danger")
        return redirect(url_for("posts"))

@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    post = session.query(Post).get(id)
    post.title = request.form["title"],
    post.content = content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))


@app.route("/comment/<id>/edit", methods=["GET"])
@login_required
def edit_comment_get(id):
    user = current_user
    comment = session.query(Comment).get(id)
    if user.id == comment.author_id or user.id == 1:
        return render_template("edit_comment.html",
                          comment=comment  
                          )
    else:
        flash("Cannot modify other users' comments", "danger")
        return redirect(url_for("posts"))
    
@app.route("/comment/<id>/edit", methods=["POST"])
@login_required
def edit_comment_post(id):
    comment = session.query(Comment).get(id)
    comment.content = content=mistune.markdown(request.form["content"])
    session.commit()
    flash("You successfully edited your comment.", "info")
    return redirect(url_for("posts"))



@app.route("/post/<id>/delete", methods=["GET"])
@login_required
def delete_post_get(id):
    user = current_user
    post = session.query(Post).get(id)
    if user.id == post.author_id or post.author_id == None:
        return render_template("delete_post.html",
                          post=post
                          )
    else:
        flash("Cannot modify other users' posts", "danger")
        return redirect(url_for("posts"))




@app.route("/post/<id>/delete", methods=["POST"])
@login_required
def delete_post_delete(id):
    post = session.query(Post).get(id)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/comment/<id>/delete", methods=["GET"])
@login_required
def delete_comment_get(id):
    user = current_user
    comment = session.query(Comment).get(id)
    if user.id == comment.author_id or user.id == 1:
        return render_template("delete_comment.html",
                          comment=comment
                          )
    else:
        flash("Cannot modify other users' comments", "danger")
        return redirect(url_for("posts"))

    
@app.route("/comment/<id>/delete", methods=["POST"])
@login_required
def delete_comment_delete(id):
    comment = session.query(Comment).get(id)
    session.delete(comment)
    session.commit()
    flash("You successfully deleted your comment.", "info")
    return redirect(url_for("posts") + "post/" + str(comment.post_id))

"""



@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")





@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    flash("You are now logged in.", "info")
    return redirect(request.args.get('next') or url_for("market_overview"))




@app.route("/logout", methods=["GET"])
def logout_get():
    return render_template("logout.html")



@app.route("/logout", methods=["POST"])
def logout_post():
    logout_user()
    flash("You are now logged out.", "info")
    return redirect(url_for("market_overview"))




@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")




@app.route("/signup", methods=["POST"])
def signup_post():
    name=request.form["name"]
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]
    password_2=request.form["repassword"]
    
    if session.query(User).filter_by(username=username).first():
        flash("User with that username already exists", "danger")
        return redirect(url_for("signup_get"))
    
    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return redirect(url_for("signup_get"))
        
    if not (password and password_2) or password != password_2:
        flash("Passwords did not match", "danger")
        return redirect(url_for("signup_get"))
    
    user = User(name=name, username=username, email=email, password=generate_password_hash(password))
    
    session.add(user)
    session.commit()
    login_user(user)
    
    """
    mail=Mail(app)
    message = Message(subject="A new user named " + user.name + " signed up with BCHBE",
                  body="The new user's email address is " + current_user.email,
                  sender="buckscountyhomebrewexchange@gmail.com",
                  recipients=["buckscountyhomebrewexchange@gmail.com"])
    
    mail.send(message)
    
    message = Message(subject="You're Ready to Trade",
                  body="Thanks for signing up to trade on the Bucks County Homebrew Exchange, " + current_user.name + "! You're now ready to fill in your profile, list your homebrews on the market, and start trading!",
                  sender="buckscountyhomebrewexchange@gmail.com",
                  recipients=[current_user.email])
    
    mail.send(message)
    """
    
    flash("Success! You're ready to start trading", "info")
    return redirect(url_for("market_overview"))
