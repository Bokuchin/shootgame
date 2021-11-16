#上下キーで移動
#スペースキーで射撃
#23行目のrandom.seed(1)を有効にすることで、敵機出現位置を毎回同じにすることができる
import random, sys
import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))

#自機
myimg = pg.transform.scale(pg.image.load("images/myship.png"), (50, 50))
myrect = pg.Rect(50, 300, 50, 50)

#弾丸
bulletimg = pg.transform.scale(pg.image.load("images/beam.png"), (16, 16))
bullets = []

#敵機
enemyimg = pg.transform.scale(pg.image.load("images/enemy.png"), (50, 50))
enemies = []
#敵機数100機、出現位置ランダム
ex = [600 + (100 * i) for i in range(100)]
#random.seed(1)#敵機出現位置を固定にする場合アンコメントしてください
ey = [random.randint(0, 550) for i in range(100)]
for i in range(100):
    enemies.append(pg.Rect(ex[i], ey[i], 50, 50))

#星
starimg = pg.transform.scale(pg.image.load("./images/star.png"), (12, 12))
stars = []
for i in range(60):
    star = pg.Rect(random.randint(0, 600), 10 * i, 30, 30)
    star.w = random.randint(1, 4)#星の動く速さ
    stars.append(star)

#リプレイボタン画像
replay_img = pg.image.load("images/replaybtn.png")

#変数諸々
pushflg = False
page = 1
score = 0#スコアを入れる変数
flg = 0#射撃ボタン押しっぱなしで連射を禁止するためのフラグ
flg2 = 0#外部プログラムで射撃押しっぱなし連射を禁止するためのフラグ
frame = 0#フレーム数
des_e = 0
key = None
gamestop = 0
#移動変数
houkou = 0#1なら下、-1なら上
#射撃変数
fire = 0#1なら射撃

#btnを押したらnewpageへジャンプ
def btn_to_jump(btn, newpage):
    global page, pushflg
    #プレイヤーの入力を調べる
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]:
        pg.mixer.Sound("sounds/NES-Shooter01-7(Score).wav").play()
        if btn.collidepoint(mx, my) and pushflg == False:
            page = newpage
            pushFlag = True
        else:
            pushFlag = False

#STAGE
def stage():
    #画面初期化
    global score, page, bcount, flg, flg2, frame, key, des_e, fire, houkou
    des_e = 0
    frame += 1
    screen.fill(pg.Color("gray13"))
    #星の処理
    for star in stars:
        star.x -= star.w#wは星の動く速さ
        screen.blit(starimg, star)
        if star.x < 0:
            star.x = 800
            star.y = random.randint(0, 600)
    #プレイヤーからの入力を調べて自機の処理
    key = pg.key.get_pressed()
    if key[pg.K_UP] == 1 or houkou == -1:
        myrect.y = myrect.y - 10
        if myrect.y < 0:
            myrect.y = 0
    if key[pg.K_DOWN] == 1 or houkou == 1:
        myrect.y = myrect.y + 10
        if myrect.y > 550:
            myrect.y = 550
    screen.blit(myimg, myrect)

    #射撃
    if key[pg.K_SPACE] and flg == 0:
        bulletrect = pg.Rect(myrect.x + 50, myrect.y + 8, 16, 16)
        bullets.append(bulletrect)
        pg.mixer.Sound("sounds/NES-Shooter01-1(Shoot).wav").play()
        flg = 1
    elif key[pg.K_SPACE] != 1 and flg == 1:
        flg = 0
    #外部自動化プログラムの入力を受け付ける部分(射撃の)
    if fire == 1 and flg2 == 0:
        bulletrect = pg.Rect(myrect.x + 50, myrect.y + 0, 50, 50)
        bullets.append(bulletrect)
        pg.mixer.Sound("sounds/NES-Shooter01-1(Shoot).wav").play()
        flg2 = 1
    elif fire != 1 and flg2 == 1:
        flg2 = 0
    for i in reversed(range(len(bullets))):
        bullets[i].x += 15
        screen.blit(bulletimg, bullets[i])
        if bullets[i].x >= 800:
            del bullets[i]
    #敵機の処理
    enx = 0
    for enemy in enemies:
        enemy.x -= 10
        screen.blit(enemyimg, enemy)
        if enemy.x < 0:#通り過ぎた敵機は-100の位置に置いとく
            enemy.x = -100
            enemy.y = -100
        #自機と敵機の衝突処理
        if enemy.colliderect(myrect):
            page = 2
            pg.mixer.Sound("sounds/NES-Shooter01-5(Damage).wav").play()
        #弾丸と敵機の衝突処理
        for i in reversed(range(len(bullets))):
            if enemy.colliderect(bullets[i]):
                score = score + 100
                enemy.y = -100
                enemy.x = -100
                des_e = 1
                del bullets[i]
                pg.mixer.Sound("sounds/NES-Shooter01-3(Damage).wav").play()
        enx += enemy.x
        if enx <= -10000:
            page = 3
    #スコアの処理
    font = pg.font.Font(None, 40)
    text = font.render("SCORE : "+str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20,20))
    #フレーム数の表示
    font = pg.font.Font(None, 40)
    text = font.render("FRAME :"+str(frame), True, pg.Color("WHITE"))
    screen.blit(text, (250,20))

