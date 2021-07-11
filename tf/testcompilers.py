# -*- coding: utf-8 -*
from __future__ import print_function
import sys,random,os,shutil,gc,subprocess,datetime,re,time,signal,shutil
import eventlet,io
from subprocess import Popen, PIPE, STDOUT
import numpy as np 
#os.environ['CUDA_VISIBLE_DEVICES'] = '1'
#only delete the programs under 'include'
sys.path.extend(['.', '..'])

eventlet.monkey_patch()
filepaths =[]

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
	f = open(writepath,'w+')
	f.write(str(result_str))
	f.close()

def timeout(cmd):
	"""call shell-command and either return its output or kill it
	if it doesn't normally exit within timeout seconds and return None"""
	start = datetime.datetime.now()
	process = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#	while process.poll() is None:
#		time.sleep(0.2)
#		now = datetime.datetime.now()
#		if (now - start).seconds > 5:
#			os.kill(process.pid, signal.SIGKILL)
#			os.waitpid(-1, os.WNOHANG)
#			return None
	return process.stdout.readlines()

def whethererror(rewritepath):
	flagcrash = False
	f = open(rewritepath)
	lines = f.readlines()
	for j in range(len(lines)):
		if 'error:' in lines[j]
			flagcrash = True
	f.close()
	return flagcrash

def whethergcccrash(rewritepath):
	flagcrash = False
	f = open(rewritepath)
	lines = f.readlines()
	for j in range(len(lines)):
		if 'internal compiler error' in lines[j]:
			flagcrash = True
	f.close()
	return flagcrash
def whetherllvmcrash(rewritepath):
	flagcrash = False
	f = open(rewritepath)
	lines = f.readlines()
	for j in range(len(lines)):
		if 'dump:' in lines[j]:
			flagcrash = True
	f.close()
	return flagcrash
def readfile(rewritepath):
	f = open(rewritepath)
	lines = f.readlines()

	return str(lines)
	

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def all_files_path(rootDir): 
	global filepaths                      
	for root, dirs, files in os.walk(rootDir):
		for file in files:
			file_path = os.path.join(root, file)
			filepaths.append(file_path)
		for dir in dirs:
			dir_path = os.path.join(root, dir) 
			all_files_path(dir_path)

