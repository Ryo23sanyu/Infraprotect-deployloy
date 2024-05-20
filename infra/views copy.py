import glob
import pprint
import re
from django.views import View
import pandas as pd
import os
import ezdxf
import tkinter
import tkinter.filedialog
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from markupsafe import Markup
from requests import Response
from .models import Approach, Article, DamageReport, Infra, LoadGrade, LoadWeight, Photo, Panorama, Number, Regulation, Rulebook, Thirdparty, UnderCondition
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import BridgeCreateForm, BridgeUpdateForm, CensusForm, FileUploadForm, NumberForm, UploadForm, PhotoUploadForm, NameForm
from django.views.generic.edit import FormView
from ezdxf.entities.mtext import MText
from PIL import Image, ImageTk

class ListInfraView(LoginRequiredMixin, ListView):
    template_name = 'infra/infra_list.html'
    model = Infra # 使用するモデル「infra」
    def get_queryset(self, **kwargs):
        # モデル検索のクエリー。Infra.objects.all() と同じ結果で全ての Infra
        queryset = super().get_queryset(**kwargs)
        # パスパラメータpkによりarticleを求める
        article = Article.objects.get(id = self.kwargs["pk"])
        # 求めたarticleを元にモデル検索のクエリーを絞り込む
        queryset = queryset.filter(article=article)
        # 絞り込んだクエリーをDjangoに返却し表示データとしてもらう
        return queryset

    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["pk"]
        return super().get_context_data(**kwargs)


class DetailInfraView(LoginRequiredMixin, DetailView):
    template_name = 'infra/infra_detail.html'
    model = Infra
    # fields = ('交通量', '大型車混入率')
    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["pk"]
        return super().get_context_data(**kwargs)
  
class CreateInfraView(LoginRequiredMixin, CreateView):
  template_name = 'infra/infra_create.html' # 対応するhtmlの名前
  model = Infra # models.pyのどのモデルと紐付くか
  # form_class = BridgeCreateForm # forms.pyのどのクラスと紐付くか
  fields = ('title', '径間数', '橋長', '全幅員','橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検', '海岸線との距離', '路下条件', '交通量', '大型車混入率', '特記事項', 'カテゴリー', 'article')
  success_url = reverse_lazy('detail-infra')

  def form_valid(self, form):
    #ここのobjectはデータベースに登録を行うmodelつまりInfraの１レコードです。
    #formはModelFormと呼ばれるフォームの仕組みで、saveを実行すると関連付いているモデルとして登録を行う動きをします。
    object = form.save(commit=False)
    #ここでのobjectは登録対象のInfraモデル１件です。登録処理を行いPKが払い出された情報がobjectです
    #今回はarticle_id、つまりarticleオブジェクトが無いのでこれをobjectに設定します。
    #articleオブジェクトを検索しobjectに代入する事で登録できます。
    article = Article.objects.get( id = self.kwargs["pk"] )
    # id = 1 のarticleを検索
        # article = Article.objects.get(id = 1 )
    object.案件名 = article
    # titleの項目に「A」を設定
        # article.title = "A"
    #設定したのちsaveを実行し更新します。
    object.save()
    return super().form_valid(form)

  def get_success_url(self):
    return reverse_lazy('list-infra', kwargs={'pk': self.kwargs["pk"]})

  #新規作成時、交通規制の全データをコンテキストに含める。
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["loadWeights"] = LoadWeight.objects.all()
    context["loadGrades"] = LoadGrade.objects.all()
    context["rulebooks"] = Rulebook.objects.all()
    context["approachs"] = Approach.objects.all()
    context["regulations"] = Regulation.objects.all()
    context["thirdpartys"] = Thirdparty.objects.all()
    context["underconditions"] = UnderCondition.objects.all()
    return context
    
  def keikan_create_view(request): # keikan_create_view関数を定義
    if request.method == "POST": # リクエストメソッドがpostの場合
        form = BridgeCreateForm(request.POST) # BridgeCreateFormというフォームクラスのインスタンスを生成
        if form.is_valid(): # formが正常の場合
            keikan_number = form.cleaned_data['径間数'] # form.cleaned_dataから'径間数'キーに対応するデータを取得
            request.session['keikan_number'] = keikan_number # 取得した"径間数"を現在のユーザーセッションに保存
            return redirect('table') # 「table」という名前のURLにリダイレクト
        else:
            form = BridgeCreateForm() # 新しい空のフォームインスタンスを生成
    return render(request, 'infra/infra_create.html', {'form': form}) # 'infra_create.html'テンプレートをレンダリング
  def damage_view(request): # damage_view関数を定義
    keikan_number = request.session.get('keikan_number', 1) # request.session.getメソッドを使い、セッションから"径間数"を取得、デフォルト値は1
    keikan_range = list(range(keikan_number)) # 1からkeikan_number（"径間数"）までの連続する整数列を生成
    return render(request, 'table.html', {'keikan_range': keikan_range}) # 'table.html'テンプレートをレンダリング

class DeleteInfraView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/infra_delete.html'
  model = Infra
  success_url = reverse_lazy('list-infra')
  
