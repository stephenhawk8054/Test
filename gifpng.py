import os
import shutil
import sys
from pathlib import Path

import humanize
from tqdm import tqdm


def create_gif(s, fps):
    step = input('\nStep? 1-Extract frames / 2-gifski & PTS / 3-APNG > ')
    path1 = 'C:/Users/12110/Downloads/Video/temp'
    path2 = 'C:/Users/12110/Downloads/Video/temp4'
    pts_path = "C:/Program Files/Adobe1/Adobe Photoshop 2020/Photoshop.exe"
    gauntlet_path = 'C:/Program Files (x86)/PNGGauntlet/PngGauntlet.exe'

    if step is '1':
        ext = input('Extract frames? y/n > ')
        if ext is 'y':
            shutil.rmtree('temp')
            os.makedirs('temp')
            command = "powershell ffmpeg -i " + s + ".mp4 ./temp/%03d.png"
            os.system(command)
            print('Extract frames success!')

        open_dir = input('Open temp? y/n > ')
        if open_dir is 'y': 
            path = os.path.realpath(path1)
            os.startfile(path, 'open')

        create_gif(s, fps)
    elif step is '2':
        if not os.path.isdir(path2):
            os.makedirs(path2)

        files = os.listdir(path1)
        for i, filename in tqdm(enumerate(files)):
            os.rename(os.path.join(path1, filename), os.path.join(path2, ''.join(['{0:03}'.format(i+1), '.png'])))
        shutil.rmtree(path1)
        os.rename(path2, path1)
        size = humanize.naturalsize(sum(file.stat().st_size for file in Path(path1).rglob('*'))) 
        print('------------------------------------ ' + size)

        cont = input('Continue to gifski? y/n > ')
        if cont is 'y':
            command2 = "powershell ./gifski.exe -o " + s + "_ski.gif --fps " + fps + " --quality 100 ./temp/*.png"
            os.system(command2)

        pts = input('\nOpen PTS? y/n > ')
        if pts is 'y':
            os.startfile(pts_path, 'open')
        create_gif(s, fps)
    elif step is '3':
        compress = input('Compress PNG files? y/n > ')
        if compress is 'y':
            os.startfile(gauntlet_path, 'open')

        cont = input('Continue to APNG? y/n > ')
        if cont is 'y':
            command3 = "ffmpeg -r " + fps +" -i ./temp/%03d.png -plays 0 -vf setpts=PTS-STARTPTS -f apng -pred mixed " + s + ".png"
            os.system(command3)
        create_gif(s, fps)
    else:
        exit()

# Test 12
s = sys.argv[1]
fps = sys.argv[2]
create_gif(s, fps)
