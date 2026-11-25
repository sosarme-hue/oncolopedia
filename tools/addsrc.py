import re,sys
def addsrc(p, lines):
    s=open(p).read()
    i=s.index('## Fuentes') if '## Fuentes' in s else s.index('## Sources')
    tail=s[i:]
    nums=[int(m) for m in re.findall(r'^(\d+)\. ',tail,re.M)]
    n=max(nums) if nums else 0
    # find end of last numbered line
    ms=list(re.finditer(r'^\d+\. .*$',tail,re.M))
    end=i+ms[-1].end()
    add=''.join('\n%d. %s'%(n+k+1,l) for k,l in enumerate(lines) if l.split('[')[0][:40] not in s)
    s=s[:end]+add+s[end:]
    open(p,'w').write(s)
