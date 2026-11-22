"""Plaat en gif van een stokset: origineel boven, Tau 1 eronder."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tau, rapport
R = '/home/claude/amir/karakters/amir/tau1/rapport/'
for s in sys.argv[1:]:
    n = sum(1 for f in os.listdir(os.path.dirname(tau.pad(s, 0))) if f.startswith(s + '_') and f[-6:-4].isdigit())
    o = [tau.pad(s, i, echt=True) for i in range(n)]
    t = [tau.uitpad(s, i) if hasattr(tau, 'uitpad') else None for i in range(n)]
    rapport.plaat(s, o, t, R + s + '_plaat.png')
    rapport.gif(o, t, R + s + '.gif')
    print(s, n)
