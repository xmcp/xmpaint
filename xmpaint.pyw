#coding=utf-8
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.ttk import *
import subprocess
import threading
import time
import os

class GraphWiz:
    @staticmethod
    def esc(x):
        return x.replace('\\',' ').replace('"','\\"')

    def __init__(self,directed,nicktxt):
        self.directed=directed
        self.output=['%s A{\n'%('digraph' if directed else 'graph'),'node[fontname="黑体"]; edge[fontname="黑体"];']
        self.edge_hl=set()
        self.nicks={self.esc(k):v for x in nicktxt.split('\n') if x for k,_,v in [x.partition(' ')]}
    
    def getnick(self,name,isedge):
        name=self.esc(name)
        return self.nicks.get(('|' if isedge else '')+name,name)
    
    def highlight_edge(self,a,b):
        a=self.getnick(a,isedge=False)
        b=self.getnick(b,isedge=False)
        self.edge_hl.add((a,b))
        if not self.directed:
            self.edge_hl.add((b,a))
            
    def highlight_node(self,a):
        self.output.append('"%s"[color="black",fillcolor="greenyellow",style="bold,filled"];\n'%\
            self.getnick(a,isedge=False))
            
    def addedge(self,a,b,label=None):
        a=self.getnick(a,isedge=False)
        b=self.getnick(b,isedge=False)
        fstr='"%s"->"%s"'%(a,b) if self.directed else '"%s"--"%s"'%(a,b)
        if label:
            label=self.getnick(label,isedge=True)
            if (a,b) in self.edge_hl:
                self.output.append(fstr+'[label="%s",color="red",style="bold,filled"];\n'%label)
            else:
                self.output.append(fstr+'[label="%s"];\n'%label)
        else:
            if (a,b) in self.edge_hl:
                self.output.append(fstr+'[color="red",style="bold,filled"];\n')
            else:
                self.output.append(fstr+';\n')

    def result(self):
        return ''.join(self.output+['}'])
                
