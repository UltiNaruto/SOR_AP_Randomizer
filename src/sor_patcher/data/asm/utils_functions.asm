    ORG     $000A0000

draw_string_func:
    jmp    draw_string
    align  4

draw_char_func:
    jmp    draw_char
    align  4

init_custom_palette_func:
    jmp    init_custom_palette
    align  4

draw_string:
    movem.l A6-A0/D7-D0, -(SP)       ; save all registers to stack
    move.l  A0, A1                   ; copy A0 to A1
    clr.l   D3                       ; ensure that D3 is clean
    move.w  D2, D3                   ; move color to D3
ds_loop:
    cmpi.b  #0, (A1)                 ; check if nul terminator
    beq     end_of_draw_string       ; if yes then stop drawing
    move.l  A1, D7                   ; D7 = A1
    sub.l   A0, D7                   ; D7 = A1 - A0
    clr.l   D2                       ; ensure that D2 is clean
    move.b  (A1), D2                 ; move character to D2
    jsr     draw_char                ; draw current character
    addq.l  #1, A1                   ; move to next character of the string in A0
    addi.l  #1, D0                   ; move to next pixel horizontally
    jmp     ds_loop                  ; loop until character is nul terminator
end_of_draw_string:
    movem.l (SP)+, D0-D7/A0-A6       ; load all registers from stack
    rts

draw_char:
    movem.l A6-A0/D7-D0, -(SP)       ; save all registers to stack
    move.l  D0, -(SP)                ; save D0 to stack
    move.l  D2, D0                   ; move D2 to D0
    jsr     get_char_address         ; get the character sprite to draw
    move.l  (SP)+, D0                ; load D0 from stack
    move.l  A0, D2                   ; comparing with address register doesn't work so we transfer to D0
    cmpi.l  #0xFF, D2                ; did we find a character to draw
    beq.b   end_of_draw_char         ; if not then don't draw
    jsr     draw_sprite              ; draw sprite
end_of_draw_char:
    movem.l (SP)+, D0-D7/A0-A6       ; load all registers from stack
    rts

draw_sprite:
    movem.l A6-A0/D7-D0, -(SP)       ; save all registers to stack
    lsl.l   #1, D0                   ; X = (X << 1)
    lsl.l   #7, D1                   ; Y = (Y << 7)
    add.l   D1, D0                   ; store pixel position in D0
    lsl.l   #8, D0                   ; pixel position = (pixel position << 8)
    lsl.l   #8, D0                   ; pixel position = (pixel position << 8)
    addi.l  #0x40000003, D0          ; write patterns to VRAM command
    move.l  D0, 0x00C00004           ; write to VRAM command
    lsl.w   #8, D3                   ; D3 = palette << 8
    lsl.w   #5, D3                   ; D3 = D3 << 5
    add.w   D2, D3                   ; tile ID from D2
    move.w  D3, 0x00C00000           ; Low plane, palette 3, no flipping, tile ID 1
end_of_draw_sprite:
    movem.l (SP)+, D0-D7/A0-A6       ; load all registers from stack
    rts

get_char_address:
    movem.l A6-A1/D7-D0, -(SP)       ; save all registers to stack
    move.l  #char_index_table, A0    ; A0 holds the character table indexes
    move.l  A0, A1                   ; copy A0 to A1
gca_loop:
    cmp.b   (A1), D0                 ; check if the character exists in the char index table
    beq     found_char               ; if it exists then get character sprite address and return it
    cmpi.b  #0xFF, 0x1(A1)           ; check if we are at the end of the char index table
    beq     not_found_char           ; if we are then it's no use continuing to search, we return -1
    addq.l  #2, A1                   ; increment by 2 since it's a tuple[char, int8]
    jmp     gca_loop                 ; loop until a condition is satisfied
found_char:
    clr.l   D7                       ; ensure that D7 is clean
    move.b  0x1(A1), D7              ; copy temporarly result to D7
    jmp     end_of_get_char_address  ; we found the character sprite so return A0
not_found_char:
    clr.l   D7                       ; ensure that D7 is clean
    move.b  0xFF, D7                 ; set A0 to -1
end_of_get_char_address:
    move.l  D7, A0                   ; copy D7 to A0
    movem.l (SP)+, D0-D7/A1-A6       ; load all registers from stack
    rts

init_custom_palette:
    movem.l A6-A0/D7-D0, -(SP)       ; save all registers to stack
    move.l #0xC0000003, 0x00C00004   ; set palette 0 from color 0
    move.l #0x00000EEE, 0x00C00000   ; black + white
    move.l #0xC0200003, 0x00C00004   ; set palette 1 from color 0
    move.l #0x00000222, 0x00C00000   ; black + grey
    move.l #0xC0400003, 0x00C00004   ; set palette 2 from color 0
    move.l #0x0000000E, 0x00C00000   ; black + red
    move.l #0xC0600003, 0x00C00004   ; set palette 3 from color 0
    move.l #0x000000E0, 0x00C00000   ; black + green
options_menu_not_ready:
    movem.l (SP)+, D0-D7/A0-A6       ; load all registers from stack
    rts

    align   4

char_index_table:
    dc.b    "A",  0x01
    dc.b    "B",  0x02
    dc.b    "C",  0x03
    dc.b    "D",  0x04
    dc.b    "E",  0x05
    dc.b    "F",  0x06
    dc.b    "G",  0x07
    dc.b    "H",  0x08
    dc.b    "I",  0x09
    dc.b    "J",  0x0A
    dc.b    "K",  0x0B
    dc.b    "L",  0x0C
    dc.b    "M",  0x0D
    dc.b    "N",  0x0E
    dc.b    "O",  0x0F
    dc.b    "P",  0x10
    dc.b    "Q",  0x11
    dc.b    "R",  0x12
    dc.b    "S",  0x13
    dc.b    "T",  0x14
    dc.b    "U",  0x15
    dc.b    "V",  0x16
    dc.b    "W",  0x17
    dc.b    "X",  0x18
    dc.b    "Y",  0x19
    dc.b    "Z",  0x1A
    dc.b    "0",  0x1B
    dc.b    "1",  0x1C
    dc.b    "2",  0x1D
    dc.b    "3",  0x1E
    dc.b    "4",  0x1F
    dc.b    "5",  0x20
    dc.b    "6",  0x21
    dc.b    "7",  0x22
    dc.b    "8",  0x23
    dc.b    "9",  0x24
    dc.b    "*",  0x25
    dc.b    "-",  0x26
    dc.b    ">",  0x27
    dc.b    ".",  0x29
    dc.b    ",",  0x2A
    dc.b    "'",  0x2B
    dc.b    0x22, 0x2C ; " symbol
    dc.b    "?",  0x2D
    dc.b    "!",  0x2E
    dc.b    ":",  0x2F
    dc.b    ";",  0x30
    dc.b    " ",  0x31
    dc.w    0xFFFF