from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pygbag', '--build', '--no_opt', '--disable-sound-format-error', '--ume_block', '0', '--width', '1000', '--height', '700', '--title', 'Get the Cash', str(root/'python-game')], check=True)
out=root/'play'
shutil.copytree(root/'python-game'/'build'/'web',out,dirs_exist_ok=True)
p=out/'index.html'
s=p.read_text()
s=s.replace('if not platform.window.MM.UME:', 'if False:')
s=s.replace('fb_ar   :  1.77', 'fb_ar   :  1.4285714286')
s=s.replace('gui_divider : 2', 'gui_divider : 1')
s=s.replace('"#7f7f7f"', '"#0b1515"')
s=s.replace('</head>', '<style>#infobox{background:#0b1515;color:#daff5a;border-radius:8px;font:16px Arial;max-width:90%;}#pyconsole{display:none}body{overflow:hidden}</style></head>')
s=s.replace('platform.window.config.gui_divider = 1', 'platform.window.config.gui_divider = 1')

p.write_text(s)
(root/'audio').mkdir(exist_ok=True)
shutil.copy2(root/'python-game'/'audio'/'JohannTheme.mp3',root/'audio'/'JohannTheme.mp3')

(out/'game.apk').unlink(missing_ok=True)
