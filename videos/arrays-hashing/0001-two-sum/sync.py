# Pads each rendered scene with frozen frames so cumulative video length matches the narration
import json, subprocess, sys
FPS = 30
ts = json.load(open('timestamps.json'))['subtitles']
groups = [('Scene1_Hook',[0]),('Scene2_Problem',[1,2]),('Scene3_BruteForce',[3,4,5,6]),('Scene4_Insight',[7,8]),
          ('Scene5_HashMap',[9,10,11,12,13,14,15]),('Scene6_Complexity',[16,17]),('Scene7_Outro',[18,19])]
only = set(sys.argv[1:])
cum, prev_end, lines = 0.0, 0, []
for name, ix in groups:
    src = f'media/videos/script/1440p30/{name}.mp4'
    dst = f'media/synced/{name}.mp4'
    cum += sum(ts[i]['duration_s'] for i in ix)
    end = round(cum * FPS)
    lines.append(f"file '{dst}'")
    if only and name not in only:
        prev_end = end
        continue
    n = int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries',
                            'stream=nb_read_frames','-of','csv=p=0',src],capture_output=True,text=True).stdout)
    pad = (end - prev_end) - n
    prev_end = end
    vf = f'tpad=stop_mode=clone:stop={pad}' if pad > 0 else 'null'
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vf',vf,'-c:v','libx264','-crf','16','-preset','slow',
                    '-pix_fmt','yuv420p','-r',str(FPS),dst],check=True)
    subprocess.run(['cp', src.replace('.mp4','.srt'), dst.replace('.mp4','.srt')])
    print(name, 'frames', n, 'pad', pad)
open('concat.txt','w').write('\n'.join(lines) + '\n')
