** 構成
Data/							元データ
 - traces_TK.csv				疑似人流データから抽出した東京（緯度:35.65-35.75, 経度:139.68-139.8）のトレース
 - regions_TK.csv				東京のregion情報
 - traintraces_TK.csv			学習用トレース（サンプル）
 - testtraces_TK.csv			評価用トレース（サンプル）

Data_Anonymized/				匿名加工データ（シャッフル前）

Data_Anonymized_Shuffled/		匿名加工データ（シャッフル後）

ExtractData_from_PF/			疑似人流データからデータを抽出するプログラム
 - Read_PF.py					疑似人流データから東京（緯度:35.65-35.75, 経度:139.68-139.8）のトレースを抽出する
 - MakeTrainTestData_PF.py		Read_PF.pyで抽出したトレースから，学習用・評価トレースを作成する

SmlProg_Anonymize/				匿名加工サンプルプログラム
 - A1-none.py					評価用トレースをそのまま出力する（何もしない）
 - A2-MRLH.py					MRLH (Merging Regions and Location Hiding) [Shokri+,S&P11]
 - A3-kRR.py					k-RR (k-ary randomized response) [Kairouz+,ICML16]
 - A4-PL.py						PL (Planaer Laplace mechanism) [Andres+,CCS13]【TBD】

SmlProg_Localize/				属性推定（Localization）サンプルプログラム【属性推定することが決定後，作成予定】
 - L1-rand.py					ランダム推定【TBD】
 - L2-TransML-Viterbi.py		最尤推定で遷移行列を学習し，Viterbiアルゴリズムにより属性推定する [Shokri+,S&P11]【TBD】

SmlProg_Reidentify/				再識別（Reidentify）サンプルプログラム【再識別することが決定後，作成予定】
 - R1-rand.py					ランダム識別【TBD】
 - R2-TransML-Bayes.py			最尤推定で遷移行列を学習し，ベイズ決定則により再識別する [Murakami+,TrustCom15]【TBD】

ShuffleIDs.py					指定したディレクトリ下の全匿名加工データに対して，ユーザIDをシャッフルするプログラム

EvalSecurity.py					安全性スコア評価プログラム【TBD】

EvalUtility.py					有用性スコア評価プログラム【TBD】

Eval.bat						一気通貫で各サンプルプログラムの有用性・安全性スコアを評価するプログラム【TBD】


## 実行
- python3.6以上の環境？で、環境に合わせてEval.bashの中身を変えてから実行すればいい
- numpyだけ必要

```bash
pip install -r requirements.txt
bash Eval.bash
```
