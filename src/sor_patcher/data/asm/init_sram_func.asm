    ORG     $0007FF10
    movem.l a6-a0/d7-d0, -(SP)       ; save all registers to stack
    move.b  #1, (0x00A130F1).l       ; enable SRAM reading/writing

    lea     (0x001FFFFF).l, A0       ; load SRAM memory into A0
    move.l  #3, D7
read_magic_word:
    jsr     fix_address
    move.b  (A1), D0
    lsl.l   #8, D0
    addq.l  #1, A0
    dbf     D7, read_magic_word
    jsr     fix_address
    move.b  (A1), D0

    cmpi.l  #0x534F5231, D0          ; check if save is initialized
    beq.w   end_of_func              ; SRAM is initialized so return

    ; for loop to reset the seed name
    lea     (0x000E0048).l, A2       ; move constants address to A0
    lea     (0x00200039).l, A0       ; pointer to SRAM at the offset of seed name
    move.l  #0x3F, D0
reset_seed_name:
    move.b  (A2)+, D1
    jsr     fix_address
    move.b  D1, (A1)
    addq.l  #1, A0
    dbf     D0, reset_seed_name
    ; end of for loop

    lea     (0x000E0000).l, A2       ; move constants address to A1

    ; write seed name length to SRAM
    move.l  0x44(A2), D0             ; read length of seed name
    lea     (0x00200038).l, A0
    move.l  #1, D7
write_seed_name_length:
    jsr     fix_address
    move.b  D0, (A1)
    lsr.l   #8, D0
    subq.l  #1, A0
    dbf     D7, write_seed_name_length

    lea     (0x00200034).l, A0
    move.l  #2, D0
loop:
    jsr     fix_address
    move.b  #0, (A1)
    addq.l  #1, A0
    dbf     D0, loop

    lea     (0x00200031).l, A0
    move.l  #2, D0
loop2:
    jsr     fix_address
    move.b  #0xFF, (A1)
    addq.l  #1, A0
    dbf     D0, loop2

    lea     (0x00200018).l, A0
    move.l  #24, D0
loop3:
    jsr     fix_address
    move.b  #0, (A1)
    addq.l  #1, A0
    dbf     D0, loop3

    lea     (0x00200015).l, A0
    move.l  #2, D0
loop4:
    jsr     fix_address
    move.b  #0xFF, (A1)
    addq.l  #1, A0
    dbf     D0, loop4

    lea     (0x0020000C).l, A0
    move.l  #8, D0
loop5:
    jsr     fix_address
    move.b  #0, (A1)
    addq.l  #1, A0
    dbf     D0, loop5

    lea     (0x00200006).l, A0
    move.l  #5, D0
loop6:
    jsr     fix_address
    move.b  #0xFF, (A1)
    addq.l  #1, A0
    dbf     D0, loop6

    ; write slot number to SRAM
    lea     (0x00200005).l, A0
    move.w  0x42(A2), D0             ; read slot number
    move.l  #1, D7
write_slot_number:
    jsr     fix_address
    move.b  D0, (A1)
    lsr.l   #8, D0
    subq.l  #1, A0
    dbf     D7, write_slot_number

    ; write magic word SOR1 to SRAM
    lea     (0x00200003).l, A0
    move.l  #0x534F5231, D0          ; write string SOR1 to D1
    move.l  #3, D7
write_magic_word:
    jsr     fix_address
    move.b  D0, (A1)
    lsr.l   #8, D0
    subq.l  #1, A0
    dbf     D7, write_magic_word

end_of_func:
    move.b  #0, (0x00A130F1).l       ; disable SRAM reading/writing
    movem.l (SP)+, d0-d7/a0-a6       ; load all registers from stack
    rts

fix_address:
    move.l  D0, -(SP)                ; backup D0 to stack

    move.l  A0, A1
    move.l  A1, D0
    subi.l  #0x00200000, D0
    divu    #2, D0
    clr.w   D0
    swap    D0
    cmpi.l  #1, D0
    beq.b   odd_address
    addq.l  #1, A1
    jmp     end_of_fix_address
odd_address:
    subq.l  #1, A1
end_of_fix_address:
    move.l  (SP)+, D0                ; restore D0 from stack
    rts