if __name__ == "__main__":
	start = datetime.datetime.now()
	count0 = 0
	all_files_path('./inferseed/')
	for filepath in filepaths:
		realname = filepath.split('/')[-1]
		rewritepath00 = './'+realname
		shutil.copy(filepath, rewritepath00)
		cmd1 = '/usr/local/gcc-7.1.0/bin/g++ -c -std=c++11 -w -fsyntax-only '+ rewritepath00
		rewritepath1 = './detectbug/gcc/'+realname+".txt"
		run_cmd_save_errorInformation(cmd1,rewritepath1)
		flagerror1 = whethererror(rewritepath1)
		execute1 = ''

		flagcrash1 = whethergcccrash(rewritepath1)

		if bool(1-flagerror1) and bool(1-flagcrash1):
			cmdexecgcco0 = '/usr/local/gcc-7.1.0/bin/g++ -std=c++11 -O0 -Wno-narrowing '+ rewritepath00
			rewritepathgcco0 = './detectbug/gcco0/'+realname+".txt"
			try:
				with eventlet.Timeout(15, True):
					run_cmd_save_errorInformation(cmdexecgcco0,rewritepathgcco0)
					cmdexecgcco00 = './a.out'
					rewritepathout = './out.txt'
					if os.path.exists(cmdexecgcco00):
						run_cmd_save_errorInformation(cmdexecgcco00,rewritepathout)
						out = readfile(rewritepathout)
						del rewritepathout
						print('yes, execute1 under O0 is:'+str(out))
						execute1 = out
						os.remove('./a.out')
			except eventlet.timeout.Timeout:
				print('timeout')
				mediumtime = datetime.datetime.now()
				consumtime = mediumtime - start+ inserttime
				fwfw = open('./detectbug/timeout.txt','a+')
				fwfw.write(str(consumtime)+'\n')
				fwfw.write('gcc o0: '+str(rewritepath1) +' : '+realname+ '\n')
				fwfw.close()
				if os.path.exists(rewritepath00):
					shutil.copy(rewritepath00, './detectbug/timeout/'+realname)
				deletepath = './'+realname[:realname.index('.C')]+'.o'
				print(deletepath)
				if os.path.exists(deletepath):
					os.remove(deletepath)
				if os.path.exists(rewritepath00):
					os.remove(rewritepath00)
				continue


		cmd6 = '/home/clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++ -c -std=c++11 -ferror-limit=0  '+  rewritepath00
		rewritepath6 = './detectbug/clang/'+realname+'.txt'
		run_cmd_save_errorInformation(cmd6,rewritepath6)
		flagerror6 = whethererror(rewritepath6)
		execute6 = ''
		flagcrash6 = whetherllvmcrash(rewritepath6)
		if bool(1-flagerror6) and bool(1-flagcrash6):
			cmdexecclang0 = '/home/clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++ -std=c++11 -O0 -ferror-limit=0 '+  rewritepath00
			rewritepathclango0 = './detectbug/clango0/'+realname+".txt"
			try:
				with eventlet.Timeout(15, True):
					run_cmd_save_errorInformation(cmdexecclang0,rewritepathclango0)
					cmdexecclang00 = './a.out'
					rewritepathout = './out.txt'
					if os.path.exists(cmdexecclang00):
						run_cmd_save_errorInformation(cmdexecclang00,rewritepathout)
						out = readfile(rewritepathout)
						del rewritepathout
						print('yes, execute6 under O0 is:'+str(out))
						execute6 = out
						os.remove('./a.out')
			except eventlet.timeout.Timeout:
				print('timeout')
				mediumtime = datetime.datetime.now()
				consumtime = mediumtime - start+ inserttime
				fwfw = open('./detectbug/timeout.txt','a+')
				fwfw.write(str(consumtime)+'\n')
				fwfw.write('clang o0: '+str(rewritepath1) +' : '+realname+ '\n')
				fwfw.close()
				if os.path.exists(rewritepath00):
					shutil.copy(rewritepath00, './detectbug/timeout/'+realname)
				deletepath = './'+realname[:realname.index('.C')]+'.o'
				print(deletepath)
				if os.path.exists(deletepath):
					os.remove(deletepath)
				if os.path.exists(rewritepath00):
					os.remove(rewritepath00)
				continue



		if flagcrash1 or flagcrash6:
			print('---------------------crash--------------------------')
			if flagcrash1:
				mediumtime = datetime.datetime.now()
				consumtime = mediumtime - start+ inserttime
				fw00 = open('./detectbug/crash-gcc.txt','a+')
				fw00.write(str(consumtime)+'\n')
				fw00.write(str(rewritepath1) + ' : '+realname+'\n')
				fw00.close()
			if flagcrash6:
				mediumtime = datetime.datetime.now()
				consumtime = mediumtime - start+inserttime
				fw00 = open('./detectbug/crash-clang.txt','a+')
				fw00.write(str(consumtime)+'\n')
				fw00.write(str(rewritepath1) + ' : '+realname+'\n')
				fw00.close()

			shutil.copy(rewritepath00, './detectbug/crash/'+realname)
			if os.path.exists(rewritepath00):
				os.remove(rewritepath00)
			continue


		if flagerror1 and flagerror6:
			print('program error')
			shutil.copy(rewritepath00, './detectbug/invalid/'+realname)
			if os.path.exists(rewritepath1):
				os.remove(rewritepath1)

			if os.path.exists(rewritepath6):
				os.remove(rewritepath6)
			if os.path.exists(rewritepath00):
				os.remove(rewritepath00)
			continue
		elif bool(1-flagerror1) and bool(1-flagerror6):
			print('program valid')
		elif bool(1-flagerror1) and bool(flagerror6):
			print('regect valid program by clang')
			shutil.copy(rewritepath00, './detectbug/reject/'+realname)
			fw00 = open('./detectbug/reject-valid.txt','a+')
			fw00.write('reject by clang : '+str(rewritepath1) +' : '+realname+ '\n')
			fw00.close()
			if os.path.exists(rewritepath00):
				os.remove(rewritepath00)
			if os.path.exists(rewritepath001):
				os.remove(rewritepath001)
			continue
		elif bool(flagerror1) and bool(1-flagerror6):
			print('regect valid program by gcc')
			shutil.copy(rewritepath00, './detectbug/reject/'+realname)
			fw00 = open('./detectbug/reject-valid.txt','a+')
			fw00.write('reject by gcc : '+str(rewritepath1) +' : '+realname+ '\n')
			fw00.close()
			if os.path.exists(rewritepath00):
				os.remove(rewritepath00)
			if os.path.exists(rewritepath001):
				os.remove(rewritepath001)
			continue
		
		if str(execute1) != str(execute6):
			print('wrong code')
			mediumtime = datetime.datetime.now()
			consumtime = mediumtime - start+ inserttime
			shutil.copy(rewritepath00, './detectbug/wrongcode/'+realname)
			fw00 = open('./detectbug/wrong-code.txt','a+')
			fw00.write(str(consumtime)+'\n')
			fw00.write('gcc and clang: '+str(rewritepath1) +' : '+realname+ '\n')
			fw00.close()
		else:
			if os.path.exists(rewritepath1):
				os.remove(rewritepath1)

			if os.path.exists(rewritepath6):
				os.remove(rewritepath6)
		
		deletepath = './'+realname[:realname.index('.C')]+'.o'
		print(deletepath)
		if os.path.exists(deletepath):
			os.remove(deletepath)
		#exit(0)
		if os.path.exists(rewritepath00):
			os.remove(rewritepath00)
		if os.path.exists(rewritepath001):
			os.remove(rewritepath001)
		mediumtime = datetime.datetime.now()
		consumtime = mediumtime - start+ inserttime
		if consumtime.__ge__(datetime.timedelta(days=0,hours=48,minutes=0,seconds=0)):
			flagwhile = False
			break

		
		del_file('./detectbug/gcc/')
		del_file('./detectbug/gcco0/')
		del_file('./detectbug/clang/')
		del_file('./detectbug/clango0/')
	end = datetime.datetime.now()
	print(str(end-start))
				