class UpdateInfraView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/infra_update.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検', '海岸線との距離', '路下条件', '交通量', '大型車混入率', '特記事項', 'カテゴリー', 'article')
  success_url = reverse_lazy('detail-infra')
  def get_success_url(self):
    return reverse_lazy('detail-infra', kwargs={'pk': self.kwargs["pk"]})

  #新規作成時、交通規制の全データをコンテキストに含める。
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # 編集中のインスタンスに紐づく交通規制のIDをリストとして取得
    # コンテキストに追加
    selected_regulations = self.object.交通規制.values_list('id', flat=True)# 選択状態を保持
    context['selected_regulations'] = list(selected_regulations)# 選択状態を保持
    context["regulations"] = Regulation.objects.all()
    
    selected_loadWeights = self.object.活荷重.values_list('id', flat=True)
    context['selected_loadWeights'] = list(selected_loadWeights)
    context["loadWeights"] = LoadWeight.objects.all()
    
    selected_loadGrades = self.object.等級.values_list('id', flat=True)
    context['selected_loadGrades'] = list(selected_loadGrades)
    context["loadGrades"] = LoadGrade.objects.all()
    
    selected_rulebooks = self.object.適用示方書.values_list('id', flat=True)
    context['selected_rulebooks'] = list(selected_rulebooks)
    context["rulebooks"] = Rulebook.objects.all()
    
    selected_approachs = self.object.近接方法.values_list('id', flat=True)
    context['selected_approachs'] = list(selected_approachs)
    context["approachs"] = Approach.objects.all()
    
    selected_thirdpartys = self.object.第三者点検.values_list('id', flat=True)
    context['selected_thirdpartys'] = list(selected_thirdpartys)
    context["thirdpartys"] = Thirdparty.objects.all()
    
    selected_underconditions = self.object.路下条件.values_list('id', flat=True)
    context['selected_underconditions'] = list(selected_underconditions)
    context["underconditions"] = UnderCondition.objects.all()
    return context

def infra_view(request):
  if request.method == 'POST':
    等級 = request.POST.get('等級', None)
    # load_gradeを使って必要な処理を行う
    # 例えば、選択されたload_gradeに基づいてデータをフィルタリングして表示するなど

  # 通常のビューロジック
  return render(request, 'infra/infra_detail.html')

def index_view(request):
  order_by = request.GET.get('order_by', '案件名')
  object_list = Article.objects.order_by(order_by)
  return render(request, 'infra/index.html', {'object_list': object_list})

# def index_view(request):
  # order_by = request.GET.get('order_by', 'span_number')
  # object_list = Infra.objects.order_by(order_by)
  # return render(request, 'infra/index.html', {'object_list': object_list})

class ListArticleView(LoginRequiredMixin, ListView):
  template_name = 'infra/article_list.html'
  model = Article
  
class DetailArticleView(LoginRequiredMixin, DetailView):
  template_name = 'infra/article_detail.html'
  model = Article
  
class CreateArticleView(LoginRequiredMixin, CreateView):
  template_name = 'infra/article_create.html'
  model = Article
  fields = ('案件名', '土木事務所', '対象数', '担当者名', 'その他')
  success_url = reverse_lazy('list-article')
  
class DeleteArticleView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/article_delete.html'
  model = Article
  success_url = reverse_lazy('list-article')
  
class UpdateArticleView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/article_update.html'
  model = Article
  fields = ('案件名', '土木事務所', '対象数', '担当者名', 'その他')
  success_url = reverse_lazy('list-article')
  
# class ArticleInfraView(LoginRequiredMixin, DetailView):
 # template_name = 'infra/infra_article.html'
 #  model = Article
 
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'infra/file_upload.html', {'form': form})

def file_upload_success(request):
    return render(request, 'infra/file_upload_success.html')
  
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'infra/photo_list.html', {'photos': photos})

def selected_photos(request):
    selected_photo_ids = request.POST.getlist('selected_photos')
    selected_photos = Photo.objects.filter(id__in=selected_photo_ids)
    return render(request, 'infra/selected_photos.html', {'selected_photos': selected_photos})

# 会社別に表示

#@login_required
#def my_view(request):
    #user = request.user
    # 会社情報を使ってコンテンツをフィルタリングする処理
    #filtered_data = Data.objects.filter(company=user.company)
    #return render(request, 'template.html', {'filtered_data': filtered_data})
  
# 全景写真

# def panorama_list(request):
#     panorama = Panorama.objects.all()
#     return render(request, 'panorama_list.html', {'panorama': panorama})

def panorama_list(request):
    panoramas = Panorama.objects.all()
    if request.method == 'POST':
        selected_ids = request.POST.getlist('image_list')
        for panorama in panoramas:
            if str(panorama.id) in selected_ids:
                panorama.checked = True
            else:
                panorama.checked = False
            panorama.save()
        return redirect('image_list')  # 再描画のためにリダイレクト
    
    return redirect('image_list')
    #return render(request, 'image_list.html', {'panoramas': panoramas})


def panorama_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        checked = request.POST.get('checked', False)
        panorama = Panorama.objects.create(image=image, checked=checked)
        return redirect('photo')
    return render(request, 'panorama_upload.html')
   
# 番号表示  

def number_view(request):
    start = "0101"
    end = "0206"

    # 最初の2桁と最後の2桁を取得
    start_prefix = start[:2]
    start_suffix = start[2:]
    end_prefix = end[:2]
    end_suffix = end[2:]

    # 抽出した数字を文字列として結合
    result = ""
    for prefix in range(int(start_prefix), int(end_prefix)+1):
        for suffix in range(int(start_suffix), int(end_suffix)+1):
            result += "{:02d}{:02d}\n".format(prefix, suffix)

    return HttpResponse(result)