def buildraw(*_):
    compiler=compilervar.get()
    lines=[]
    hllines=[]
    global img
    global canvasimg
    starttime=time.time()
    
    #interpret
    tk.title('Interpreting data...')
    gw=GraphWiz(directed.get()=='yes',nickin.get(1.0,END))
    
    for data in hlin.get(1.0,END).split('\n'):
        if data:
            splited=data.split(' ')
            if len(splited)==2:
                gw.highlight_edge(*splited)
            elif len(splited)==1:
                gw.highlight_node(splited[0])
            else:
                messagebox.showerror('Error','Syntax error in highlight item "%s"'%data)    
    
    for data in textin.get(1.0,END).split('\n'):
        if not data:
            continue
        splited=data.split()
        if len(splited)<2:
            messagebox.showerror('Error','Syntax error in adjacency item "%s"'%data)
            return
        elif len(splited)>3:
            splited=[splited[0],splited[1],' '.join(splited[2:])]
        gw.addedge(*splited)
    
    #write
    tk.title('Writing graph file...')
    if not os.path.exists('output'):
        os.mkdir('output')
    try:
        with open('output/out.gv','w',encoding='utf-8') as f:
            f.write(gw.result())
    except Exception as e:
        messagebox.showerror('Error','Can\'t write file: %s'%e)
        return

    #build
    tk.title('Building graph file...')
    if not os.path.isfile('compiler/%s.exe'%compiler):
        messagebox.showerror('Error','Can\'t find %s compiler'%compiler)
        return
    exe=subprocess.Popen(
        '"compiler/%s.exe" output/out.gv -o output/out.png -Tpng'%compiler,
        shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr=exe.communicate()
    code=exe.wait()
    if code!=0:
        return messagebox.showerror('Error','Compiler returned %d.\n\nSTDOUT:\n%s\n\nSTDERR:\n%s'%(
            code,
            stdout.decode(encoding='gbk',errors='ignore'),
            stderr.decode(encoding='gbk',errors='ignore'),
        ))
    #log(stdout.decode(encoding='gbk',errors='ignore'),'output')
    #log(stderr.decode(encoding='gbk',errors='ignore'),'output')

    #display
    tk.title('Loading image...')
    try:
        img=PhotoImage(file='output/out.png')
    except Exception as e:
        messagebox.showerror('Error','Can\'t display image: %s'%e)
        return

    if canvasimg:
        canvas.delete(canvasimg)
    midwidth=canvas.winfo_width()//2
    midheight=canvas.winfo_height()//2
    imgwidth=img.width()
    imgheight=img.height()
    tk.title('Redrawing canvas...')
    canvas['scrollregion']=(
        midwidth-imgwidth/2-10,midheight-imgheight/2-10,
        midwidth+imgwidth/2+10,midheight+imgheight/2+10)
    canvasimg=canvas.create_image(\
        midwidth,midheight,anchor=CENTER,image=img)

    #cleanup
    if shouldCleanup.get()=='yes':
        tk.title('Cleaning up...')
        try:
            os.remove('output/out.gv')
            os.remove('output/out.png')
        except OSError as e:
            messagebox.showerror('Error','Can\'t remove temp file: %s'%e)
            return

def build(*_):
    def mybuild():
        global building
        building=True
        buildbtn['state']='disabled'
        try:
            buildraw()
        except Exception as e:
            messagebox.showerror('Error','Unhandled exception: %r'%e)
            raise
        finally:
            tk.title('xmPaint')
            building=False
            buildbtn['state']='normal'

    if building:
        return
    t=threading.Thread(target=mybuild,args=())
    t.setDaemon(True)
    t.start()

def startmove(event):
    global movex
    global movey
    movex,movey=event.x,event.y

def moving(event):
    global movex
    global movey
    canvas.xview_scroll(movex-event.x,'units')
    canvas.yview_scroll(movey-event.y,'units')
    movex,movey=event.x,event.y
    
tk=Tk()
tk.geometry('900x600')
tk.title('xmPaint')
tk.rowconfigure(0,weight=1)
tk.columnconfigure(1,weight=1)
tk.bind_all('<F5>',build)
compilervar=StringVar(value='dot')
directed=StringVar(value='yes')
shouldCleanup=StringVar(value='yes')
building=False
sidebar_visible=True

def switcher(_):
    global sidebar_visible
    sidebar_visible=not sidebar_visible
    
    if sidebar_visible:
        sidebar.grid(row=0,column=0,sticky='NS')
        tk.title('xmPaint')
    else:
        sidebar.grid_forget()
        tk.title('xmPaint （按 Alt+` 显示边栏）')

#text in
sidebar=Frame(tk)
sidebar.grid(row=0,column=0,sticky='NS')
sidebar.rowconfigure(0,weight=1)

textbook=Notebook(sidebar)
textbook.grid(row=0,column=0,columnspan=2,sticky='NSWE')
textbook.rowconfigure(0,weight=1)
textbook.columnconfigure(0,weight=1)

tk.bind('<Alt-`>',switcher)

selector=lambda obj,ind:lambda _:obj.select(ind)
for ind,(name,title,color) in enumerate((
        ('textin','邻接表 Alt + 1','#ddddff'),
        ('hlin','高亮 2','#ffffcc'),
        ('nickin','别名 3','#ccffcc'))):
        
    textframe=Frame(textbook)
    textbook.add(textframe,text=title)
    textframe.rowconfigure(0,weight=1)
    textframe.columnconfigure(0,weight=1)
    tk.bind('<Alt-Key-%d>'%(ind+1),selector(textbook,ind))
    
    textin_=Text(textframe,font='Consolas',width=20,bg=color)
    globals()[name]=textin_
    textin_.grid(row=0,column=0,sticky='NSWE')
    textin_sbar=Scrollbar(textframe,orient=VERTICAL,command=textin_.yview)
    textin_sbar.grid(row=0,column=1,sticky='NS')
    textin_['yscrollcommand']=textin_sbar.set
    
#canvas
imgframe=Frame(tk)
imgframe.grid(row=0,column=1,sticky='NSWE')
imgframe.grid_columnconfigure(0,weight=1)
imgframe.grid_rowconfigure(0,weight=1)

img=PhotoImage()
canvasimg=None

imgh=Scrollbar(imgframe,orient=HORIZONTAL)
imgv=Scrollbar(imgframe,orient=VERTICAL)
canvas=Canvas(imgframe,yscrollcommand=imgv.set,xscrollcommand=imgh.set,
              xscrollincrement='1',yscrollincrement='1')
canvas.configure(background='#FFFFFF')
imgh['command']=canvas.xview
imgv['command']=canvas.yview
canvas.grid(column=0,row=0,sticky='NSWE')
imgh.grid(column=0,row=1,sticky='WE')
imgv.grid(column=1,row=0,sticky='NS')

movex,movey=0,0
canvas.bind("<Button-1>", startmove)
canvas.bind("<B1-Motion>", moving)

#config frame
frame1=Frame(sidebar)
frame1.grid(row=1,column=0,columnspan=2)
Checkbutton(frame1,text='有向图',variable=directed,onvalue='yes',offvalue='no')\
    .grid(row=0,column=0)
Combobox(frame1,textvariable=compilervar,values=('dot','fdp','sfdp','circo'),width=5)\
    .grid(row=0,column=1,padx=2)
buildbtn=Button(frame1,text='生成 (F5)',command=build,width=8)
buildbtn.grid(row=0,column=2)

frame2=Frame(sidebar)
frame2.grid(row=2,column=0,columnspan=2)
Checkbutton(frame2,text='清理临时文件',variable=shouldCleanup,onvalue='yes',offvalue='no')\
    .grid(row=0,column=0)
Checkbutton(frame2,text='监视剪切板')\
    .grid(row=0,column=1) #todo

mainloop()
