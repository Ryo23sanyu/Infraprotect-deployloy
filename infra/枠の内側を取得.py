import ezdxf

# DXFファイルを読み込む
doc = ezdxf.readfile(r'C:\work\django\myproject\program\Infraproject\uploads\121_枠.dxf')

# 特定の画層(D-TTL)に含まれるエンティティを取得する
msp = doc.modelspace()
d_ttl_shapes = [entity for entity in msp if entity.dxf.layer == 'D-TTL']

# 座標の取得
for shape in d_ttl_shapes:
    if shape.dxftype() == 'LWPOLYLINE':
        points = shape.get_points()[0], shape.get_points()[2] # 各頂点の座標を取得(0:左上、2:右下)
        # print(points[0], points[2])  # 各頂点の(X:横方向, Y:縦方向)座標のリストを表示
        print(points)