# <<テーブルの作成>>
def table_view(request):
    # AutoCADファイル名を指定してテキストを抽出する
    dxf_filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf'
    search_title_text = "1径間" # 複数径間の場合は"1径間"
    second_search_title_text = "損傷図"
    
    def find_square_around_text(dxf_filename, target_text, second_target_text):
        doc = ezdxf.readfile(dxf_filename)
        msp = doc.modelspace()
       
        text_positions = [] # 見つかったテキストの位置を格納するためのリストを作成
        
        extracted_text = []

        # MTEXTエンティティの各要素をtextという変数に代入してループ処理
        for mtext_insert_point in msp.query('MTEXT'): # モデルスペース内の「MTEXT」エンティティをすべて照会し、ループ処理
            if mtext_insert_point.dxf.text == target_text: # エンティティのテキストが検索対象のテキストと一致した場合
                text_insertion_point = mtext_insert_point.dxf.insert # テキストの挿入点(dxf.insert)を取得します。
                text_positions.append(text_insertion_point[0]) # 挿入点のX座標をリストに保存
                break

        if not text_positions: # text_positionsリストが空の場合(見つけられなかった場合)
            for mtext_insert_point in msp.query('MTEXT'): # モデルスペース内の「MTEXT」エンティティをすべて照会し、ループ処理
                if mtext_insert_point.dxf.text == second_target_text: # エンティティのテキストが検索対象のテキストと一致した場合
                    text_insertion_point = mtext_insert_point.dxf.insert # テキストの挿入点(dxf.insert)を取得します。
                    text_positions.append(text_insertion_point[0]) # 挿入点のX座標をリストに保存
                    break
        
        # Defpointsレイヤーで描かれた正方形枠の各要素をsquare変数に代入してループ処理
        for defpoints_square in msp.query('LWPOLYLINE[layer=="Defpoints"]'): # 
            if len(defpoints_square) == 4: # 正方形(=4辺)の場合
                square_x_values = [four_points[0] for four_points in defpoints_square] # squareというリストをループして各点(point)からx座標(インデックス0の要素)を抽出
                square_min_x = min(square_x_values) # 枠の最小X座標を取得
                square_max_x = max(square_x_values) # 枠の最大X座標を取得
                
            # 文字のX座標が枠の最小X座標と最大X座標の間にあるかチェック
            # text_positionsの各要素をtext_x_positionという変数に代入してforループを処理
            for text_x_position in text_positions:
                
                # 文字の座標がDefpoints枠のX座標内にある場合
                if square_min_x <= text_x_position <= square_max_x:
                    
                    # print(list(square)) 4点の座標を求める 
                    left_top_point = list(defpoints_square)[0][0] # 左上の座標
                    right_top_point = list(defpoints_square)[1][0] # 右上の座標
                    right_bottom_point = list(defpoints_square)[2][0] # 右下の座標
                    left_bottom_point = list(defpoints_square)[3][0] # 左下の座標

                    defpoints_max_x = max(left_top_point,right_top_point,left_bottom_point,right_bottom_point) # X座標の最大値
                    defpoints_min_x = min(left_top_point,right_top_point,left_bottom_point,right_bottom_point) # X座標の最小値
                    
        # 指定したX座標範囲内にあるテキストを探す
        for circle_in_text in msp.query('MTEXT'):
            if defpoints_min_x <= circle_in_text.dxf.insert.x <= defpoints_max_x and circle_in_text.dxf.layer != 'Defpoints':
            # MTextのテキストを抽出する
                text = circle_in_text.plain_text()
                x, y, _ = circle_in_text.dxf.insert
                if not text.startswith("※"):
                    cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
                    # if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
                    if len(cad_data) > 0 and not any(keyword in text for keyword in ["×", ".", "損傷図"]) and not text.endswith("径間"):
                # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                        related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
                # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                        for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                        # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                            if entity_extension(circle_in_text, neighbor):
                            # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                                related_text = neighbor.plain_text()
                                defx, defy, _ = neighbor.dxf.insert
                            #extracted_text.append(neighbor_text)
                                break # 文字列が見つかったらbreakによりforループを終了する

                        if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                            cad_data.append(related_text[:]) # cad_dataに「部材名～使用写真」までを追加
                            cad_data.append([str(x), str(y)]) # 続いてcad_dataに「MTEXT」のX,Y座標を追加
                    #最後にまとめてcad_dataをextracted_textに追加する
                        extracted_text.append(cad_data[:] + [[str(defx), str(defy)]]) # extracted_textに「MTEXTとその座標」およびdefのX,Y座標を追加
                        
# << ※特記なき損傷の抽出用 ↓ >>                            
                else:
                    lines = text.split('\n')# 改行でテキストを分割してリスト化
                    sub_text = [[line] for line in lines]# 各行をサブリストとして持つ多重リストを構築

                    pattern = r"\s[\u2460-\u3256]"# 文字列のどこかにスペース丸数字の並びがあるかをチェックする正規表現パターン
                    pattern_start = r"^[\u2460-\u3256]"  # 文字列の開始が①～㉖であることをチェックする正規表現パターン
                    pattern_anywhere = r"[\u2460-\u3256]"  # 文字列のどこかに①～㉖があるかをチェックする正規表現パターン
                    last_found_circle_number = None  # 最後に見つかった丸数字を保持する変数

                    # リストを逆順でループし、条件に応じて処理
                    for i in range(len(sub_text)-1, -1, -1):  # 後ろから前にループ
                        item = sub_text[i][0]  # textリストの各サブリストの最初の要素（[0]）をitem変数に代入（地覆 ㉓-c）
                        if item.startswith("※"):
                            sub_text.remove(sub_text[i]) # 配列から除外する
                        elif re.search(pattern, item):  # itemが正規表現patternと一致している場合（スペース丸数字の並びがある）
                            last_found = item  # last_found変数にitem要素を代入（地覆 ㉓-c）
                            # print(last_found) 丸数字が付いている要素のみ出力
                        elif 'last_found' in locals():  # last_foundが定義されている（要素が代入されている）場合のみ
                            space = last_found.replace("　", " ")
                            # 大文字スペースがあれば小文字に変換
                            second = space.find(" ", space.find(" ") + 1)#10
                            # 2つ目のスペース位置まで抽出
                            sub_text[i][0] = item + last_found[second:]
                            # item:スペース丸数字の並びがない文字列
                            # last_found:スペース丸数字の並びがある文字列
                            # last_found[second:]:スペースを含めた文字列
                        elif re.match(pattern_start, item): # 文字列が①～㉖で開始するかチェック
                            last_found_circle_number = item # 丸数字の入っている要素を保持
                            sub_text.remove(sub_text[i])
                        else:
                            if last_found_circle_number is not None and not re.search(pattern_anywhere, item):
                                # 要素に丸数字が含まれておらず、直前に丸数字が見つかっている場合
                                sub_text[i][0] += " " + last_found_circle_number  # 要素の末尾に丸数字を追加

                    for sub_list in sub_text:
                        # サブリストの最初の要素を取得してスペース区切りで分割
                        split_items = sub_list[0].split()
                        
                        # 分割した要素から必要なデータを取り出して新しいサブリストに格納
                        header = split_items[0] + " " + split_items[1]  # 例：'主桁 Mg0101'
                        status = split_items[2]  # 例：'①-d'
                        # photo_number = '写真番号-00'
                        # defpoints = 'defpoints'
                        
                        # 新しい形式のサブリストを作成してprocessed_listに追加
                        # new_sub_list = [header, status, photo_number, defpoints]
                        new_sub_list = [header, status]
                        extracted_text.append(new_sub_list)

                        new_sub_list.append([str(x), str(y)])
