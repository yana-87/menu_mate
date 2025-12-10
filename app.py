from flask import Flask, render_template, redirect, url_for, request
from extensions import db
from models import Menu
import random

# アプリケーション本体を作成
app = Flask(__name__)
# データベース接続先の設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///menu.db"
# 警告メッセージをオフ
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# アプリとデータベースを接続
db.init_app(app)


# 一覧画面
@app.route("/")
def index():
    menus = Menu.query.all()
    return render_template("index.html", menus=menus)


# メニュー追加機能
@app.route("/add", methods=["POST"])
def add_menu():
    name = request.form.get("name")
    category = request.form.get("category")
    # 受け取ったデータをインスタンス化
    new_menu = Menu(name=name, category=category)
    db.session.add(new_menu)
    db.session.commit()
    return redirect(url_for("index"))


# メニュー編集機能
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_menu(id):
    # 指定されたIDのメニューを取得
    # 存在しない場合は404エラーを返す
    menu = Menu.query.get_or_404(id)
    # POSTの場合はデータを更新
    if request.method == "POST":
        menu.name = request.form.get("name")
        menu.category = request.form.get("category")
        # データベースに変更を保存
        db.session.commit()
        # 一覧画面にリダイレクト
        return redirect(url_for("index"))
    return render_template("edit.html", menu=menu)


# メニュー削除機能
@app.route("/delete/<int:id>", methods=["POST"])
def delete_menu(id):
    # 指定されたIDのメニューを取得
    # 存在しない場合は404エラーを返す
    menu = Menu.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    return redirect(url_for("index"))


# ランダムメニュー表示機能
@app.route("/random", methods=["POST"])
def random_menu():
    category = request.form.get("category")

    if category:
        menus = Menu.query.filter_by(category=category).all()
    else:
        menus = Menu.query.all()

    if menus:
        selected_menu = random.choice(menus)
        return render_template("random.html", menu=selected_menu)
    else:
        return render_template("random.html", menu=None)


# アプリの起動
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
