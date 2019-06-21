## 構成

Data/							元データ
 - regions_TK.csv				東京のregion情報
 - traintraces_TK.csv			学習用トレース（サンプル）
 - testtraces_TK.csv			評価用トレース（サンプル）

Data_Anonymized/				匿名加工データ（シャッフル前）

Data_Anonymized_Shuffled/		匿名加工データ（シャッフル後）

ExtractData_from_PF/			疑似人流データからデータを抽出するプログラム
 - Read_PF.py					疑似人流データから東京（緯度:35.65-35.75, 経度:139.68-139.8）のトレースを抽出する
 - MakeTrainTestData_PF.py		Read_PF.pyで抽出したトレースから，学習用・評価トレースを作成する

SmplProg_Anonymize/				匿名加工サンプルプログラム
 - A1-none.py					評価用トレースをそのまま出力する（何もしない）
 - A2-MRLH.py					MRLH (Merging Regions and Location Hiding) [Shokri+,S&P11]
 - A3-kRR.py					k-RR (k-ary randomized response) [Kairouz+,ICML16]
 - A4-PL.py						PL (Planaer Laplace mechanism) [Andres+,CCS13]
 - A5-YA.py						Yamaoka anonymization (cheating anonymization)

SmplProg_Reidentify/			再識別（Reidentification Attack）サンプルプログラム
 - R1-rand.py					ランダム識別
 - R2-VisitProb.py				ユーザ毎の領域滞在分布を学習し，最も事後確率の大きいユーザとして再識別する

SmplProg_Track/					属性推定（Tracking Attack）サンプルプログラム
 - T1-rand.py					ランダム推定
 - T2-VisitProb.py				ユーザ毎の領域滞在分布を学習し，最も事後確率の大きい領域として属性推定する

SmplResults/					サンプルプログラムの実験結果ファイル（EvalAll.pyを実行して得られたファイル）
 - results_test.xlsx			評価用トレースを学習用に指定したときの実験結果（最大知識モデルに相当）
 - results_train.xlsx			学習用トレースを学習用に指定したときの実験結果（部分知識モデルに相当）

ShuffleIDs.py					指定したディレクトリ下の全匿名加工データに対して，ユーザIDをシャッフルするプログラム

EvalSecR.py						安全性スコア（再識別）評価プログラム

EvalSecT.py						安全性スコア（属性推定）評価プログラム

EvalUtil.py						有用性スコア評価プログラム

EvalAll.py						一気通貫で各サンプルプログラムの有用性・安全性スコアを評価するプログラム

Eval.bash						匿名加工とシャッフルを行うプログラム（old version）

## 実行
- python3.6以上の環境？で、環境に合わせてEvalUtil.pyの中身を変えてから実行すればいい
- numpy, scipyだけ必要

```bash
pip install -r requirements.txt
python EvalAll.py
```
