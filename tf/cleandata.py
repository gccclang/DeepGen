import re
import glob,subprocess,shutil,sys
from subprocess import Popen, PIPE, STDOUT
from os import walk
import os
import glob
import pdb

def remove_comment(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ' ' # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def remove_space(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s', ' ', text)
    text = re.sub(r'\\t', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text

def all_files_path(rootDir):                       
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file_path = os.path.join(root, file)
            filepaths.append(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir) 
            all_files_path(dir_path)
def run_cmd_save_errorInformation(cmd,writepath):
	result_str=''
	#process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	error_f = process.stderr
	errors = error_f.read()
	#print(errors)
	if errors:
		result_str = errors
	if error_f:
		error_f.close()
	#f = open(writepath,'w+',encoding='utf-8')
	f = open(writepath,'w+')
	f.write(str(result_str))
	f.close()
def run_cmd_save_errorInformation1(cmd,writepath):
	r = os.popen(cmd)
	info = r.readlines()
	#f = open(writepath,'w+',encoding='utf-8')
	f = open(writepath,'w+')
	for line in info:
	    line = line.strip('\n')
	    print('-------------------------')
	    print(line)
	    f.write(line+'\n')
	f.close()
def errorfile(rewritepath):
	flagcrash = False
	f = open(rewritepath)
	lines = f.readlines()
	for j in range(len(lines)):
		if 'error:' in lines[j]:
			flagcrash = True
	f.close()
	return flagcrash

path = './seed/'
files = []
filepaths = []
cleadatalist = [[]]
valid_count = 0

#read c++ keyword
keyword = []
with open('./c++keyword.txt', 'r') as fr:
	for key in fr.readlines():
	    keyword.append(key.strip())
for root, d_names, f_names in os.walk(path):
	for f in f_names:
	    files.append(os.path.join(root, f))
for file in files:
	delset = {}
	delsetshunxu = {}
	typecount = {}
	print(file)
	filelist = file.split('/')
	realname = filelist[len(filelist)-1]
	
	#text = open(file, 'r', encoding='utf-8').read()
	text = open(file, 'r').read()
	cmd = '/home/tangtang/compiler/clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++ -Xclang -ast-dump -fsyntax-only '+ file
	#cmd = '/home/oscar/compiler/llvm-project/build/bin/clang++ -cc1 -ast-dump '+ file
	rewritepathast = './ast-information/'+realname+'.txt'
	run_cmd_save_errorInformation1(cmd,rewritepathast)
	#read ast
	astinfor = []
	with open(rewritepathast, 'r') as fa:
	    for infor in fa.readlines():
	        astinfor.append(infor)
	astinfor.pop(0)	
	Cfile = set()
	Cfilelist = []
	allwordlist = []
	Cfilelength = 0
	#print(type(Cfile))
	Cfileword = ''
	Cfilemethodname = ''
	f =open (file,'r',True)
	try:
	    while True:
	        ch = f.read(1)
	        if not ch:
	            break
	        if ch.isalpha() or ch == '_':
	            if Cfilemethodname.strip() != '':
	                Cfilemethodname = ''.join([Cfilemethodname,ch])
	            else:
	                Cfileword = ''.join([Cfileword,ch])
	        elif ch == '.':
	            Cfilemethodname = ''.join([Cfilemethodname,ch])
	        else:
	            if Cfileword.strip() != '':
	                allwordlist.append(Cfileword)	
	                flaginsert = True
	                for subkey in keyword:
	                    if subkey == Cfileword:
	                        flaginsert = False
	                        break
	                if flaginsert:
	                    Cfile.add(Cfileword)
	                    newlength = len(Cfile)
	                    if Cfilelength != newlength:
	                        Cfilelength = newlength
	                        Cfilelist.append(Cfileword)
	                Cfileword = ''
	            if Cfilemethodname.strip() != '':
	                allwordlist.append(Cfilemethodname)
	                Cfilemethodname = ''
	            allwordlist.append(ch)
	finally:
	    f.close()

	Cfilecopy = Cfile.copy()
	for subword in Cfile:
	    flag = False
	    if subword.isalpha() or '_' in subword:
	        for subkey in keyword:
	            if subkey == subword:
	                flag = True
	                break
	        if flag is False:
	            for subinfor in astinfor:
	                if 'col:' in subinfor:
	                    newsubinfor = subinfor[subinfor.index('-')+1:]
	                    typenewsubword = newsubinfor[:newsubinfor.index(' ')]
	                    remainsubword = newsubinfor[newsubinfor.index('col')+3:]
	                    newsubword = ' '+subword+' '
	                    if newsubword in remainsubword:
	                        Cfilecopy.remove(subword)
	                        delset[subword] = typenewsubword
	                        break

	if len(Cfilecopy) != 0:
	    for remainword in Cfilecopy:
	        for subinfor1 in astinfor:
	            if 'col:' in subinfor1:
	                newsubinfor1 = subinfor1[subinfor1.index('-')+1:]
	                typenewsubword1 = newsubinfor1[:newsubinfor1.index(' ')]
	                remainsubword1 = newsubinfor1[newsubinfor1.index('col')+3:]
	                if remainword in remainsubword1:
	                    delset[remainword] = typenewsubword1
	                    break

	for keyorder in Cfilelist:
	    if keyorder in delset.keys():
	        print('yes')
	        keyvalue = delset[keyorder]
	        print('keyvalue:'+keyvalue)
	        if len(typecount) != 0:
	            if keyvalue in typecount.keys():
	                typevalue = typecount[keyvalue]
	                print('typevalue:'+typevalue)
	                newtypevalue = chr(ord(typevalue)+1)
	                typecount[keyvalue] = newtypevalue
	                delsetshunxu[keyorder] = keyvalue+newtypevalue
	                print('/////'+keyorder+'/////'+delsetshunxu[keyorder])
	            else:
	                typecount[keyvalue] = 'A'
	                delsetshunxu[keyorder] = keyvalue+'A'
	        else:
	            typecount[keyvalue] = 'A'
	            delsetshunxu[keyorder] = keyvalue+'A'

	cleandata = ''
	for eachword in allwordlist:
	    butihuanflag = True
	    for subdelsetshunxu in delsetshunxu.keys():
	        if subdelsetshunxu == eachword:
	            butihuanflag = False
	            print(subdelsetshunxu+':'+delsetshunxu[subdelsetshunxu])	            
	            cleandata += str(delsetshunxu[subdelsetshunxu])		
	    if butihuanflag:
	         cleandata += eachword

	cleandata_nocomment = remove_comment(cleandata)
	cleandata_nospace = remove_space(cleandata_nocomment)
	rewritepathnew = './inferseed/'+realname
	fwnew = open(rewritepathnew,'a+')
	fwnew.write(cleandata_nospace)
	fwnew.close()
	cleadatalist.append(cleandata_nospace)

fwrite = open('./train.txt','a+')	
for index_cleandata in range(0,len(cleadatalist)):
	fwrite.write(cleadatalist[index_cleandata]+'\n')
	fwrite.write('\n')
fwrite.close()

