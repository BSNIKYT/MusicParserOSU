import os
import shutil
from pathlib import Path
import tkinter
from tkinter import filedialog
import getpass

# Set up the working directory and necessary folders
working_directory = Path.cwd()
copy_to = working_directory / 'MusicParserOSU'

copy_to.mkdir(exist_ok=True)

# Determine the default osu! folder
default_osu_folder = Path('C:/Users') / getpass.getuser() / 'AppData/Local/osu!'

def get_osu_folder():
    """Get the osu! folder from the user if the default does not exist."""
    if default_osu_folder.exists():
        return default_osu_folder
    else:
        print('Введите актуальную папку OSU!')
        tkinter.Tk().withdraw()  # Hide the root window
        foldername = Path(filedialog.askdirectory() or input('>>> '))
        if not foldername.exists():
            raise FileNotFoundError('[ERROR] Папка не существует!')
        if foldername.name != 'osu!':
            raise NotADirectoryError('[ERROR] Вы не ввели папку с расположением osu!')
        return foldername

def get_audio_filename(osu_file):
    """Extract the audio filename from an osu! file."""
    with osu_file.open('r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('AudioFilename:'):
                print(line.split(':', 1)[1].strip())
                return line.split(':', 1)[1].strip()
    raise ValueError('[ERROR] AudioFilename not found in the .osu file.')

foldername = get_osu_folder()
print(f'Будет сохранено: {copy_to}')

# Set up the songs folder path
songs_folder = foldername / 'Songs'
if not songs_folder.exists():
    raise FileNotFoundError('[ERROR] Папки Songs не существует!')

if not any(songs_folder.iterdir()):
    raise Exception('[ERROR] Папка с музыкой пуста!')

err_ = []
not_err = []

def process_folder(folder):
    """Process an individual folder to copy the audio file."""
    try:
        osu_files = list(folder.glob('*.osu'))
        if not osu_files:
            raise FileNotFoundError(f'[ERROR] No .osu files found in folder: {folder}')
        
        audio_filename = get_audio_filename(osu_files[0])
        audio_file = folder / audio_filename
        if not audio_file.exists():
            raise FileNotFoundError(f'[ERROR] Audio file "{audio_filename}" not found in folder: {folder}')
        
        f_name = ' '.join(folder.name.split(' ')[1:]) + Path(audio_filename).suffix
        shutil.copyfile(audio_file, copy_to / f_name)
        not_err.append(folder)
    except Exception as e:
        print(e)
        err_.append(folder)

# Process each folder in the songs directory
for folder in songs_folder.iterdir():
    if folder.is_dir():
        process_folder(folder)

input(f'''
Успех!\nБыло обработано успешно: {len(not_err)}.\nC ошибкой: {len(err_)}.
Для продолжения нажмите Enter или любую другую клавишу >>> ''')
