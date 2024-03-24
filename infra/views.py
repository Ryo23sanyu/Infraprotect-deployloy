import glob
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from markupsafe import Markup
import pandas as pd
from .models import Infra
from .models import Article
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FileUploadForm, UploadForm
from .forms import PhotoUploadForm, NameForm
from .models import Photo, Panorama
import os
from django.contrib.auth.decorators import login_required
import ezdxf
from ezdxf.entities.mtext import MText
import tkinter
import tkinter.filedialog
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
    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["pk"]
        return super().get_context_data(**kwargs)
  
class CreateInfraView(LoginRequiredMixin, CreateView):
  template_name = 'infra/infra_create.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員','橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー', 'article')
  success_url = reverse_lazy('detail-infra')
  # def get_success_url(self):
    # return reverse_lazy('detail-infra', kwargs={'pk': self.kwargs["pk"]})
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

class DeleteInfraView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/infra_delete.html'
  model = Infra
  success_url = reverse_lazy('list-infra')
  
class UpdateInfraView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/infra_update.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー', 'article')
  success_url = reverse_lazy('detail-infra')
  def get_success_url(self):
    return reverse_lazy('detail-infra', kwargs={'pk': self.kwargs["pk"]})
  
def infra_view(request):
  if request.method == 'POST':
    等級 = request.POST.get('等級', None)
    # load_gradeを使って必要な処理を行う
    # 例えば、選択されたload_gradeに基づいてデータをフィルタリングして表示するなど

  # 通常のビューロジック
  # ・・・
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

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'image_list.html', {'form': form})

def selected_photos(request):
    selected_photo_ids = request.POST.getlist('selected_photos')
    selected_photos = Photo.objects.filter(id__in=selected_photo_ids)
    return render(request, 'infra/selected_photos.html', {'selected_photos': selected_photos})
  
# <<写真の表示>>
  
def image_list(request):
   
    # 特定のディレクトリ内の全てのファイルパスをリストで取得したい場合はglobを使うと良い。    
    import glob

    files = glob.glob( "infra/static/infra/img/*.jpg" )

    # ページに表示する際、"infra/static/" を削除する。
    image_files = []
    for file in files:
        image_files.append( file.replace("infra/static/", "") )

    # テンプレートに画像ファイルの一覧を渡してレンダリングする
    return render(request, 'image_list.html', {'image_files': image_files})

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
        selected_ids = request.POST.getlist('selected_panoramas')
        for panorama in panoramas:
            if str(panorama.id) in selected_ids:
                panorama.checked = True
            else:
                panorama.checked = False
            panorama.save()
        return redirect('panorama_list')  # 再描画のためにリダイレクト

    return render(request, 'image_list.html', {'panoramas': panoramas})



def panorama_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        checked = request.POST.get('checked', False)
        panorama = Panorama.objects.create(image=image, checked=checked)
        return redirect('panorama_list')
    return render(request, 'panorama_upload.html')
   
# 番号表示  
  
