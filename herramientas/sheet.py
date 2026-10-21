# Contact sheet for review: python sheet.py out.png cols img1 img2 ...   (or: --video video.mp4 t1,t2,...)
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

args = sys.argv[1:]
out, cols = args[0], int(args[1])
if args[2] == '--video':
    video, stamps = args[3], args[4].split(',')
    tmp = tempfile.mkdtemp()
    files = []
    for s in stamps:
        f = os.path.join(tmp, f'{s}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', s, '-i', video, '-frames:v', '1', f], check=True)
        if os.path.exists(f):
            files.append((s, f))
else:
    files = [(os.path.basename(f), f) for f in args[2:]]
    files.sort(key=lambda x: float(x[0].split('_')[-1].rsplit('.', 1)[0]) if x[0].startswith('t_') else 0)
w, h = 360, 480
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * h), 'black')
d = ImageDraw.Draw(sheet)
for k, (lab, f) in enumerate(files):
    im = Image.open(f).convert('RGB').resize((w, h))
    x, y = (k % cols) * w, (k // cols) * h
    sheet.paste(im, (x, y))
    d.text((x + 6, y + 4), lab, fill='yellow')
sheet.save(out)
print(out)
