## このレポジトリは
位置情報のデータ，サンプルプログラム（匿名化・ID識別・トレース推定），シャッフル（仮名化），有用性・安全性評価アルゴリズムのコードを管理しています
詳しくは、[PWSCUP Slack](https://join.slack.com/t/pwscup/shared_invite/enQtNjIwMjQ4OTgzOTU1LTY4NTA2Y2RiZTA1M2E1MDdhYjg4YjY1MTY3OTFmODdiMTI3NmQxNTBjZjkyZjlkZjEzNzA1OGZjYTA4NTM3Y2I)で！


## 実行
- python3.6以上の環境？であれば動きます
  - 必要なパッケージを``` pip install ``` しましょう
  - Eval.bash, EvalAll.pyでサンプルプログラムを用いた匿名加工・ID識別・トレース推定ができます．詳細は以下のとおり．
  - Eval.bash: 大阪データセットの元トレース（チーム番号：001，データセット番号：01）に対して，以下の匿名加工・ID識別・トレース推定を行う．
    - 匿名加工アルゴリズム：A2-MRLH
    - ID識別アルゴリズム：I1-rand
    - トレース推定アルゴリズム：T1-rand
  - EvalAll.py: 大阪データセットの元トレース（チーム番号：001，データセット番号：01）に対して，以下の全匿名加工・全ID識別・全トレース推定アルゴリズムを走らせる（30分程度かかかるので注意）．
    - 匿名加工アルゴリズム：A1-none, A2-MRLH, A3-kRR, A4-PL, A5-YA
    - ID識別アルゴリズム：I1-rand, I2-VisitProb, I3-HomeProb
    - トレース推定アルゴリズム：T1-rand, T2-VisitProb, T3-HomeProb

```bash
pip install -r requirements.txt
bash Eval.bash
python EvalAll.py
```

## 構成
- README.md
  - このファイル

- Data/                   元データ
  - PeopleFlow/           疑似人流データから抽出したデータセット
    - POI_TK.csv            東京のPOI情報（POI ID, 緯度，経度，カテゴリーなど）
    - POI_TK_readme.txt     東京のPOI情報の説明
    - regions_TK.csv				東京の領域情報（領域ID，縦軸ID，横軸ID，中心部の緯度，中心部の経度，病院フラグ）
    - traintraces_TK.csv		学習用トレース（サンプル）
    - testtraces_TK.csv			評価用トレース（サンプル）
  - PWSCup2019_Osaka/     PWSCup2019用人工データ（全チームに参考情報として公開予定の大阪データセット）
    - info_region.csv       大阪の領域情報（領域ID，縦軸ID，横軸ID，中心部の緯度，中心部の経度，病院フラグ）
    - info_time.csv         時刻情報（参照トレース/元トレース，時刻ID，日，時，分）
    - orgtraces_teamXXX_dataYY_ZZZ.csv    チーム番号XXX，データセット番号YYの元トレース
    - reftraces_teamXXX_dataYY_ZZZ.csv    チーム番号XXX，データセット番号YYの参照トレース

- Data_Anonymize/				       匿名加工データ（シャッフル前）

- Data_Anonymize_Shuffle/		  匿名加工データ（シャッフル後）

- Data_IDDisclose/            ID識別結果データ

- Data_TraceInfer/            トレース推定結果データ

- Prog_Eval/                有用性・安全性評価プログラム
  - EvalSecI.py						  ID識別安全性評価プログラム
  - EvalSecT.py             トレース推定安全性評価プログラム
  - EvalUtil.py             有用性評価プログラム

- Prog_Shuffle/             シャッフル（仮名化）プログラム
  - ShuffleIDs.py           指定したディレクトリ下の全匿名加工データに対して，ユーザIDをシャッフルするプログラム

- SmplProg_Anonymize/				匿名加工サンプルプログラム
  - A1-none.py					評価用トレースをそのまま出力する（何もしない）
  - A2-MRLH.py					MRLH (Merging Regions and Location Hiding) [Shokri+,S&P11]
  - A3-kRR.py					  k-RR (k-ary randomized response) [Kairouz+,ICML16]
  - A4-PL.py						PL (Planaer Laplace mechanism) [Andres+,CCS13]
  - A5-YA.py						Yamaoka anonymization (cheating anonymization)

- SmplProg_IDDisclose/			ID識別（ID-disclosure）サンプルプログラム
  - I1-rand.py					  ランダムなID識別
  - I2-VisitProb.py				ユーザ毎の領域滞在分布を学習し，最も尤度の大きいユーザとしてID識別する
  - I3-HomeProb.py        ユーザ毎の領域滞在分布を学習し，最も尤度の大きいユーザとしてID識別する（8時台のデータのみを使用）

- SmplProg_Track/					トレース推定（Trace Inference）サンプルプログラム
  - T1-rand.py					  ランダムなトレース推定
  - T2-VisitProb.py				ユーザ毎の領域滞在分布を学習し，最も尤度の大きい領域としてID識別後，位置情報を推定する
  - T3-HomeProb.py        ユーザ毎の領域滞在分布を学習し，最も尤度の大きい領域としてID識別後，位置情報を推定する（8時台のデータのみを使用）

- SmplResults/					サンプルプログラムの実験結果ファイル（EvalAll.pyを実行して得られたファイル）
  - results_team001_data01.csv			EvalAll.pyを実行して得られたファイル
  - results_team001_data01.xlsx			results_team001_data01.csvの結果を図にまとめたファイル

- Eval.bash						大阪の元トレース（チーム番号：001，データセット番号：01）を匿名加工（A2-MRLH）・ID識別（I1-rand）・トレース推定（T1-rand）する．

- EvalAll.py					大阪の元トレース（チーム番号：001，データセット番号：01）に対して，全匿名加工・全ID識別・全トレース推定アルゴリズムを走らせる．
