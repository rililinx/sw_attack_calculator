import re
import sys
import subprocess

# Run tests with trace to collect coverage
subprocess.run([sys.executable, '-m', 'trace', '--count', '--missing', 'run_pytest.py'], check=True)

# Parse coverage data for attack_logic
cover_file = 'attack_logic.cover'
executed = 0
total = 0
with open(cover_file) as f:
    for line in f:
        m = re.match(r"\s*(\d+|>>>>>>)", line)
        if not m:
            continue
        total += 1
        if m.group(1) != '>>>>>>':
            executed += 1
coverage = executed / total * 100 if total else 0

# Determine badge color
if coverage >= 90:
    color = '#4c1'
elif coverage >= 75:
    color = '#dfb317'
elif coverage >= 60:
    color = '#fe7d37'
else:
    color = '#e05d44'

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='110' height='20'>
<linearGradient id='a' x2='0' y2='100%'>
  <stop offset='0' stop-color='#bbb' stop-opacity='.1'/>
  <stop offset='1' stop-opacity='.1'/>
</linearGradient>
<rect rx='3' width='110' height='20' fill='#555'/>
<rect rx='3' x='60' width='50' height='20' fill='{color}'/>
<path fill='{color}' d='M60 0h4v20h-4z'/>
<rect rx='3' width='110' height='20' fill='url(#a)'/>
<g fill='#fff' text-anchor='middle' font-family='Verdana,Geneva,sans-serif' font-size='11'>
  <text x='30' y='14'>coverage</text>
  <text x='84' y='14'>{coverage:.1f}%</text>
</g>
</svg>"""

with open('coverage.svg', 'w') as f:
    f.write(svg)
print(f"Coverage: {coverage:.1f}%")
