#-*-coding:gbk-*-
from ftplib import FTP
import os

# login to host using username and password
def login(host, username, password):
    ftp = FTP()
    ftp.set_debuglevel(0)
    # connect to host and login with username and password
    ftp.connect(host)
    ftp.login(username, password)
            
    return ftp

# test encode and login with username and password
# if no encode useful then use gbk
def test_encode_and_login(host, username, password):
    encodes = ['UTF-8','gbk','GB2312','GB18030','Big5','HZ']
    for i in range(len(encodes)):
        try:
            ftp = login(host, username, password)
            codes_result = ""
            ftp.encoding = encodes[i]
            lst = ftp.nlst()
            for s in lst:
                print(s)
            print(encodes[i])
            return ftp
        except Exception as e:
            print(e)
            ftp.quit()
        except(UnicodeDecodeError):
            ftp.quit()
        finally:
            pass
    ftp = login(host, username, password)
    ftp.encoding = 'gbk'
    return ftp

#download file from ftp from remote path to local path
def download_file(ftp, remote_path, local_path):
    bufsize = 2**15
    with open(local_path, "wb") as f:
        ftp.retrbinary('RETR {0}'.format(remote_path), f.write, bufsize)
    f.close()
    return ftp

# change current directory to pathname
def change_cd(ftp, pathname):
    ftp.cwd(pathname)
    pathname = ftp.pwd()
    return ftp
    
    
    

if __name__ == "__main__":
    host = "public.sjtu.edu.cn"
    username = 'wangdong'
    password = 'public'
    directory = 'static'
    ftp = test_encode_and_login(host, username, password)
    pathname = '/'
    while True:
        print("current directory:" + pathname)
        print(ftp.pwd().encode("utf-8"))
        ftp.dir()
        lst = ftp.nlst()
        op = int(input("choose operation:\n 1:download,2:change directory,3:quit"))
        if op == 1:
            filename = input("please input file name:\n")
            if filename in lst:
                remote_path = pathname + '/' + filename
                local_path = directory + '/' + filename
                ftp = download_file(ftp, remote_path, local_path)
                print("download success!")
            else:
                print("no file:" + filename)
        elif op == 2:
            dirname = input("please input file name:\n")
            if dirname in lst:
                pathname = pathname + '/' + dirname
                if pathname == '//':
                    pathname = '/'
                print("!!!!!!"+ pathname)
                ftp = change_cd(ftp, pathname)
                print("change current directory success!")
            elif dirname == '.':
                continue
            elif dirname == '..':
                if pathname == '/':
                    pathname = '/'
                else:
                    pathlist = pathname.split('/')
                    pathname = '/'
                    for i in range(len(pathlist) - 1):
                        pathname += '/' + pathlist[i]
                ftp = change_cd(ftp, pathname)
                print("change current directory success!")
            else:
                print("no dirtory:" + filename)
        elif op == 3:
            ftp.quit()
            break
        else:
            continue
            



        
    
    
