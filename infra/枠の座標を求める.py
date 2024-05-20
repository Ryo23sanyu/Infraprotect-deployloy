import ezdxf

# ファイルパス
filename = R'C:\work\django\myproject\program\Infraproject\uploads\2径間.dxf'

doc = ezdxf.readfile(filename)
msp = doc.modelspace()

# 処理したいレイヤーの名前
layers_to_process = ["Defpoints"]

# 必要なレイヤーの描画オブジェクトを探す
for layer_name in layers_to_process:
    # レイヤーが存在するか確認
    if not doc.layers.has_entry(layer_name):
        print(f"Layer {layer_name} not found.")
        continue
    
    # レイヤー内のLINESタイプのオブジェクトを取得
    for entity in doc.modelspace().query('LINE[layer=="{}"]'.format(layer_name)):
        start_point = entity.dxf.start
        end_point = entity.dxf.end
        # ここでは、線の始点と終点の座標を表示しますが、
        # 必要に応じて他の処理を行ってください。
        print(f"Layer: {layer_name}, Start: {start_point}, End: {end_point}")