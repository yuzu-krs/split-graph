# CSVファイルからグラフを自動生成

これは，**csvファイル**を分割し,グラフを生成するデスクトップアプリになります.
グラフの**平均**やグラフの**比較**を自動で行えます．

## **デモ** 
今回は10回分の平均のグラフを描画します．
2つのcsvファイルから比較グラフを作成していきます．

1. 実行結果をcsvファイルで出力します(ファイル名は任意)．
- csvファイルの1行目は y,x にしてください．
- 例えば，秒数とNの値のグラフを描画したいときは yに秒数 xにNの値
- 以下のような形式にしてください．(yが0,100,200,・・・,9900)×10行(10回分の平均のグラフのため)
- test1.csv
https://github.com/yuzu-krs/split-graph/issues/1#issue-2244567542
- test2.csv
https://github.com/yuzu-krs/split-graph/issues/2#issue-2244590793

<br>

2. サーバからローカルに2つのcsvファイルをダウンロードします．


<br>


3. デスクトップアプリをダウンロードする
https://github.com/yuzu-krs/split-graph/blob/main/auto-split-plot.zip
<br>

4. 先ほどのcsvファイルをダウンロードしたディレクトリに解凍したsplit-graph.exeを実行してください．

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/9c8c011a-c75c-4cce-91c1-33a81b6adb20)
<br>
5. サーバからダウンロードしたcsvファイルを分割しますので1を入力 
※分割は，y,xのxの最初の値で区切られます．xの次の行が0ならば0で分割,64なら次の64が来るまで分割される．

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/f366ec00-d586-4603-9f75-468cc7dba705)
<br>

6. csvファイルを選択してください

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/f34dcb6d-5f89-4ff7-92b8-5552129f9b41)
<br>

7. フォルダ名を入力してください(グラフの名前になるので注意)

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/3f8ae5e2-c773-4d05-9b31-0c0cfcfdeb64)
<br>

8. test1のフォルダが生成され，10回分に分割された．

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/d8e58034-77a9-4487-a99e-930fae7a2372)
<br>

9. test2.csvも同じように分割してください．

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/8d6c80fb-5ecb-4b04-a019-c27d2257582a)
<br>

10. データがそろったのでグラフを作成する．

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/914bb0d8-e2e7-4cf2-bee4-2e36b323b959)
<br>

11. 2つのグラフを比較するので2

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/91934894-aba9-433e-b124-a8aa5acacba1)
<br>

12. 2つのフォルダを選択する(選択したそれぞれのフォルダの配下のcsvファイルの平均がグラフとしてプロットされる)

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/55ab642f-2d77-467e-9e4e-7f82c10ec3ef)
<br>

13. x,y,タイトルの名前を入力する

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/8f0195a3-40a1-4490-b2f3-49cd8bb02c79)

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/3eb5cd93-7ccb-4137-9616-d73cda63afe8)

![image](https://github.com/yuzu-krs/split-graph/assets/89998242/3ed1ea5d-fd1c-48dd-87d0-d27df2e19bbc)
<br>

14. 完成
![image](https://github.com/yuzu-krs/split-graph/assets/89998242/95fd3fdb-e113-4fdb-8f87-d56e02201bbe)





