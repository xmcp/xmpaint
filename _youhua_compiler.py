#coding=utf-8
import sys
if sys.version[0]=='2':
    os.system('start c:/python34/pythonw.exe '+sys.argv[0])
    sys.exit(-1)

import subprocess
import os
import hashlib

def buildraw(compiler):
    lines=[]
    hllines=[]
    
    #interpret
    for data in profile_hl.split('\n'):
        if data:
            splited=data.split()
            if len(splited)==2:
                hllines.append(splited)
            elif len(splited)==1:
                lines.append('"%s"[color="black",fillcolor="greenyellow",style="bold,filled"];\n'%\
                    splited[0].replace('\\','\\\\').replace('"','\\"'))
            else:
                raise SyntaxError('qipa highlight')
    
    for data in profile_text.split('\n'):
        if not data:
            continue
        splited=data.split()
        for now in range(len(splited)):
            splited[now]=splited[now].replace('\\','\\\\').replace('"','\\"')
        if len(splited)==3:
            if [splited[0],splited[1]] in hllines:
                lines.append('"%s"->"%s"[label="%s",color="red",style="bold,filled"];\n'\
                    %tuple(splited))
            else:
                lines.append('"%s"->"%s"[label="%s"];\n'%tuple(splited))
        elif len(splited)==2:
            if [splited[0],splited[1]] in hllines:
                lines.append('"%s"->"%s"[color="red",style="bold,filled"];\n'%tuple(splited))
            else:
                lines.append('"%s"->"%s";\n'%tuple(splited))
        else:
            raise SyntaxError('qipa text')
            

    #write
    if not os.path.exists('output'):
        os.mkdir('output')
    try:
        with open('output/out.gv','w') as f:
            f.write('digraph A{\n')
            for a in lines:
                f.write(a)
            f.write('}')
    except Exception as e:
        raise ZeroDivisionError('cannot write file')

    #build
    if not os.path.isfile('compiler/%s.exe'%compiler):
        raise ZeroDivisionError('no compiler')
    exe=subprocess.Popen(
        '"compiler/%s.exe" output/out.gv -o output/out.png -Tpng'%compiler,
        shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr=exe.communicate()
    code=exe.wait()
    if code!=0:
        raise ZeroDivisionError('build failed')

    #judge
    if not os.path.isfile('output/out.png'):
        raise ZeroDivisionError('no out file')
    with open('output/out.png','rb') as f:
        return hashlib.md5(f.read()).hexdigest()

compilers=['circo','dot','fdp','sfdp']
profile_hl='''
1
2
3 4
5 6
'''
profile_text='''
1 2 1to2
2 3
3 4 3to4
4 5 4to5
!@#$%^&*() -_=+[]{};:\'",.<>/?
5 6 5to6
6 1
'''
print('--- Calculating md5...')
correct_md5={}
correct_md5['sfdp']=buildraw('sfdp')
correct_md5['fdp']=buildraw('fdp')
correct_md5['dot']=buildraw('dot')
correct_md5['circo']=buildraw('circo')
fnum=len(os.listdir('compiler'))
for ind,file in enumerate(os.listdir('compiler')):
    print('--- %d/%d: %s...'%(ind+1,fnum,file))
    os.rename('compiler/'+file,'compiler/'+file+'__')
    try:
        for c in compilers:
            if buildraw(c)!=correct_md5[c]:
                raise ZeroDivisionError('wrong md5')
    except ZeroDivisionError as e:
        os.rename('compiler/'+file+'__','compiler/'+file)
        print('  ! %s'%e)
    else:
        print('  ^ Deleted')
        os.remove('compiler/'+file+'__')
