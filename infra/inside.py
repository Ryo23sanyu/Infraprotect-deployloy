import ast
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd
import ezdxf

def extract_entities(filename):
    doc = ezdxf.readfile(filename)
    modelspace = doc.modelspace()
    entities = []
    for entity in modelspace:
        entities.append(entity)
    return entities

def find_boundaries(entities):
    boundaries = []
    for entity in entities:
        if entity.dxftype() == 'POLYLINE':
            # ここでは特定の条件(例: レイヤー名が'BOUNDARY'など)でポリラインを判別することができます
            # 特定のポリラインを見つけた場合、そのポリラインの頂点情報を取得します
            vertices = entity.get_points()
            boundaries.append(vertices)
    return boundaries

def is_inside_boundary(entity, boundary):
    x, y, _ = entity.dxf.location
    num_vertices = len(boundary)
    inside = False
    j = num_vertices - 1
    for i in range(num_vertices):
        if ((boundary[i][1] > y) != (boundary[j][1] > y)) and \
                (x < (boundary[j][0] - boundary[i][0]) * (y - boundary[i][1]) /
                (boundary[j][1] - boundary[i][1]) + boundary[i][0]):
            inside = not inside
        j = i
    return inside

filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_細握橋.dxf'
entities = extract_entities(filename)
boundaries = find_boundaries(entities)
inner_entities = extract_inner_entities(entities, boundaries)

print(inner_entities)