import base64,hashlib,io,json,struct,zlib,zipfile,bsdiff4,gzip
from pathlib import Path
def enc(b): return base64.b64encode(b).decode()
def sha(b):return hashlib.sha256(b).hexdigest()
def compress(b,l):
 c=zlib.compressobj(l,zlib.DEFLATED,-15);return c.compress(b)+c.flush()
def apply(old,plan):
 bz=zipfile.ZipFile(io.BytesIO(old));out=[]
 for op in plan['ops']:
  if op[0]=='literal':v=base64.b64decode(op[1])
  elif op[0]=='copy':v=old[op[1]:op[1]+op[2]]
  else:
   bd=bz.read(op[1]) if op[1] else b''
   v=apply(bd,op[3]) if op[0]=='nested' else bsdiff4.patch(bd,base64.b64decode(op[3]))
   if op[2]:v=compress(v,op[2])
  out.append(v)
 v=b''.join(out);assert sha(v)==plan['sha256'];return v

root=Path(__file__).resolve().parent
import urllib.request
with urllib.request.urlopen('https://github.com/martinhida-glitch/nox-app-descargas/releases/download/v9.0.7/xuper-fenix-v6.apk',timeout=120) as response:base=response.read()
assert sha(base)=='1bd3929a641e3354427b282e9337954e621a48ef63014af57c7c97bc2d41ab7b'
raw=b''.join(p.read_bytes() for p in sorted((root/'transport').glob('*.part')))
assert sha(raw)=='c2592bde130880f48c421fd37f3826fee26eb2e7f2a6142a9adff9a3d25283c0'
apk=apply(base,json.loads(gzip.decompress(raw)))
assert sha(apk)=='9a2cbf5eef126cc6d47302e28393c0473971d61cb8c92b8f358099b1a1437f24'
assert len(apk)==95981592
out=Path('release-v908');out.mkdir(exist_ok=True)
(out/'xuper-fenix-v6.apk').write_bytes(apk)
with zipfile.ZipFile(io.BytesIO(apk)) as archive:assert archive.testzip() is None
(out/'SHA256.txt').write_text(sha(apk)+'  xuper-fenix-v6.apk\n')
print('Approved signed build 90017 recovered byte for byte; SHA256 and CRC PASS.')
