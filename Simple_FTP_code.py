
############################################################# FTP _ Bilgisayar Ağları _ Mustafa Serhat USLU _ 161180061 #########################################################################

import ftplib
import os


def ftp_connect():
    while True:
        site_address = input('Please enter FTP address: ')                      #### CONNECT TO HOST AND LOGIN ####
        try:
            with ftplib.FTP(site_address) as ftp:

                print("Enter Username for the site:")
                EnterUserName= input()
                print("Enter Password for the site:")
                EnterPasswd= input()
                ftp.login(user=EnterUserName, passwd=EnterPasswd)
                print(ftp.getwelcome())

                print('Current Directory', ftp.pwd())
                ftp.dir()
                print('Valid commands are cd/get/put/ls/lslocal/makedir/deldir/rename/exit - examaple: get readme.txt')
                ftp_command(ftp)
                break  # once ftp_command() exits, end this function

        except ftplib.all_errors as e:
            print('Failed to connect, check your address and credentials.', e)



def ftp_command(ftp):
    while True:  # Run until 'exit' command is received from user            #### TAKE COMMAND (example: put SomeTextFile.txt) ####
        command = input('\nEnter a command:\n') #VD: makedir test sẽ
        commands = command.split()  # split command and file/directory into list


        if commands[0] == 'cd':                                               #### Là chuyển thư mục trên server FTP ####
            try:
                ftp.cwd(commands[1])
                print('Directory of', ftp.pwd())
                ftp.dir()
                print('Current Directory', ftp.pwd())
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'Directory may not exist or you may not have permission to view it.')


        elif commands[0] == 'get':                                           #### Là tải file từ server FTP về máy tính  ####
            try:
                ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
                print('File successfully downloaded.')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'File may not exist or you may not have permission to view it.')


        elif commands[0] == 'ls':                                           #### Là in ra thư mục trên server FTP ####
            print('Directory of current remote file', ftp.pwd())
            ftp.dir()

        elif commands[0] == 'lslocal':                                      #### Là in ra thư mục trên máy tính ####
            print('Directory of current local file: \n')
            for i in os.listdir():
                print("Local file ---> " + i)


        elif commands[0] == 'put':                                         #### Là tải file từ máy tính lên server FTP ####
            uploadfile = open(commands[1], 'rb')
            ftp.storbinary('STOR ' + commands[1], uploadfile)
            print('File successfully uploaded.')


        elif commands[0] == 'makedir':                                      #### Là tạo thư mục trên server FTP ####
            # Check if directory exists (in current location)
            def directory_exists(dir):
                filelist = []
                ftp.retrlines('LIST', filelist.append)
                for f in filelist:
                    if f.split()[-1] == dir and f.upper().startswith('D'):
                        print("The directory already exists, you are being directed there now: (check with ls)")
                        return True
                return False

            # Change directories - create if it doesn't exist
            def chdir(dir):
                if directory_exists(dir) is False:
                    print("Directory successfully created:")
                    ftp.mkd(dir)
                ftp.cwd(dir)

            chdir(commands[1]) #Finally start the functions


        elif commands[0] == 'deldir':                                 #### DELETE A DIRECTORY  ####
            # Check if directory exists (in current location)
            def directory_exists(dir):
                filelist = []
                ftp.retrlines('LIST', filelist.append)
                for f in filelist:
                    if f.split()[-1] == dir and f.upper().startswith('D') or f.split()[-1] == dir:
                        print("The directory exists, deleting it:")
                        return True
                return False
                print("The directory to be deleted doesn't exist.")

            # Delete if the target directory exists.
            def chdir(dir):
                if directory_exists(dir) is True:
                    print("Directory deletion completed:")
                    ftp.rmd(dir)

            chdir(commands[1])  #Finally start the functions

        elif commands[0] == 'rename':                                 #### RENAME A FILE OR A DIRECTORY ####
            # Check if directory exists (in current location)
            def directory_exists(dir):
                filelist = []
                ftp.retrlines('LIST', filelist.append)
                for f in filelist:
                    if f.split()[-1] == dir and f.upper().startswith('D') or f.split()[-1] == dir:
                        print("The directory exists, renaming it:")
                        return True
                return False
                print("The target to be renamed doesn't exist.")

            # Rename if the target directory exists.
            def chdir(dir, todir):
                if directory_exists(dir) is True:
                    print("Renaming target:")
                    ftp.rename(dir, todir)

            chdir(commands[1], commands[3])  # Finally start the functions

        elif commands[0] == 'exit':                                 #### EXIT APPLICATION ####
            ftp.quit()
            print('Goodbye!')
            break

        else:
             print('Invalid command, try again (Valid commands are cd/get/put/ls/lslocal/makedir/deldir/rename/exit - examaple: get readme.txt).')

print('Welcome to Python FTP')
ftp_connect()