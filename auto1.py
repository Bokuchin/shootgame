#shootgame.pyの敵出現位置を固定した場合の操作自動化のデモプログラム。自機の動きは決定的。
import time, sys
import shootgame as sh
flg = 0
def auto():#射撃をオートにする関数
    global flg
    #sh.fireが1は、射撃ボタンを押すことに相当する。sh.fireが0は射撃ボタンを離すことに相当する。
    #このauto()関数は、１回目の実行で射撃ボタンを押し、２回目の実行で射撃ボタンを離す。３回目は押す、４回目は離す…
    if flg == 0:
        sh.fire = 1
        flg = 1
    elif flg == 1:
        sh.fire = 0
        flg = 0

def auto2():#移動をオートにする関数
    if sh.frame == 1:#フレーム数が1の時
        sh.houkou = -1#自機を上に移動する
    if sh.frame == 30:#フレーム数が30の時
        sh.houkou = 1#自機を下に移動する
    if sh.frame == 90:
        sh.houkou = -1
    if sh.frame == 150:
        sh.houkou = 1
    if sh.frame == 210:
        sh.houkou = -1
    if sh.frame == 270:
        sh.houkou = 1
    if sh.frame == 330:
        sh.houkou = -1
    if sh.frame == 390:
        sh.houkou = 1
    if sh.frame == 450:
        sh.houkou = -1
    if sh.frame == 510:
        sh.houkou = 1
    if sh.frame == 570:
        sh.houkou = -1
    if sh.frame == 660:
        sh.houkou = 1
    if sh.frame == 720:
        sh.houkou = -1
    if sh.frame == 790:
        sh.houkou = 1
    if sh.frame == 850:
        sh.houkou = -1
    if sh.frame == 910:
        sh.houkou = 1
    if sh.frame == 970:
        sh.houkou = -1
    if sh.frame == 1030:
        sh.houkou = 1


while True:
    if sh.shootq == 1:
        sys.exit()

    if sh.frame % 2 == 0:#フレーム数が偶数の時に射撃する
        auto()
    auto2()
    sh.main()
