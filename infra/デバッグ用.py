# 指定したInfra(pk)に紐づくTableのエクセル出力処理をする。 
def data_output(request, article_pk, pk):
    # 指定したInfraに紐づく Tableを取り出す
    table = Table.objects.filter(infra=pk).first()
    print(table.dxf.url) # 相対パス
    
    # 絶対パスに変換
    encoded_url_path = table.dxf.url
    decoded_url_path = urllib.parse.unquote(encoded_url_path) # URLデコード
    dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
    print(dxf_filename)
#         ↑ を読んでエクセルファイルを作る
    
    # TODO: エクセルファイルを新規作成するが、 既存のファイルを読み込む方向で修正。
    wb  = px.Workbook()


    # 径間の数だけシートを作る。
    infra   = Infra.objects.filter(id=pk).first()
    amount  = infra.径間数

    for number in range(1,amount+1):

        # TODO: ↓ 後でクライアント側から指定できるようにする。
        search_title_text           = f"{number}径間"
        second_search_title_text    = "損傷図"

        # 1回の実行で作れるのは、径間の1個分しか作れない。エクセルのシート1枚。
        sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)



    # TODO: できあがったエクセルファイルをレスポンスする

    #メモリ空間内に保存
    virtual     = BytesIO()
    wb.save(virtual)

    #バイト文字列からバイナリを作る
    binary      = BytesIO(virtual.getvalue())

    #レスポンスをする
    return FileResponse( binary, filename="download.xlsx" )