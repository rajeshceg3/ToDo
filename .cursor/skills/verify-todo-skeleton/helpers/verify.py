#!/usr/bin/env python3
import argparse,json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[4];p=argparse.ArgumentParser();p.add_argument('mode',choices=['doctor','drive']);p.add_argument('--out',default='.verification-evidence/skeleton');a=p.parse_args();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);r={'mode':a.mode,'ok':False,'checks':[]}
try:
 before=subprocess.run(['git','status','--porcelain'],cwd=root,capture_output=True,text=True,check=True).stdout
 readme=root/'README.md';assert readme.is_file(),'README missing';assert readme.read_text().strip()=='# ToDo','Skeleton contract changed: reinterview source';r['checks'].append({'readme_heading':'# ToDo'})
 if a.mode=='drive':
  files=subprocess.run(['git','ls-files'],cwd=root,capture_output=True,text=True,check=True).stdout.splitlines();product=[f for f in files if not f.startswith('.cursor/skills/verify-todo-skeleton/') and f not in ['.gitignore','README.md']];assert product==[],'New product files require real application verification, not skeleton PASS';r['checks'].append({'tracked_product_files':product,'runtime':'NO_APPLICATION_SOURCE','application_verified':False})
 after=subprocess.run(['git','status','--porcelain'],cwd=root,capture_output=True,text=True,check=True).stdout;assert before==after,'Source state changed';r['ok']=True
except Exception as e:r['failure']=str(e)
(out/(a.mode+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(0 if r['ok'] else 1)
