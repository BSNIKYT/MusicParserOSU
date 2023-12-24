import os
import shutil
import tkinter
import tkinter.filedialog
import getpass

if str(os.name) == "nt":
  dir_pref = "\\"
else:
  dir_pref = "/"

working_directory = os.getcwd()
f_w_name = 'MusicParserOSU'
if not os.path.exists(f_w_name):
   os.mkdir(f_w_name)



copy_to = working_directory+dir_pref+f_w_name
foldername = rf'C:/Users/{str(getpass.getuser())}/AppData/Local/osu!'

if not os.path.exists(foldername):
    print('Введите актуальную папку OSU!')
    try:
      import tkinter
      import tkinter.filedialog
      foldername = tkinter.filedialog.askdirectory()
    except:
      foldername = input('>>> ')


if not os.path.exists(foldername):
    print('[ERROR] Папка не существует!')
    raise Exception('Папка не существует!')


if (foldername).split('/')[-1] != 'osu!':
    print('[ERROR] Вы не ввели папку с расположением osu!')
    raise Exception('Вы не ввели папку с расположением osu!')

print(f'Будет сохранено: {copy_to}')

sonds_folder = foldername+dir_pref+'Songs'
if not os.path.exists(sonds_folder):
    print('[ERROR] Папки Songs не существует!')
    raise Exception('Папки Songs не существует!')

os.chdir(sonds_folder)



if len(os.listdir(os.getcwd())) == 0:
    print('[ERROR] Папка с музыкой пуста!')
    raise Exception('Папка с музыкой пуста!')
err_ = []
not_err = []
for folder in os.listdir(os.getcwd()):
    try:
        os.chdir(folder)
        if os.path.exists('audio.mp3'):
            f_name = ''#.join(folder.split(' ')[1:])
            i = 1
            for d in folder.split(' ')[:]:
                if i != 1:f_name = f'{f_name} {d}'
                i = i + 1
            f_name=f_name+'.mp3'
            # print(f_name)
            shutil.copyfile(os.getcwd()+dir_pref+'audio.mp3', copy_to+dir_pref+f_name)
        os.chdir(sonds_folder)
        not_err.append(folder)
    except:
        print(f'[ERROR] Folder: {folder}')
        err_.append(folder)


print(f'Успех!\nБыло обработано успешно: {len(not_err)}.\nC ошибкой: {len(err_)}.')
