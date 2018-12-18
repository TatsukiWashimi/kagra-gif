# CDMR
## Log

2018/12/10：GWpyを使っていない昔の古いコードが残っていたので、新しくした。


## データ
### 期間
|No.   |Start GPS  | Start JST           | tlen  | memo |
| ---  |---------- | --------------------| ----- | --- |
|1     |1217170818 | 2018-08-02 00:00:00 | 2**13 | main.py |
|2     |1217257218 | 2018-08-03 00:00:00 | 2**13 | main.py |
|3     |1217926818 | 2018-08-10 18:00:00 | 2**13 | main.py |
|4     |1217935011 | 2018-08-10 20:16:33 | 2**13 | main.py |
|5     |1219309218 | 2018-08-26 18:00:00 | 2**13 | main.py |
|6     |1214784018 | 2018-07-05 09:00:00 | ???   | img_cdmr_xarm.pngのデータ |
|7     |1217229027 | 2018-08-02 16:10:09 | ???   | img_cdmr_imc.pngのデータ |
|8     |1209368000 | 2018-05-03 16:33:02 | 2**13 | main_blrms.py |
|9     |1209286818 | 2018-05-02 18:00:00 | 2**13 | main_blrms.py |
|10    |1214784018 | 2018-07-05 09:00:00 | 2**13 | main_blrms.py |
|11    |1214611218 | 2018-07-03 09:00:00 | 2**13 | main_blrms.py |
|12    |1211252736 | 2018-05-25 12:05:18 | 2**13 | main_blrms.py |

 * 解析につかったものと、ゴミが混ざっているので実際に確認する必要あり。


### 使用チャンネル
|Location| Channel name|
|---|---|
|Xend  | K1:PEM-EXV\_SEIS\_{WE/NS/Z}\_SENSINF\_IN1\_DQ | 
|Yend  | K1:PEM-EYV\_SEIS\_{WE/NS/Z}\_SENSINF\_IN1\_DQ |
|Center| K1:PEM-IXV\_SEIS\_{WE/NS/Z}\_SENSINF\_IN1\_DQ |
|MCi | K1:PEM-IMC\_SEIS\_MCI\_{WE/NS/Z}\_SENSINF\_IN1\_DQ |
|MCe | K1:PEM-IMC\_SEIS\_MCE\_{WE/NS/Z}\_SENSINF\_IN1\_DQ |

 * Xエンドは30dbのアンプあり。
 * センターとYエンドはない。
 * IMCの2つは45dbのアンプがある状態。
 * このときすべて2048Hz









### memo

Commit : 82d18eb
* main.pyはBandPassしたデータやCDMRのプロットなどをするメイン関数だった。Gwpyに対応していないので、消す。一応解析につかった時期とチャンネルは上の通り。No6とNo7はこのときのコミットにはなかった。
* その他のファイルすべて消した。一応上に書いてある情報で解析はできるはず。

