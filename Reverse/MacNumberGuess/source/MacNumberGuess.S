bits 64
section .text
global _start
_start:
    mov r8, 0xdeadbeefdeadc0de
new_game:
    mov rax, r8
    add rax, 777
    mov r8, rax
    and rax, 0xff
    mov r9, rax
; print "number:\n"
    mov rsi, 0x0a3a7265626d756e
    push rsi
    mov rsi, rsp
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rdx, 8 ; n
    syscall
    pop rsi
read_nb:
    sub rsp, 5
    mov rax, 0 ; read
    mov rdi, 0 ; stdin
    mov rsi, rsp ; buffer of 10
    mov rdx, 5
    syscall
    xor rax, rax
convert_byte:
    xor rbx, rbx
    mov bl, BYTE [rsi]
    cmp bl, '0'
    jl cmp_res
    cmp bl, '9'
    jg cmp_res
    sub bl, '0'
    mov rdx, 10
    mul rdx
    add rax, rbx
    add rsi, 1
    jmp convert_byte

cmp_res:
    add rsp, 5
    mov rcx, r9
    cmp rcx, rax
    jg plus
    cmp rcx, rax
    jl minus
    jmp equal
plus:
    mov rsi, 0x0a2b
    push rsi
    mov rsi, rsp ; "+\n"
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rdx, 2 ; n
    syscall
    pop rsi
    jmp read_nb
minus:
    mov rsi, 0x0a2d
    push rsi
    mov rsi, rsp ; "-\n"
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rdx, 2 ; n
    syscall
    pop rsi
    jmp read_nb
equal:
    mov rsi, 0x0a6e6977
    push rsi
    mov rsi, rsp ; "win\n"
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rdx, 4 ; n
    syscall
    pop rsi
    cmp r9, 137
    jne new_game
; print flag
    mov rsi, 0xebccd433d2978226
    mov rax, 0xe1ffe100e1ffe100 
    xor rsi, rax
    push rsi
    mov rsi, 0x82cb8c5f95cf8f5f
    mov rax, 0xe1ffe100e1ffe100 
    xor rsi, rax
    push rsi
    mov rsi, rsp ; "_n0t_m4c&ch3353\n"
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rdx, 16 ; n
    syscall
    pop rsi
    pop rsi
; exit(0)
    mov rax, 0x3C
    mov rdi, 0
    syscall 