#データのリセット処理
def gamereset():
    global score, frame, clearsound, bullets#なぜかbulletsを書かないとエラー出る
    score = 0
    frame = 0
    clearsound = 0
    myrect.x = 50
    myrect.y = 300
    
    for i in reversed(range(len(bullets))):
        bullets[i].x = -100
        screen.blit(bulletimg, bullets[i])
        del bullets[i]
    bullets = []
    for i in range(100):
        enemies[i] = pg.Rect(ex[i], ey[i], 50, 50)

#ゲームオーバー処理
def gameover():
    global gamestop, frame
    gamestop = 1
    screen.fill(pg.Color("NAVY"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("RED"))
    screen.blit(text, (100, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    font = pg.font.Font(None, 40)
    text = font.render("SCORE :"+str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20, 20))
    #フレーム数の表示
    font = pg.font.Font(None, 40)
    text = font.render("FRAME :"+str(frame), True, pg.Color("WHITE"))
    screen.blit(text, (250,20))
    btn_to_jump(btn1, 1)
    if page == 1:
        gamereset()
#ゲームクリア処理
def gameclear():
    global gamestop, clearsound, frame
    gamestop = 1
    screen.fill(pg.Color("green"))
    font = pg.font.Font(None, 150)
    text = font.render("GAME CLEAR!", True, pg.Color("darkorange"))
    screen.blit(text, (10, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    font = pg.font.Font(None, 40)
    text = font.render("SCORE :"+str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20, 20))
    #フレーム数の表示
    font = pg.font.Font(None, 40)
    text = font.render("FRAME :"+str(frame), True, pg.Color("WHITE"))
    screen.blit(text, (250,20))
    if clearsound == 0:
        pg.mixer.Sound("sounds/NES-Shooter01-8(Score).wav").play()
        clearsound = 1
    btn_to_jump(btn1, 1)
    if page == 1:
        gamereset()


#メインループ
clearsound = 0
shootq = 0
def main():
    global page, shootq
    if page == 1:
        stage()
    elif page == 2:
        gameover()
    elif page == 3:
        gameclear()
    pg.display.update()
    pg.time.Clock().tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            shootq = 1
            pg.quit()
            sys.exit()
    
if __name__ == '__main__':
    while True:
        if page == 1:
            stage()
        elif page == 2:
            gameover()
        elif page == 3:
            gameclear()
        pg.display.update()
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                shootq = 1
                pg.quit()
                sys.exit()
