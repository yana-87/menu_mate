from flask import Flask, render_template, redirect, url_for
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


@app.route("/")
def index():
    return "<h1>Welcome Menu Mate</h1>"


# アプリの起動
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
