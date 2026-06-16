import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rct:pg.Rect):
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル
    True：画面内/False：画面外
    """
    yoko,tate=True,True

    if rct.left<0 or WIDTH<rct.right:
        yoko=False
    if rct.top<0 or HEIGHT<rct.bottom:
        tate=False
    return yoko,tate

def gameover(screen:pg.Surface)->None:
    #黒い矩形を描画する
    black=pg.Surface((WIDTH,HEIGHT))
    black.fill((0,0,0))
    black.set_alpha(255)
    #白文字でGame Overを書く
    fonto=pg.font.Font(None,50)
    text=fonto.render("GAME OVER",True,(255,255,255))
    text_rect=text.get_rect(center=(WIDTH//2,HEIGHT//2))
    #こうかとんの画像左右二枚を置く
    cry_img=pg.transform.rotozoom(pg.image.load("fig/8.png"),0,1.0)
    cryleft_rct=cry_img.get_rect()
    cryleft_rct.center=(WIDTH//2-150,HEIGHT//2)
    cryright_rct=cry_img.get_rect()
    cryright_rct.center=(WIDTH//2+150,HEIGHT//2)
    #surfaceに貼ってる
    black.blit(cry_img,cryleft_rct)
    black.blit(cry_img,cryright_rct)
    black.blit(text,text_rect)
    screen.blit(black,(0,0))
    #五秒間表示させるを実装する
    pg.display.update()
    time.sleep(5)
    
def get_kk_imgs()->dict[tuple[int,int],pg.Surface]:
    img_left=pg.transform.rotozoom(pg.image.load("fig/3.png"),0,1.0)
    img_right=pg.transform.flip(pg.image.load("fig/3.png"),True,False)
    kk_dict={(0,0):img_left,
             (+5,0):img_right,
             (+5,-5):pg.transform.rotozoom(img_right,45,1),
             (0,-5):pg.transform.rotozoom(img_right,90,1),
             (-5,-5):pg.transform.rotozoom(img_left,-45,1),
             (-5,0):img_left,
             (-5,+5):pg.transform.rotozoom(img_left,45,1),
             (0,+5):pg.transform.rotozoom(img_right,-90,1),
             (+5,+5):pg.transform.rotozoom(img_right,-45,1),

             }
    return kk_dict
    

    
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    bb_img=pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct=bb_img.get_rect()
    bb_rct.centerx=random.randint(0,WIDTH)
    bb_rct.centery=random.randint(0,HEIGHT)
    vx,vy=+5,+5
    bb_img.set_colorkey((0,0,0))
    kk_img=get_kk_imgs()

    
   
    
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): 
            #こうかとんrectと爆弾rectが重なったら
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
         #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
          #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move(-sum_mv[0],-sum_mv[1])#動きをなかったことにする
        screen.blit(kk_img[tuple(sum_mv)], kk_rct)

        bb_rct.move_ip(vx,vy)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
