from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

# モデルの定義
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

# サンプルデータの追加
with app.app_context():
    db.create_all()
    sample_items = [
        {'name': 'Item 1', 'description': 'Description 1'},
        {'name': 'Item 2', 'description': 'Description 2'},
        {'name': 'Item 3', 'description': 'Description 3'},
        # ... 他のサンプルデータ
    ]
    for item_data in sample_items:
        db.session.add(Item(**item_data))
    db.session.commit()

# ページングのアイテム数
PER_PAGE = 5

@app.route('/')
def index():
    return render_template('./pandas.html')

@app.route('/data', methods=['GET', 'POST'])
def get_data():
    # 検索
    search = request.args.get('search')
    if search:
        items = Item.query.filter(
            (Item.name.ilike(f'%{search}%')) |
            (Item.description.ilike(f'%{search}%'))
        )
    else:
        items = Item.query

    # ソート
    sort = request.args.get('sort')
    if sort:
        sort_column = sort[1:]
        if sort[0] == '-':
            items = items.order_by(getattr(Item, sort_column).desc())
        else:
            items = items.order_by(getattr(Item, sort_column))

    # ページネーション
    page = int(request.args.get('page', 1))
    items = items.paginate(page=page, per_page=PER_PAGE)

    # レスポンスをJSONで返す
    return jsonify({
        'data': [
            {'id': item.id, 'name': item.name, 'description': item.description}
            for item in items.items
        ],
        'total': items.total,
        'page': items.page,
        'per_page': items.per_page
    })

if __name__ == '__main__':
    app.run(debug=True)
