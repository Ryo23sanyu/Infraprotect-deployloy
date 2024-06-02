import glob, re, sys 

## 引数の指定がある場合: 特定のアプリのmodels.pyに対して実行する。
## 引数の指定が無い場合: プロジェクトの全アプリのmodels.pyに対して実行する。

if len(sys.argv) > 1:
    models_paths    = glob.glob(f"./{sys.argv[1]}/models.py")
else:
    models_paths    = glob.glob("./*/models.py")

forms_paths     = [ models_path.replace("models", "forms") for models_path in models_paths ]

# すべてのmodels.pyを順次読み込み
for models_path,forms_path in zip(models_paths, forms_paths):

    #====forms.pyの冒頭===========================

    with open(models_path, "r") as mf:

        # models.pyを文字列で読み込み
        models_code     = mf.read()
        model_classes   = re.findall(r'class (\w+)\(models\.Model\):', models_code)

        # forms.pyのimport部を作成
        import_models   = ""
        for model_class in model_classes:
            import_models += f"{model_class},"

        import_models   = import_models.rstrip(",")


        # forms.pyのコードを作る。
        forms_code      = [ "# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #\n"]
        forms_code.append( f"from django import forms\nfrom .models import {import_models}\n" )

    #====forms.pyの冒頭===========================

    #====forms.pyの本体===========================

    with open(models_path, "r") as mf:

        # models.pyをリストで読みこみ
        models_codes    = mf.readlines()
        fields_list     = []

        for models_code in models_codes:
            print(models_code)

            # モデルクラス名を取得
            model_name  = re.search(r'class (\w+)\(models\.Model\):', models_code)
            if model_name:

                # バリデーション対象のフィールドがあれば追加。
                if fields_list:
                    forms_code.append(f"        fields\t= " + str(fields_list) + "\n")
                    fields_list = []

                # モデルクラス名を元に、フォームクラスを作る。
                forms_code.append( f"class {model_name.group(1)}Form(forms.ModelForm):")
                forms_code.append( "    class Meta:" )
                forms_code.append( f"        model\t= {model_name.group(1)}" )

            # モデルフィールド名を取得
            field_name = re.search(r'(\w+).*=\s*models\.', models_code)
            if field_name:
                fields_list.append(field_name.group(1))


        # バリデーション対象のフィールドがあれば追加。
        if fields_list:
            forms_code.append(f"        fields\t= " + str(fields_list) + "\n")
            fields_list = []

        # === 軽微な調整 ===
        # 'を"に
        forms_code  = [ c.replace("'", "\"") for c in forms_code]
        forms_code  = [ c.replace("[", "[ ") for c in forms_code]
        forms_code  = [ c.replace("]", " ]") for c in forms_code]

        # === 軽微な調整 ===

        # 書き込みするコード
        for c in forms_code:
            print(c)

    #====forms.pyの本体===========================

    #====対応するforms.pyへ保存===================

    # 書き込みするコード
    with open(forms_path, "a") as ff:
        for code in forms_code:
            ff.write(code + "\n")

    #====対応するforms.pyへ保存===================