# << ※特記なき損傷の抽出用 ↑ >>
        return extracted_text

    def entity_extension(mtext, neighbor):
        # MTextの挿入点
        mtext_insertion = mtext.dxf.insert
        # 特定のプロパティ(Defpoints)で描かれた文字の挿入点
        neighbor_insertion = neighbor.dxf.insert
        #テキストの行数を求める
        text = mtext.plain_text()
        text_lines = text.split("\n") if len(text) > 0 else []
        # 改行で区切ったリスト数→行数
        text_lines_count = len(text_lines)
        
        # Defpointsを範囲内とするX座標範囲
        x_start = mtext_insertion[0]  # X開始位置
        x_end  = mtext_insertion[0] + mtext.dxf.width # X終了位置= 開始位置＋幅
        y_start = mtext_insertion[1] + mtext.dxf.char_height # Y開始位置
        y_end  = mtext_insertion[1] - mtext.dxf.char_height * (text_lines_count + 1) # 文字の高さ×(行数+1)
        
        # MTextの下、もしくは右に特定のプロパティで描かれた文字が存在するかどうかを判定する(座標：右が大きく、上が大きい)
        if (
            neighbor_insertion[0] >= x_start and neighbor_insertion[0] <= x_end
        ):
            if ( #y_endの方が下部のため、y_end <= neighbor.y <= y_startとする
                neighbor_insertion[1] >= y_end and neighbor_insertion[1] <= y_start
            ):
                return True
        
        return False

    extracted_text = find_square_around_text(dxf_filename, search_title_text, second_search_title_text) # 関数の定義

    for index, data in enumerate(extracted_text):
        # 最終項目-1まで評価
        if index < (len(extracted_text) -1):
            # 次の位置の要素を取得
            next_data = extracted_text[index + 1]
            # 特定の条件(以下例だと、１要素目が文字s1,s2,s3から始まる）に合致するかチェック
            if ("月" in next_data[0] and "日" in next_data[0]) or ("/" in next_data[0]) and (re.search(r"[A-Z]", next_data[0], re.IGNORECASE) and re.search(r"[0-9]", next_data[0])):
                # 合致する場合現在の位置に次の要素を併合 and "\n" in cad
                data.extend(next_data)
                # 次の位置の要素を削除
                extracted_text.remove(next_data)
# extracted_text = [['主桁 Mg0101', '①-d', '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]

# << ◆部材名(first)の要素◆ >>
        # コンマが3つ以上存在する場合、3の倍数の位置で改行を挿入    
        def insert_line_breaks_on_commas(text):
            # コンマのカウントと改行の挿入を行う
            count = 0
            new_text = ''
            for char in text:
                if char == ',':
                    count += 1
                    if count % 3 == 0:
                        # 3, 6, 9番目のコンマの後に改行タグを挿入
                        new_text += ',</br>'
                        continue
                new_text += char
            return new_text
        
        # 正規表現を使って、コンマの直後に数字以外の文字が続く場所を見つけます。
        pattern = re.compile(r',(?![0-9])')
        
        result_first_list = []  # 結果を格納するリスト
        for sub_list in extracted_text:
            # 正規表現による置換を実行
            replaced_text = pattern.sub(",</br>", sub_list[0])
            # コンマごとに改行を挿入
            with_inserted_breaks = insert_line_breaks_on_commas(replaced_text)
            # 最終的な文字列をMarkupオブジェクトとしてリストに追加
            final_text = Markup(with_inserted_breaks)
            result_first_list.append(final_text)

        # 書き直したコードの結果を使用する
        first_item = result_first_list
        
# << ◆損傷種類(second)の要素◆ >>
    # リストの各要素から記号を削除する
        def remove_symbols(other_items):
            symbols = ['!', '[', ']', "'"]

            processed_other_items = []
            for item in other_items:
                processed_item = ''.join(c for c in item if c not in symbols)
                processed_other_items.append(processed_item)
    
            return processed_other_items
        
    # それ以外の要素(損傷名)を抽出
        pattern = r'[\u2460-\u2473\u3251-\u3256].*-[a-zA-Z]' # 丸数字とワイルドカードとアルファベット
        other_items = []
        for sub_list in extracted_text:
            filtered_sub_list = []
            for item in sub_list:
                if isinstance(item, str):# itemが文字列か確認
                    if re.match(pattern, item):# itemが正規表現と一致した場合
                        filtered_sub_list.append(item)# filtered_sub_listリストに格納
            other_items.append(filtered_sub_list)# forループの後にfiltered_sub_listリストをother_itemsリストに格納

        second = remove_symbols(other_items)
        # 丸数字を直接列挙
        circle_numbers = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖'
        second_items = []

        # リスト内の各文字列に対して処理を行う
        for second_over in second:
            # アルファベット(aからe)と直後に続く特定の丸数字の間にコンマを挿入
            if second_over == "":
                second_items.append(None)
            else:
                second_item = re.sub(f'([a-e])([{circle_numbers}])', r'\1,\2', second_over)
                second_split = second_item.split(",")
                second_items.append(second_split)
                
