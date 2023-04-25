import random
import sys

import pygame as pg


delta = {                                               # 各キーが押下された時の移動動作を辞書で設定
         pg.K_UP: (0, -1),
         pg.K_DOWN: (0, +1),
         pg.K_LEFT: (-1, 0),
         pg.K_RIGHT: (+1, 0)
        }


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect):
    """
    オブジェクトが画面内or画面外を特定し，真理値タプルを返す関数
    
        scr_rct (pg.Rect): 画面Surfaceのrect
        obj_rct (pg.Rect): こうかとん，または爆弾Surfaceのrect
        返り値: 縦方向，横方向のはみ出し判定結果（画面内=True / 画面外=False） 
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex01/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex01/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_rev = pg.transform.flip(kk_img, True, False)
    
    kk_dct = {                                          # こうかとんの各向きの画像を格納した辞書
          (0, -1) : pg.transform.rotozoom(kk_img_rev, 90, 1.0),
          (+1, -1): pg.transform.rotozoom(kk_img_rev, 45, 1.0), # Issue3変更点
          (+1, 0) : pg.transform.rotozoom(kk_img_rev, 0, 1.0),
          (+1, +1): pg.transform.rotozoom(kk_img_rev, 315, 1.0),
          (0, +1) : pg.transform.rotozoom(kk_img_rev, 270, 1.0),
          (-1, +1): pg.transform.rotozoom(kk_img, 45, 1.0),
          (-1, 0) : pg.transform.rotozoom(kk_img, 0, 1.0),
          (-1, -1): pg.transform.rotozoom(kk_img, 315, 1.0)
             }

    
    kk_rect = kk_img.get_rect()                         # こうかとんのrectの座標を取得
    kk_rect.center = (900, 400)                         # こうかとんの初期位置を(900, 400)に設定
    bb_img = pg.Surface((20, 20))                       # 1辺が20の正方形Surfaceの作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)   # Surfaceの中心に半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))                      # 黒を透過させる
    x, y = random.randint(0, 1600), random.randint(0, 900)  # ランダムな座標x, yを生成
    screen.blit(bb_img, [x, y])                         # 爆弾をx, yの位置に描画
    vx, vy = +1, +1                                     # 縦，横方向の速度を設定
    bb_rect = bb_img.get_rect()                         # 爆弾の位置のrectの座標を取得
    bb_rect.center = (x, y)                             # rectの初期位置をx, yに設定
    tmr = 0
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1
        key_lst = pg.key.get_pressed()                  # 押されたキーを取得
        sum_delta_x = 0                                 # xの移動量の合計値
        sum_delta_y = 0                                 # yの移動量の合計値
        for k, mv in delta.items():                     # 辞書から移動方向を取得
            if key_lst[k]:
                kk_rect.move_ip(mv)
                sum_delta_x += mv[0]
                sum_delta_y += mv[1]
        sum_delta = (sum_delta_x, sum_delta_y)
        if sum_delta == (0, 0):                         # キーが押されていないとき
            kk_img                                      # 直前のこうかとんに
        else:                                           # そうでないとき
            kk_img = kk_dct[sum_delta]                  # 合計値に合わせた向きに
        
        if check_bound(screen.get_rect(), kk_rect) != (True, True):  # こうかとんがはみ出ていると
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rect.move_ip(-mv[0], -mv[1])
        
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect)                    # こうかとんの位置を移動した後の座標で描画
        bb_rect.move_ip(vx, vy)                         # rectの座標を移動
        yoko, tate = check_bound(screen.get_rect(), bb_rect)  # 爆弾の横と縦のはみ出ているかを判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rect)                    # 爆弾を画面に描画
        
        if kk_rect.colliderect(bb_rect):                # こうかとんと爆弾の衝突判定
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()