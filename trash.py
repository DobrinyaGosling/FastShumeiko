s = ['qwertyuiopasdfghjklzxcvbnm']
s[0] += s[0].upper()
print(id(s))
import time
s[0] = 'Ди НАХ'
print(id(s))
time.sleep(2)
for l in s:
    time.sleep(0.5)
    print(l)