# << ◆写真番号-00(third)、Defpoints(bottom)、旗揚げ座標(damage_coordinate)、Def座標(picture_coordinate)の要素◆ >>
        third_items = []
        bottom_item = []
        damage_coordinate = []
        picture_coordinate = []
        for sub_list in extracted_text:
            list_count = sum(isinstance(item, list) for item in sub_list) # リストの中にリストがいくつあるか数える
            
            if list_count == 2: # 座標が2つのとき=Defpointsが存在するとき
                bottom_item.append(sub_list[-3]) # 最後から3番目の要素を抽出（写真番号-00）
                third_items.append(sub_list[-4]) # 最後から4番目の要素を抽出（Defpoints）
                damage_coordinate.append(sub_list[-2])
                picture_coordinate.append(sub_list[-1])
            else: # Defpointsがない時
                bottom_item.append("") # bottom:写真番号なし
                third_items.append(None) # third:Defpointsなし
                damage_coordinate.append(sub_list[-1]) # damage:
                picture_coordinate.append(None) # picture:写真指定なし

        result_items = []# 配列を作成
        for item in bottom_item:# text_itemsの要素を1つずつitem変数に入れてforループする
            if ',' in item:# 要素の中にカンマが含まれている場合に実行
                sub_items = item.split(',')# カンマが含まれている場合カンマで分割
                extracted_item = []# 配列を作成
                for item in sub_items:# bottom_itemの要素を1つずつitem変数に入れてforループする
                    for p in range(len(item)):#itemの文字数をiに代入
                        if "A" <= item[p].upper() <= "Z" and p < len(item) - 1 and item[p+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                            extracted_item.append(item[:p+1]+"*/*"+item[p+1:])# アルファベットと数字の間に*/*を入れてextracted_itemに代入
                            break
                join = ",".join(extracted_item)# 加工した内容をカンマ区切りの１つの文字列に戻す
                result_items.append(join)# result_itemsに格納

            else:# ifがfalseの場合(カンマが含まれていない場合)
                non_extracted_item = ''
                for j in range(len(item)):
                    if item[j].isalpha() and j < len(item) - 1 and item[j+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                        non_extracted_item = item[:j+1]+"*/*"+item[j+1:]#アルファベットまでをextracted_itemに代入
                    elif non_extracted_item == '':
                        non_extracted_item = item
                result_items.append(non_extracted_item)

        def remove_parentheses_from_list(last):
            pattern = re.compile(r"\([^()]*\)")
            result = [pattern.sub("", string) for string in last]
            return result

        last_item = remove_parentheses_from_list(result_items)

        damage_table = []  # 空のリストを作成

    # ループで各要素を辞書型に変換し、空のリストに追加
        for i in range(len(first_item)):
            try:
                third = third_items[i]
            except IndexError:
                third = None
            
            # ['NON-a', '9月7日 S404', '9月7日 S537', '9月8日 S117,9月8日 S253']
            if len(last_item)-1 < i:
                break

            if isinstance(last_item[i], list):
                continue
            else:
                name_item = last_item[i].replace("S", "佐藤").replace("H", "濵田").replace(" ", "　")
            # name_item に格納されるのは 'NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253'のいずれかです。リストのi番目の文字列になります。

            dis_items = name_item.split(',') #「9月8日 S*/*117」,「9月8日 S*/*253」
            # コンマが付いていたら分割
            
            time_result = []
            current_date = ''  # 現在の日付を保持する変数
            for time_item in dis_items:
                # 先頭が数字で始まるかチェック（日付として扱えるか）
                if re.match(r'^\d', time_item):
                    current_date = re.match(r'^\d+月\d+日', time_item).group(0)  # 日付を更新
                    time_result.append(time_item)  # 日付がある項目はそのまま追加
                else:
                    # 日付がない項目は、現在の日付を先頭に追加
                    time_result.append(''.join([current_date, '　', time_item]))

            sub_dis_items = ['infra/static/infra/img/' + item + ".jpg" for item in time_result]
            # dis_itemsの要素の数だけ、分割した各文字の先頭に「infra/static/infra/img/」各文字の後ろに「.jpg」を追加
            # ['infra/static/infra/img/9月8日 S*/*117.jpg', 'infra/static/infra/img/9月8日 S*/*253.jpg']
            photo_paths = []
            # photo_pathsリストを作成
            for item in sub_dis_items:
                sub_photo_paths = glob.glob(item)
                photo_paths.extend(sub_photo_paths)
                # photo_pathsリストにsub_photo_pathsを追加
         
            if len(photo_paths) > 0:# photo_pathにはリストが入るため、[i]番目の要素が0より大きい場合
                picture_urls = [''.join(photo_path).replace('infra/static/', '') for photo_path in photo_paths]
                # photo_pathsの要素の数だけphoto_pathという変数に代入し、forループを実行
                # photo_pathという1つの要素の'infra/static/'を空白''に置換し、中間文字なしで結合する。
                # picture_urlsという新規配列に格納する。
            else:# それ以外の場合
                picture_urls = None
                #picture_urlsの値は[None]とする。
                
# << ◆写真メモを作成するコード◆ >>
            bridge_damage = [] # すべての"bridge"辞書を格納するリスト

            bridge = {
                "first": first_item[i],
                "second": second_items[i] if i < len(second_items) else None  # second_itemsが足りない場合にNoneを使用
            }
            bridge_damage.append(bridge)

            replacement_patterns = {
                "①腐食(小小)-b": "腐食", # 1
                "①腐食(小大)-c": "拡がりのある腐食",
                "①腐食(大小)-d": "板厚減少を伴う腐食",
                "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
                "⑥ひびわれ(小小)-b": "最大幅0.0mmのひびわれ", # 6
                "⑥ひびわれ(小大)-c": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
                "⑥ひびわれ(中小)-c": "最大幅0.0mmのひびわれ",
                "⑥ひびわれ(中大)-d": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
                "⑥ひびわれ(大小)-d": "最大幅0.0mmのひびわれ",
                "⑥ひびわれ(大大)-e": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
                "⑦剥離・鉄筋露出-c": "コンクリートの剥離", # 7
                "⑦剥離・鉄筋露出-d": "鉄筋露出",
                "⑦剥離・鉄筋露出-e": "断面減少を伴う鉄筋露出",
                "⑧漏水・遊離石灰-c": "漏水", # 8
                "⑧漏水・遊離石灰-d": "遊離石灰",
                "⑧漏水・遊離石灰-e": "著しい遊離石灰・泥や錆汁の混入を伴う漏水",
                "⑨抜け落ち-e": "コンクリート塊の抜け落ち", # 9
                "⑫うき-e": "コンクリートのうき", # 12
                "⑮舗装の異常-c": "最大幅0.0mmのひびわれ", # 15
                "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化",
                "⑳漏水・滞水-e": "漏水・滞水", # 20
                "㉓変形・欠損-c": "変形・欠損", # 23
                "㉓変形・欠損-e": "著しい変形・欠損",
                "㉔土砂詰まり-e": "土砂詰まり", # 24
            }

            pavement_items = []
            for damage_parts in bridge_damage:
                for damage_name_text in damage_parts:
                    pavement_items.append(str(damage_name_text))

                updated_second_items = []  # 更新されたsecond_itemsを格納するための新しいリスト

                for damage_number_items in second_items:#◆
                    if damage_number_items is None:#◆
                        updated_second_items.append(damage_number_items)#◆
                        continue

                    # '①'で始まる要素があるか確認
                    has_item_starting_with_1 = any(item.startswith('①') for item in damage_number_items)#◆

                    # '①'で始まる要素がある場合、'⑤'で始まる要素を削除
                    if has_item_starting_with_1:
                        updated_items = [damage_five_item for damage_five_item in damage_number_items if not damage_five_item.startswith('⑤')]#◆#★★★
                    else:
                        updated_items = damage_number_items.copy()  # items自体を直接変更しないためのコピー#◆

                    # '⑰'で始まる要素があるか確認
                    if any(seventeen_item.startswith('⑰') for seventeen_item in updated_items):#★★
                        new_sublist = []
                        # '⑰'で始まる要素がある場合、'⑰'のカッコ内の値のみ抽出
                        for inside_name_item in updated_items:#★
                            if inside_name_item.startswith('⑰'):#★
                                match = re.search(r'(?<=:)(.*?)(?=\)-e)', inside_name_item)#★
                                if match:
                                    new_sublist.append(match.group(1))
                                else:
                                    new_sublist.append(inside_name_item)  # マッチしなかった場合は元のアイテムを保持#★
                            else:
                                new_sublist.append(inside_name_item)  # '⑰'で始まらないアイテムはそのまま追加#★
                        updated_items = new_sublist  # 更新されたサブリストを反映

                    updated_second_items.append(updated_items)
                        

            # 処理結果を確認
            # first_itemとsecond_itemsを組み合わせて結果を表示する
            combined_list = []
            # second_itemsのリストが存在するか、またはNoneであるかをチェック
            combined_second = updated_second_items[i] if i < len(updated_second_items) else None
            
            # 組み合わせをリストに追加
            combined = {"first": first_item[i], "second": combined_second}
            combined_list.append(combined)

            # 結果の印刷
            for first_second_joinitem in combined_list:#★
                # item['first']のスペースまでの文字を抽出
                first_part = ""
                clean_text = str(first_second_joinitem['first']).replace("</br>", "")#★
                if "," in clean_text:
                    pattern = ',(\d|,)*(?=\s|$)' # 「,」の後に(「数字」か「,」)の場合
                    # 条件に一致するかチェック
                    if re.search(pattern, clean_text):
                        first_part = clean_text.split(" ")[0]
                    else:
                        sub_pattern = r'[A-Za-z0-9/ /]'
                        # 置換処理を行い、日本語のみ抽出
                        result = re.sub(sub_pattern, '', clean_text)
                        first_part = result  # 数字、アルファベット、コンマを削除
                else:
                    first_part = clean_text.split(" ")[0]
                
                # item['second']を置換
                second_parts = []
                if first_second_joinitem['second'] is not None:#★
                    for element in first_second_joinitem['second']:#★
                        if element in replacement_patterns:
                            second_parts.append(replacement_patterns[element])
                        else:
                            second_parts.append(element)
                
                # second_partsが複数要素を持つ可能性も考えられるので、','.join()で文字列に変換
                second_part_joined = ', '.join(second_parts)
                
                # 結果の表示
                if first_second_joinitem['second'] == None: # 損傷種類がNoneのとき
                    combined_data = None
                elif len(second_items[i]) == 1:
                    combined_data = f"{first_part}に{second_part_joined}が見られる。"
                else:
                    item_str = ', '.join(second_items[i]) # ['①腐食-b']を①腐食-bに変更
                    start_special_text = item_str.find(",")+1 # 最初のコンマ位置を検索
                    combined_data = f"{first_part}に{second_part_joined}が見られる。\n【関連損傷】\n{item_str[start_special_text:]}"
                    # \n文字列のときの改行文字
                items = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/noImage.png', 'textarea_content': combined_data, 'damage_coordinate': damage_coordinate[i], 'picture_coordinate': picture_coordinate[i]}
                # {'first': Markup('排水管 Dp0102'), 'second': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e'], 'third': '写真番号-32', /
                # 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070486.JPG'], 'picture': 'infra/noImage.png', /
                # 'textarea_content': '排水管に拡がりのある腐食が見られる。\n【関連損傷】\n ⑤防食機能の劣化(分類1)-e', /
                # 'damage_coordinate': ['547059.1990495767', '229268.8593029478'], /
                # 'picture_coordinate': ['549204.9604817769', '229256.3408485695']}

                #優先順位の指定
                order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
                order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
                order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
                        
                def sort_category(text): # sort_category関数を定義
                    # ',' でテキストを分割し、最初の部分のみを考慮する
                    first_part = text.split(',')[0]
                    for key, val in order_dict.items(): # keyがキー(主桁～防護柵)、valが値(1～6)
                        if first_part.startswith(key): # textの1文字目がキー(主桁～防護柵)の場合
                            return val # 値(1～6)を返す
                    return max(order_dict.values()) + 1
                
                def extract_numbers(s):
                    # 文字列から数値部分だけを抽出してリストに格納する
                    return [int(''.join(filter(str.isdigit, part))) for part in s.split(',') if ''.join(filter(str.isdigit, part))]

                def get_first_key(first):
                    num_parts = extract_numbers(first)
                    # 数値が含まれていない場合は、ソートで最後になるような大きな値を返す
                    return min(num_parts) if num_parts else float('inf')

                def sort_number(second_list):
                    # リストが空の場合の処理
                    if not second_list or len(second_list) == 0:  # 条件式の調整
                        return max(order_number.values()) + 1
                    else:
                        second_text = second_list[0]
                        if "-" in second_text: #second_textの文字の中に-があるとき
                            num_text = second_text[0] #num_textにsecond_textの1文字目を入れる
                            for key, val in order_number.items():
                                if num_text.startswith(key):
                                    return val #数字を返す
                    return max(order_number.values()) + 1 #リストの最大数+1の数字を返す

                def sort_lank(second_list):
                    if not second_list or len(second_list) == 0:  # 条件式の調整
                        return max(order_number.values()) + 1
                    else:
                        second_text = second_list[0]
                        if '-' in second_text:
                            lank_text = second_text.split("-")[1]
                            for key, val in order_lank.items():
                                if lank_text.startswith(key):
                                    return val
                        return max(order_lank.values()) + 1

                damage_table.append(items)
        sorted_text_list = sorted(damage_table, key=lambda text: (sort_category(text['first']), get_first_key(text['first']), sort_number(text['second']), sort_lank(text['second'])))
    # sorted(並び替えるオブジェクト, lamda式(無名関数)で並び替え 各要素: (text[0]で始まる要素を並び替え、その中でtext[0]の並び替え))

    context = {'damage_table': sorted_text_list}  # テンプレートに渡すデータ
    print(sorted_text_list) # sorted_text_list（itemsの内容を並び替え）をすべて表示
    return render(request, 'table.html', context)

def ajax_file_send(request):
    if request.method == 'POST': # HTTPリクエストがPOSTメソッドかつ
        if 'upload-file' in request.FILES: # アップロードされたファイルがrequest.FILESに入っている場合
            myfile = request.FILES['upload-file'] # 受け取ったファイルをmyfileという変数に代入
            fs = FileSystemStorage() # FileSystemStorageのインスタンスを生成(システム上にファイルを保存する準備)
            filename = fs.save(myfile.name, myfile) # myfileを指定した名前で保存し、保存したファイルの名前をfilename変数に格納
            uploaded_file_url = fs.url(filename) # 保存したファイルにアクセスするためのURLを生成
            # success時のレスポンスはJSON形式で返すならこちらを使う
            return JsonResponse({'upload_file_url': uploaded_file_url})
            # HTMLページを返す場合はこちらを使う
            # context = {'damage_table': sorted_text_list}
            # return render(request, 'table.html', context)
        else:
            # ファイルがPOSTされていない場合はエラーレスポンスを返す
            return HttpResponseBadRequest('添付ファイルが見つかりませんでした。') # File is not attached
    else:
        # POSTメソッドでない場合はエラーレスポンスを返す
        return HttpResponseBadRequest('無効な作業です。') # Invalid request method

# 番号表示
def sample_view(request):# 追加
    start = "0101"
    end = "0206"

# 最初の2桁と最後の2桁を取得
    start_prefix = start[:2]
    start_suffix = start[2:]
    end_prefix = end[:2]
    end_suffix = end[2:]

# 抽出した数字を表示
    result = ""# 追加
    for prefix in range(int(start_prefix), int(end_prefix)+1):
        for suffix in range(int(start_suffix), int(end_suffix)+1):
            result += "{:02d}{:02d}".format(prefix, suffix)
        
    return HttpResponse(result)# 追加

# <<ファイルアップロード(プライマリーキーで分類分け)>>
def upload_directory_path(instance, filename):
    # プライマリーキーを取得する
    primary_key = instance.pk
    # 'documents/プライマリーキー/filename' のパスを返す
    return 'uploads/{}/{}'.format(primary_key, filename)

class Upload(models.Model):
    file = models.FileField(upload_to=upload_directory_path)
    
# <<センサス調査>>
def census_view(request):
    form = CensusForm()
    return render(request, 'infra_detail.html', {'form': form})

# <<全景写真の表示>>
def image_list(request):
    # 特定のディレクトリ内の全てのファイルパスをリストで取得したい場合はglobを使うと良い。
    save_path = r"C:\work\django\myproject\program\Infraproject\infra\static\infra\img"
    files_jpg = glob.glob(save_path + "\*.jpg")
    files_png = glob.glob(save_path + "\*.png")
    files = files_jpg + files_png  # 2つのリストを結合する。
    # ページに表示する際、"infra/static/" を削除する。

    web_base_path = "infra/img/"  # ウェブからアクセスする際のベースパス

    image_files = []
    for file_path in files:
        # OSの絶対パスからウェブアクセス可能な相対パスへ変換
        relative_path = file_path.replace(save_path, web_base_path).replace("\\", "/")
        image_files.append(relative_path)
    # テンプレートに画像ファイルの一覧を渡してレンダリングする
    return render(request, 'image_list.html', {'image_files': image_files})

# <<全景写真アップロード>>
save_path = r"C:\work\django\myproject\program\Infraproject\infra\static\infra\img"
def display_photo(request):
    print("リクエストメソッド:", request.method)  # リクエストのメソッドを表示
    if request.method == 'POST': # HTTPリクエストがPOSTメソッド(フォームの送信など)であれば、以下のコードを実行
        form = UploadForm(request.POST, request.FILES) # UploadFormを使用して、送信されたデータ(request.POST)とファイル(request.FILES)を取得
        print("フォームが有効か？:", form.is_valid())  # フォームの有効性を表示
        if form.is_valid(): # formのis_valid()メソッドを呼び出して、フォームのバリデーション(検証)を実行
    # フォームが有効な場合は、選択された写真を特定のフォルダに保存します
            # print("フォームが有効")
            photo = form.cleaned_data['photo'] # バリデーションを通過したデータから、'photo'キーに対応するデータを取得しphoto変数に格納
            print("アップロードされた写真の名前:", photo.name)  # アップロードされた写真の名前を表示
            file_name = photo.name  # アップロードされたファイルの名前をfile_name変数に格納
            file_path = os.path.join(save_path, file_name)
            #設定された保存パス（save_path）とファイル名（file_name）を組み合わせ、フルパスをfile_path変数に格納

            with open(file_path, 'wb') as f: # file_pathで指定されたパスにファイルをバイナリ書き込みモード('wb')で開く
                for chunk in photo.chunks(): # アップロードされたファイル(photo)をchunks()メソッドを使用して分割し、ループ処理を行う
                    f.write(chunk) # 各チャンクを開かれたファイル(f)に書き込む
            return redirect('image_list')
        else:
            print("フォームエラー:", form.errors)  # フォームのエラーを表示
        # フォームが有効・無効 共通
            print(form.errors)  # コンソールにエラーメッセージを出力
            return HttpResponseBadRequest('添付ファイルが見つかりませんでした。 エラー: {}'.format(form.errors))
            #return HttpResponseBadRequest('添付ファイルが見つかりませんでした。')
    else:
        form = UploadForm() # Forms.pyの「UploadForm」を呼び出し
    return render(request, 'upload_photo.html', {'form': form})

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'image_list.html', {'form': form})

# <<全景写真の変更>>
def change_photo(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # ここで、古い写真の削除や新しい写真の保存処理を行います。
            # 例: image_idを使用して特定のレコードを探し、そのレコードに新しい画像を保存
            image_id = request.POST.get('image_id', None)  # 画像ID取得
            if image_id:
                image_instance = UploadForm.objects.get(id=image_id)
                image_instance.photo = form.cleaned_data['photo']
                image_instance.save()
                return redirect('image_list')
            else:
                # エラー処理
                pass
        else:
            # フォームのバリデーションに失敗したときの処理
            pass
    else:
        form = UploadForm()  # GETリクエストの場合、空のフォームを表示

    return render(request, 'upload_photo.html', {'form': form})

# 番号図用
def number_create_view(request): # number_create_view関数を定義
# この行ではnumber_create_viewという名前の関数を定義しています。この関数はrequestという引数を受け取ります。
# requestはユーザーからのHTTPリクエストを表し、Djangoが自動的に関数に渡します。
    if request.method == 'POST': # HTTPリクエストメソッドがPOSTメソッド(データをサーバーに送る役割)の場合
        form = NumberForm(request.POST) # 

        if form.is_valid(): # POSTメソッドがform.pyで定めたfieldsに従っている場合
            form.save() # DBに保存する。
        else:
            print(form.errors) # エラーの理由を出す。

        return redirect('/') # 
    else:
        form = NumberForm() # GETリクエストの場合、空のフォームを表示します。

    return render(request, 'select_item.html', {'form': form})

# << 所見一覧 >>
def opinion_view(request):
    return render(request, 'opinion.html')

# << 橋梁緒言の選択肢 >>
def infraregulations_view(request):
    form = BridgeCreateForm()
    regulations = Regulation.objects.all()
    context = {
        'form': form,
        'regulations': regulations,
    }
    return render(request, 'infra_create.html', context)

def infraloadWeights_view(request):
    form = BridgeCreateForm()
    loadWeights = LoadWeight.objects.all()
    context = {
        'form': form,
        'loadWeights': loadWeights,
    }
    return render(request, 'infra_create.html', context)

def infraloadGrades_view(request):
    form = BridgeCreateForm()
    loadGrades = LoadGrade.objects.all()
    context = {
        'form': form,
        'loadGrades': loadGrades,
    }
    return render(request, 'infra_create.html', context)

def infrarulebooks_view(request):
    form = BridgeCreateForm()
    rulebooks = Rulebook.objects.all()
    context = {
        'form': form,
        'rulebooks': rulebooks,
    }
    return render(request, 'infra_create.html', context)

def infraapproachs_view(request):
    form = BridgeCreateForm()
    approachs = Approach.objects.all()
    context = {
        'form': form,
        'approachs': approachs,
    }
    return render(request, 'infra_create.html', context)

def infrathirdpartys_view(request):
    form = BridgeCreateForm()
    thirdpartys = Thirdparty.objects.all()
    context = {
        'form': form,
        'thirdpartys': thirdpartys,
    }
    return render(request, 'infra_create.html', context)

def infraunderConditions_view(request):
    form = BridgeCreateForm()
    underConditions = UnderCondition.objects.all()
    context = {
        'form': form,
        'underConditions': underConditions,
    }
    return render(request, 'infra_create.html', context)

def infraregulations_view(request):
    form = BridgeUpdateForm()
    regulations = Regulation.objects.all()
    context = {
        'form': form,
        'regulations': regulations,
    }
    return render(request, 'infra_update.html', context)

def infraloadWeights_view(request):
    form = BridgeUpdateForm()
    loadWeights = LoadWeight.objects.all()
    context = {
        'form': form,
        'loadWeights': loadWeights,
    }
    return render(request, 'infra_update.html', context)

def infraloadGrades_view(request):
    form = BridgeUpdateForm()
    loadGrades = LoadGrade.objects.all()
    context = {
        'form': form,
        'loadGrades': loadGrades,
    }
    return render(request, 'infra_update.html', context)

def infrarulebooks_view(request):
    form = BridgeUpdateForm()
    rulebooks = Rulebook.objects.all()
    context = {
        'form': form,
        'rulebooks': rulebooks,
    }
    return render(request, 'infra_update.html', context)

def infraapproachs_view(request):
    form = BridgeUpdateForm()
    approachs = Approach.objects.all()
    context = {
        'form': form,
        'approachs': approachs,
    }
    return render(request, 'infra_update.html', context)

def infrathirdpartys_view(request):
    form = BridgeUpdateForm()
    thirdpartys = Thirdparty.objects.all()
    context = {
        'form': form,
        'thirdpartys': thirdpartys,
    }
    return render(request, 'infra_update.html', context)

def infraunderConditions_view(request):
    form = BridgeUpdateForm()
    underConditions = UnderCondition.objects.all()
    context = {
        'form': form,
        'underConditions': underConditions,
    }
    return render(request, 'infra_update.html', context)