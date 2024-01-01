import pygame as pyg
import pygame.display as disp
import pygame.transform as trans
pyg.font.init()
pyg.mixer.init()

width,height=900,500
wship,hship=80,60
window=disp.set_mode((width,height))
disp.set_caption("SPACE FIGHT")

shoot=pyg.mixer.Sound("assets/shoot.mp3")
hit=pyg.mixer.Sound("assets/hit.mp3")
load=pyg.mixer.Sound("assets/load.mp3")
victory=pyg.mixer.Sound("assets/victory.mp3")
pyg.mixer.music.load('assets/bgscore.mp3')

dblue=(3,26,116)
black=(0,0,0)
redc=(255,0,0)
white=(255,255,255)
yellowc=(255,255,0)

fps=60
border=pyg.Rect(width//2-5,0,10,height)

f=pyg.font.SysFont("comicsans",40)
wf=pyg.font.SysFont("comicsans",100)
df=pyg.font.SysFont("comicsans",80)
hf=pyg.font.SysFont("comicsans",60)
ff=pyg.font.SysFont(None,30)

speed=5
vel=10
bc=3
yh=pyg.USEREVENT+1
rh=pyg.USEREVENT+2

sword=pyg.image.load("assets/swords.png")
sword=trans.scale(sword,(wship,hship))
yellowship=pyg.image.load("assets/yellow.png")
yship=trans.rotate(trans.scale(yellowship,(wship,hship)),90)
redship=pyg.image.load("assets/red.png")
rship=trans.rotate(trans.scale(redship,(wship,hship)),270)
bg=trans.scale(pyg.image.load("assets/space.png"),(width,height))
yk=trans.scale(pyg.image.load("assets/yellowkeys.png"),(200,200))
rk=trans.scale(pyg.image.load("assets/redkeys.png"),(200,200))

def ymoves(keys,r):
    if keys[pyg.K_a] and r.x-speed>0:
        r.x-=speed
    if keys[pyg.K_d] and r.x+speed+r.height<border.x:
        r.x+=speed
    if keys[pyg.K_w] and r.y-speed>0:
        r.y-=speed
    if keys[pyg.K_s] and r.y+speed+r.width<height:
        r.y+=speed

def rmoves(keys,r):
    if keys[pyg.K_LEFT] and r.x-speed>border.x+border.width:
        r.x-=speed
    if keys[pyg.K_RIGHT] and r.x+speed+r.height<width:
        r.x+=speed
    if keys[pyg.K_UP] and r.y-speed>0:
        r.y-=speed
    if keys[pyg.K_DOWN] and r.y+speed+r.width<height:
        r.y+=speed
        
def draw(red,yellow,rb,yb,rs,ys):
    window.blit(bg,(0,0))
    pyg.draw.rect(window,black,border)
    rstext=f.render("Score: "+str(rs),1,white)
    ystext=f.render("Score: "+str(ys),1,white)
    window.blit(rstext,(width-rstext.get_width()-10,10))
    window.blit(ystext,(10,10))
    window.blit(yship,(yellow.x,yellow.y))
    window.blit(rship,(red.x,red.y))
    for b in rb:
        pyg.draw.rect(window,redc,b)
    for b in yb:
        pyg.draw.rect(window,yellowc,b)
    disp.update()

def bullets(yb,rb,yellow,red):
    for b in yb:
        b.x+=vel
        if red.colliderect(b):
            hit.play()
            pyg.event.post(pyg.event.Event(rh))
            yb.remove(b)
        elif b.x>width:
            yb.remove(b)
    for b in rb:
        b.x-=vel
        if yellow.colliderect(b):
            hit.play()
            pyg.event.post(pyg.event.Event(yh))
            rb.remove(b)
        elif b.x<0:
            rb.remove(b)

        
def end(msg):
    txt=wf.render(msg,1,white)
    wp=(width-txt.get_width())//2
    hp=(height-txt.get_height())//2
    window.blit(txt,(wp,hp))
    victory.play()
    disp.update()
    pyg.time.delay(6000)

def disp1():
    window.fill(white)
    txt=df.render("SPACE FIGHT",1,black)
    wp=(width-txt.get_width())//2
    hp=txt.get_height()
    window.blit(txt,(wp,20))
    window.blit(sword,(wp-wship,50))
    window.blit(sword,(wp+txt.get_width(),50))
    txt=hf.render("Instructions for keys",1,black)
    wp=(width-txt.get_width())//2
    window.blit(txt,(wp,30+hp))
    hp+=txt.get_height()
    window.blit(yk,(200,hp+60))
    window.blit(rk,(500,hp+60))
    disp.update()
    
def main(a):
    if a==1:
        disp1()
        pyg.time.delay(10000)
    red=pyg.Rect(700,100,wship,hship)
    yellow=pyg.Rect(100,400,wship,hship)
    load.play()
    pyg.mixer.music.play(loops=-1)
    rb,yb=[],[]
    rs=ys=10
    clock=pyg.time.Clock()
    run=True
    while run:
        clock.tick(fps)
        for e in pyg.event.get():
            if e.type==pyg.QUIT:
                run=False
                pyg.quit()
            if e.type==pyg.KEYDOWN:
                if e.key==pyg.K_LCTRL and len(yb)<bc:
                    b=pyg.Rect(yellow.x+yellow.height,yellow.y+yellow.width//2-2,10,5)
                    yb.append(b)
                    shoot.play()
                if e.key==pyg.K_RCTRL and len(rb)<bc:
                    b=pyg.Rect(red.x-red.height,red.y+red.width//2-2,10,5)
                    rb.append(b)
                    shoot.play()
            if e.type==rh:
                rs-=1
            if e.type==yh:
                ys-=1
        keys=pyg.key.get_pressed()
        ymoves(keys,yellow)
        rmoves(keys,red)
        bullets(yb,rb,yellow,red)
        draw(red,yellow,rb,yb,rs,ys)
        msg=""
        if rs==0:
            msg="YELLOW WINS"
        elif ys==0:
            msg="RED WINS"
        if msg!="":
            pyg.mixer.music.stop()
            end(msg)
            break
    main(0)
if __name__ == "__main__":
    main(1)
