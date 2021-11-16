#敵機が自機の上下に近づいたら自機の動きを止める
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

x_exist = 0
y_exist = 0
isou = 0
def auto2():#移動をオートにする関数
    global x_exist, y_exist, isou
    x_exist = 0
    y_exist = 0

    if isou == 0:#上昇フェーズ
        for e in sh.enemies:
            if 0 < e.x < 160:
                x_exist = 1
            if 0 < e.y <= sh.myrect.y:
                y_exist = 1
        if x_exist and y_exist:
            sh.houkou = 0
        else:
            sh.houkou = -1
            if sh.myrect.y == 0:
                isou = 1
    x_exist = 0
    y_exist = 0
    if isou == 1:#下降フェーズ
        for e in sh.enemies:
            if 0 < e.x < 160:
                x_exist = 1 
            if e.y >= sh.myrect.y + 50:
                y_exist = 1
        if x_exist and y_exist:
            sh.houkou = 0
        else:
            sh.houkou = 1
            if sh.myrect.y >= 549:
                isou = 0    
while True:
    if sh.shootq == 1:
        sys.exit()

    if sh.frame % 2 == 0:#フレーム数が偶数の時に射撃する
        auto()
    auto2()
    sh.main()