from django.http import HttpResponse

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

    def extract_text(filename):
        doc = ezdxf.readfile(filename)
        msp = doc.modelspace()
        
        extracted_text = []
        for entity in msp:
            if entity.dxftype() == 'MTEXT':
                if entity.dxf.layer != 'Defpoints':
                # MTextのテキストを抽出する
                    text = entity.plain_text()
                    cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
                    if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
                # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                        related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
                # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                        for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                        # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                            if entity_extension(entity, neighbor):
                            # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                                related_text = neighbor.plain_text()
                            #extracted_text.append(neighbor_text)
                                break # 文字列が見つかったらbreakにょりforループを終了する

                        if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                            cad_data.append(related_text) # 見つかった文字列を追加する
                    #最後にまとめてcad_dataをextracted_textに追加する
                        extracted_text.append(cad_data)
        
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



    # AutoCADファイル名を指定してテキストを抽出する
    filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf'
    extracted_text = extract_text(filename)

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

    # 先頭の要素を抽出
        top_item = [sub_list[0] for sub_list in extracted_text]
        
        new_text = []
        for item in top_item:
            if "," in item:
                for j in range(len(item)-1):
                    if item[j] == "," and item[j+1].isnumeric():
                        for s in range(len(item)-1):
                            if item[s].isalpha() and item[s+1].isnumeric():
                                new_text.append(item[:item.find(",")+1] + item[:s+1] + item[item.find(",")+1:])
                                break
            else:
                new_text.append(item)
                
        first_item = [Markup(sub_list[0].replace(",", "<br /><br />")) for sub_list in extracted_text]

    # リストの各要素から記号を削除する
        def remove_symbols(other_items):
            symbols = ['!', '[', ']', "'"]

            processed_other_items = []
            for item in other_items:
                processed_item = ''.join(c for c in item if c not in symbols)
                processed_other_items.append(processed_item)
    
            return processed_other_items
    # それ以外の要素を抽出
        other_items = [sub_list[1:-2] for sub_list in extracted_text]          
        second_items = remove_symbols(other_items)

    # 最後から2番目の要素を抽出（写真番号-00）
        third_items = [sub_list[-2] for sub_list in extracted_text if len(sub_list) >= 3]
        
    # 最後の要素を抽出（Defpoints）
        bottom_item = [sub_list[-1] for sub_list in extracted_text]

        damage_table = []  # 空のリストを作成

    # ループで各要素を辞書型に変換し、空のリストに追加
        for i in range(len(first_item)):
            try:
                third = third_items[i]
            except IndexError:
                third = None
            
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

            last = result_items
            # ['NON-a', '9月7日 S404(前-1)', '9月7日 S537', '9月8日 S117(前-3),9月8日 S253']
            last_item = remove_parentheses_from_list(last)
            # ['NON-a', '9月7日 S404', '9月7日 S537', '9月8日 S117,9月8日 S253']
            name_item = last_item[i].replace("S", "佐藤").replace("H", "濵田").replace(" ", "　")
            # ['NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253']

            target_file = name_item[i]
            # target_fileにname_itemの[i]番目の要素を代入
            dis_items = target_file.split(',') #「9月8日 S*/*117」,「9月8日 S*/*253」
            # コンマが付いていたら分割
            sub_dis_items = ['infra/static/infra/img/' + item + ".jpg" for item in dis_items]
            # dis_itemsの要素の数だけ、分割した各文字の先頭に「infra/static/infra/img/」各文字の後ろに「.jpg」を追加
            # ['infra/static/infra/img/9月8日 S*/*117.jpg', 'infra/static/infra/img/9月8日 S*/*253.jpg']
            for item in sub_dis_items:
                sub_photo_paths = glob.glob(item)
                # ワイルドカードを含んだ検索ができるようにする
            join_dis_items = ",".join(sub_photo_paths)
            # globの後に文字の結合
            photo_paths = join_dis_items
         
            if len(photo_paths) > 0:# photo_pathにはリストが入るため、[i]番目の要素が0より大きい場合
                picture_urls = [''.join(photo_path).replace('infra/static/', '') for photo_path in photo_paths]
                # photo_pathsの要素の数だけphoto_pathという変数に代入し、forループを実行
                # photo_pathという1つの要素の'infra/static/'を空白''に置換し、中間文字なしで結合する。
                # picture_urlsという新規配列に格納する。
            else:# それ以外の場合
                picture_urls = None
                #picture_urlsの値は[None]とする。

            item = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/img/noImage.png'}
            damage_table.append(item)

    context = {'damage_table': damage_table}  # テンプレートに渡すデータ
    return render(request, 'table.html', context)

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

# <<写真表示>>
save_path = "C:\work\django\myproject\myvenv\Infraproject\infra\static\infra\img"
def display_photo(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
    # フォームが有効な場合は、選択された写真を特定のフォルダに保存します
            photo = form.cleaned_data['photo']
            file_name = photo.name  # 写真のファイル名を取得します
            file_path = os.path.join(save_path, file_name)  # ファイルの保存先のパスを作成します

            with open(file_path, 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)  # 写真のデータをファイルに書き込みます

        return render(request, 'image_list.html', {'photo': photo})
    else:
        form = UploadForm()
    return render(request, 'upload_photo.html', {'form': form})

