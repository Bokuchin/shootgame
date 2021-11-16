#敵機絶対撃墜するマン。無駄撃ちもしない
import time, sys
import shootgame as sh
flg = 0
def auto():#射撃をオートにする関数
    global flg
    if flg == 0:
        sh.fire = 1
        flg = 1
    elif flg == 1:
        sh.fire = 0
        flg = 0

def auto2():#移動をオートにする関数
    global flg
    for e in sh.enemies:
        if e.x == 600:
            sh.myrect.y = e.y#自機のY位置を敵機のY位置に直接移動
            sh.fire = 1



while True:
    if sh.shootq == 1:
        sys.exit()

    auto2()
    sh.main()
    sh.fire = 0#sh.fireの値を1以外に戻しておく
