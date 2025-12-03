from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import random

# アプリケーション本体を作成
app = Flask(__name__)
# データベース接続先の設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///menu.db"
# 警告メッセージをオフ
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# データベースオブジェクトの作成
db = SQLAlchemy(app)


# メニューモデルの定義
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)


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


# メニュー削除機能
@app.route("/delete/<int:id>", methods=["POST"])
def delete_menu(id):
    # 指定されたIDのメニューを取得
    # 存在しない場合は404エラーを返す
    menu = Menu.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    return redirect(url_for("index"))


# アプリの起動
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
