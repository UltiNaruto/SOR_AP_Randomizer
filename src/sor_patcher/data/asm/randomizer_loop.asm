    ORG     $000800B4
    movem.l a6-a0/d7-d0, -(SP)         ; save all registers to stack
; check if easy mode is on since we got unlimited lives when it is on
    move.l  #0x000E0000, A6            ; move constants address to A6
    cmpi.b  #0, 0x40(A6)               ; are we playing in easy mode
    beq     not_easy_mode              ; if not then skip
    move.b  #9, (0x00FFFF20).l         ; set to unlimited lives
not_easy_mode:
; check if the SRAM is initialized if not then init SRAM
    jsr     init_sram_func

; this is the randomizer loop that runs each frame
randomizer_loop:
    cmpi.b  #0x12, (0x00FFFF01).l      ; check if we are in menu
    bne.b   ingame_check               ; if not then check if we are ingame
    jsr     menu_loop                  ;
    jmp     end_of_randomizer_loop     ; we are in menu so don't waste time by checking ingame
ingame_check:
    cmpi.b  #0x16, (0x00FFFF01).l      ; check if we are ingame
    bne.b   post_level_check           ; if not ingame then end the randomizer loop
    jsr     ingame_loop
    jmp     end_of_randomizer_loop     ; we are in game so don't waste time by checking post level
post_level_check:
    cmpi.b  #0x1A, (0x00FFFF01).l      ; check if we are post level
    bne.b   end_of_randomizer_loop     ; if not post level then end the randomizer loop
    jsr     post_level_loop
end_of_randomizer_loop:
    move.b  (0x00FFFB0F).l, D1         ; move menu state to D1
    move.b  D1, (0x00FFFFFF).l         ; save previous menu state
    lea     (0x00FFFFF8).l, A0         ; load frame_count address into A0
    cmpi.l  #0xFFFFFFFF, (A0)          ; check if about to overload the frame_count
    beq.b   overloaded_frame_count     ; if yes then set back frame_count to 0 without incrementing
    addi.l  #1, (A0)                   ; increment frame_count
    jmp     frame_count_incremented    ; done with frame_count handling
overloaded_frame_count:
    move.l  #0, (A0)                   ; reset frame_count
frame_count_incremented:
    movem.l (SP)+, d0-d7/a0-a6         ; load all registers from stack
    jsr     0x00072914                 ; original vblank command
    jmp     0x0001a0ae                 ; return to vblank


; Function table
init_sram_func:
    jmp     0x0007FF10
fix_address:
    jmp     0x0008008A
draw_string_func:
    jmp     0x000A0000
draw_char_func:
    jmp     0x000A0008
init_custom_palette_func:
    jmp     0x000A0010
stage_text:
    dc.b    "STAGE",0
keys_text:
    dc.b    "KEYS",0
AP_text:
    dc.b    "AP",0
stage_yes_color:
    dc.b    3
stage_no_color:
    dc.b    2
    align   4
frame_count:
    dc.l    0

; this is the menu loop it checks if we're about to load a level
; if the stage key hasn't been obtained the level won't load
menu_loop:
    cmpi.b  #0xE, (0x00FFFB0F).l       ; check if we are in options screen
    blt.b   skip_drawing_ap_infos      ; if not then skip drawing ap infos
    jsr     draw_ap_infos              ; draw ap infos
skip_drawing_ap_infos:
    cmpi.b  #0x2A, (0x00FFFB0F).l      ; check if we pressed start
    bne.b   menu_loop_ret              ; if not then end the menu loop
    cmpi.b  #0x26, (0x00FFFFFF).l      ; check if we were on exit
    beq.b   cancel_exit                ; if yes then cancel the button press and reset screen
    cmpi.b  #0x28, (0x00FFFFFF).l      ; check if we were on exit (pressed)
    beq.b   cancel_exit                ; if yes then cancel the button press and reset screen
    cmpi.b  #0x22, (0x00FFFFFF).l      ; check if we were on stage select
    bne.b   cancel_start_press         ; if not then cancel the button press
    move.b  (0x00FFFF03).l, D1         ; move current stage to D1
    jsr     request_stage_change       ; request level change to the client
    jmp     menu_loop_ret              ; end the menu loop
cancel_exit:
    move.b  #0x10, (0x00FFFF01).l      ; set menu type to main menu
    jmp     menu_loop_ret              ; end the menu loop
cancel_start_press:
    move.b  (0x00FFFFFF).l, D1         ; backup menu state to D1
    move.b  D1, (0x00FFFB0F).l         ; cancel button press
menu_loop_ret:
    rts

draw_ap_infos:
    movem.l a6-a0/d7-d0, -(SP)         ; save all registers to stack
    move.l  (0x00FFFFF8).l, D0         ; get frame count into D0
    divu    #2, D0                     ; D0 = D0 // 2
    lsr.l   #8, D0                     ; D0 = D0 >> 8
    lsr.l   #8, D0                     ; D0 = D0 >> 8
    cmpi.b  #0, D0                     ; check if it is the first frame out of 2
    bne.w   end_of_draw_ap_infos       ; if not then skip drawing
    jsr     init_custom_palette_func   ; init palette
    clr.l   D0                         ; reset D0 to 0
    lea     stage_text, A0             ; passing text argument
    move.l  #0x04, D0                  ; passing x argument
    move.l  #0x1A, D1                  ; passing y argument
    move.l  #0x1, D2                   ; we use unselected text palette
    jsr     draw_string_func
    lea     keys_text, A0              ; passing text argument
    move.l  #0x0A, D0                  ; passing x argument
    move.l  #0x1A, D1                  ; passing y argument
    move.l  #0x1, D2                   ; we use unselected text palette
    jsr     draw_string_func
; start of draw keys loop TODO: fix bug
    move.l  #8, D7                     ; we loop for 9 stages
    move.l  #0x18, D0                  ; start x position at 0x0F
    move.l  #0x1A, D1                  ; y position at 0x1A
draw_keys_loop:
    move.l  #0x00200028, A0            ; set A0 to stage keys array
    add.l   D7, A0                     ; A0 points now to iterated stage key
    jsr     fix_address
    move.l  D7, D2                     ; copy D7 to D2
    addi.l  #0x31, D2                  ; add '1' to D2 to get current stage character
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
    clr.l   D6                         ; ensure that D6 is clean
    move.b  (A1), D6                   ; read stage key status
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing
    cmpi.b  #1, D6                     ; check if we have the key
    beq.b   draw_ap_infos_has_key      ; if yes then color is green
    move.b  (stage_no_color), D3       ; D3 holds the red color
    jmp     draw_stage_key             ; skip to draw stage key
draw_ap_infos_has_key:
    move.b  (stage_yes_color), D3      ; D3 holds the green color
draw_stage_key:
    jsr     draw_char_func             ; draw current string
    subi.l  #1, D0                     ; decrement x position
    dbf     D7, draw_keys_loop         ; loop until all 9 stage keys are drawn
; end of draw keys loop
    lea     AP_text, A0                ; passing text argument
    move.l  #0x04, D0                  ; passing x argument
    move.l  #0x19, D1                  ; passing y argument
    move.l  #0x1, D2                   ; we use unselected text palette
    jsr     draw_string_func
; start of draw ap seed name loop
    move.l  #0x07, D0                  ; passing x argument
    move.l  #0x19, D1                  ; passing y argument
    lea     0x000E0048, A0             ; passing text argument
    move.l  #1, D2                     ; we use unselected text palette
    jsr     draw_string_func           ; draw string
; end of draw ap seed name loop
end_of_draw_ap_infos:
    movem.l (SP)+, d0-d7/a0-a6         ; load all registers from stack
    rts


; this is the ingame loop it checks every objects to see if a location is destroyed
; if it's the case then SRAM gets modified to tell the AP client we checked the location
; when in stage 8 we check if we have beaten the twins boss
; if so then we request stage 9 to beat the final boss
; if we get denied then we don't have final boss access yet
ingame_loop:
    cmpi.b  #0, (0x00FFFA46).l         ; check if we are not paused
    bgt.w   paused                     ; if paused then end the ingame loop
    clr.l   D1                         ; reset D1 to 0 since D1 might not be clean at that point
    move.b  (0x00FFFF03).l, D1         ; move current stage to D1
    lsl.b   #2, D1                     ; multiply current stage by 4 to get the entry of the offset table
    move.l  (A6, D1), A5               ; move object types pointer to A5
    addi.b  #0x20, D1                  ; adds 0x20 to offset since we want objects table pointer
    move.l  (A6, D1), A2               ; move objects pointer to A6
    subi.b  #0x20, D1                  ; subtracts 0x20 from D1 to get back 4*current stage
    lsr.b   #2, D1                     ; divide 4*current stage by 4 to get back the current stage
    clr.l   D2                         ; reset D2 to 0 since D2 might not be clean at that point
    ; get number of entity types and add 1 to A5 so that we keep
    ; a reference to which entity types we track
    move.b  (A5)+, D2
    clr.l   D3                         ; reset D3 to 0 since D3 might not be clean at that point
    ; get number of objects and add 1 to A2 so that we keep
    ; a reference to which objects we track
    move.b  (A2)+, D3
    move.l  A2, A3                     ; copy A2 to A3 so we can loop for objects
    move.l  #0x00FFB800, A4            ; A4 holds now the beginning of the entity table
entity_table_loop:
    move.l  A4, D0                     ; copy A4 to D0
    cmpi.l  #0x00FFD980, D0            ; loop through entity table
    bge.w   ingame_loop_ret            ; return once we're done checking the entity table
    
    cmpi.b  #0, (A4)                   ; if entity type is 0 then we got no entity in this entry
    beq.w   entity_table_loop_next     ; then move to next entry
    
    ; check if we are destroying the door to final boss in stage 8
    cmpi.b  #7, D1                     ; stage 8?
    bne.b   not_transitioning_to_stage_9
    cmpi.b  #1, (0x00FFFFFD).l         ; stage 9?
    beq.b   not_transitioning_to_stage_9
    cmpi.b  #2, (A4)                   ; is this a player?
    bgt.b   not_transitioning_to_stage_9
    cmpi.w  #0x0238, 0x10(A4)          ; player is at door?
    blt.b   not_transitioning_to_stage_9
    cmpi.w  #0x023A, 0x10(A4)          ; player is at door?
    bgt.b   not_transitioning_to_stage_9
    cmpi.b  #1, (0x00FFFA56).l         ; is player forced to go left?
    bne.b   not_transitioning_to_stage_9
    cmpi.b  #9, (0x00FFFFFD).l         ; is transitioning to stage 9?
    beq.b   transitioning_to_stage_9
    lea     (0x00200013).l, A0
    jsr     fix_address
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
    move.b  #1, (A1)                   ; set stage cleared
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing
    move.b  #8, D1
    jsr request_stage_change
    move.w  #0x237, 0x10(A4)
transitioning_to_stage_9:
    jmp ingame_loop_ret
not_transitioning_to_stage_9:

; check if the entity type correspond to the current stage ones
    clr.l   D7                         ; index = 0
ent_type_check_loop:
    cmp.b   D2, D7                     ; is it an entity type that we must check?
    bge.w   entity_table_loop_next     ; if we're done checking the entity types of the current stage
    clr.l   D6                         ; reset D6 to 0 so we can use it for storing the flag temporarly
    move.b  (A4), D6                   ; copy content of A4 to D6
    clr.l   D5                         ; reset D5 to 0 so we can use it for storing the flag temporarly
    move.b  (A5, D7.l), D5             ; copy content of A5 + D7 to D5
    cmp.b   D5, D6                     ; compare entity type of current entity with entity type of randomized objects
    beq     found_valid_entity_type    ; we found the entity type we were looking for
    addi.b  #1, D7                     ; increment index
    jmp     ent_type_check_loop        ; we didn't find a valid entity type for this stage so we move to next entity
found_valid_entity_type:
    
; check if we stored the original position
    clr.l   D0
    move.w  0x10(A4), D4               ; move X to D4
    cmpi.w  #0, 0x7C(A4)               ; if original X position wasn't stored yet
    bne     orig_x_pos_alr_stored      ; if it is the case then skip storing
    move.w  D4, 0x7C(A4)               ; store original X position to another spot in the entry
    move.b  #1, D0                     ; we stored original position so we mark it in D0
    move.w  #1, 0x7A(A4)               ; mark to wait until state was set to 1
orig_x_pos_alr_stored:
    swap    D4                         ; swap so we can store Y also in D4
    move.w  0x14(A4), D4               ; move Y to D4
    cmpi.w  #0, 0x7E(A4)               ; if original Y position wasn't stored yet
    bne     orig_y_pos_alr_stored      ; if it is the case then skip storing
    move.w  D4, 0x7E(A4)               ; store original Y position to another spot in the entry
    move.b  #1, D0                     ; we stored original position so we mark it in D0
    move.w  #1, 0x7A(A4)               ; mark to wait until state was set to 1
orig_y_pos_alr_stored:
    cmpi.b  #0, D0                     ; if we just stored original position
    bne.w   entity_table_loop_next     ; then don't check yet if the location was collected

; check if the entity correspond to the current stage ones that we randomize
    clr.l   D7                         ; index = 0
entity_check_loop:
    cmp.b   D3, D7                     ; is it an entity that we must check?
    bge.w   entity_table_loop_next     ; if we're done checking the entities of the current stage
    move.l  0x7C(A4), D6               ; copy original position into D6
    lsl.l   #2, D7                     ; multiply index by 4
    move.l  (A2, D7.l), D5             ; copy content of A2 + D7 to D5
    lsr.l   #2, D7                     ; divide 4*index by 4
    cmp.l   D5, D6                     ; check if the original position corresponds the one in the stage entity table
    beq     found_valid_entity         ; we found the entity we were looking for
    addi.b  #1, D7                     ; increment index
    jmp     entity_check_loop          ; keep going with the for loop
found_valid_entity:
    
    cmpi.w  #1, 0x7A(A4)               ; do we have to wait until it's fully spawned?
    bne.b   entity_is_fully_spawned    ; if yes then move to next entity
    cmpi.b  #0, 0x30(A4)               ; is it fully spawned?
    beq.w   entity_table_loop_next     ; if no then move to next entity
    move.w  #0, 0x7A(A4)               ; set as no more waiting for entity to be fully spawned
entity_is_fully_spawned:
    move.b  #0, 0x41(A4)               ; always remove the loot drop since we handle this from the client

    clr.l   D1                         ; reset D1 to 0 since D1 might not be clean at that point
    move.b  (0x00FFFF03).l, D1         ; move current stage to D1
    move.l  D1, D6                     ; copy current stage to D6
    lsl.l   #1, D6
    lea     (0x00200018).l, A0         ; beginning of the stage object cleared table
    add     D6, A0                     ; copy D6 to A0

; fetch collected locations flag
    clr.l   D0                         ; reset D0 to 0 so we can use it for storing the flag temporarly
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
    jsr     fix_address
    move.b  (A1), D0
    lsl.l   #8, D0
    addq.l  #1, A0
    jsr     fix_address
    move.b  (A1), D0
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing

    move.l  D0, D4                     ; copy D0 to D4 since we keep D4 for updating locations cleared
; check if we already marked this location as collected
    lsr.w   D7, D4                     ; (D4 >> D7) & 1 to check if we collected the location already
    andi.w  #1, D4                     ; ^
    cmpi.w  #0, D4                     ; check if the location was collected
    beq.b   was_not_collected          ; if not then skip destroying

; handling destroy phone booth
    cmpi.b  #0x11, (A4)
    bne.b   not_phone_booth
    move.b  #2, 0x30(A4)               ; set to destroy
not_phone_booth:

; handling destroy tires
    cmpi.b  #0x18, (A4)
    bne.b   not_tire
    move.b  #2, 0x30(A4)               ; set to destroy
not_tire:

; handling destroy barrel
    cmpi.b  #0x19, (A4)
    bne.b   not_barrel
    move.b  #0x11, (A4)                ; set to phone booth
    move.b  #2, 0x30(A4)               ; set to destroy
not_barrel:

; handling destroy signalisation cone
    cmpi.b  #0x1B, (A4)
    bne.b   not_signalisation_cone
    move.b  #2, 0x30(A4)               ; set to destroy
not_signalisation_cone:

; handling destroy signalisation pole
    cmpi.b  #0x1C, (A4)
    bne.b   not_signalisation_pole
    move.b  #2, 0x30(A4)               ; set to destroy
not_signalisation_pole:

; handling destroy safety barrier
    cmpi.b  #0x1D, (A4)
    bne.b   not_safety_barrier
    move.b  #2, 0x30(A4)               ; set to destroy
not_safety_barrier:

; handling destroy container
    cmpi.b  #0x1F, (A4)
    bne.b   not_container
    move.b  #2, 0x30(A4)               ; set to destroy
not_container:

; handling destroy crate
    cmpi.b  #0x41, (A4)
    bne.b   not_crate
    move.b  #3, 0x30(A4)               ; set to destroy
not_crate:

; handling destroy table
    cmpi.b  #0x45, (A4)
    bne.b   not_table
    cmpi.b  #0x40, 0x1(A4)             ; check if it's a moving table
    bne.b   not_table
    move.b  #2, 0x30(A4)               ; set to destroy
not_table:

    jmp entity_table_loop_next         ; do not check if we need to collect since it's already collected
was_not_collected:

; check if we just broke the entity if so then mark it as collected in SRAM
    cmpi.b  #1, 0x30(A4)               ; is state set to alive or none?
    ble.b   entity_table_loop_next     ; if it is then move to next entity

    lea     (0x00200019).l, A0         ; beginning of the stage object cleared table
    add     D6, A0                     ; copy D6 to A0

    move.l  #1, D6                     ; prepare D6 for bitwise operation
    lsl.l   D7, D6                     ; left shift D6 by D7
    or.l    D6, D0                     ; apply (D0 | D6) to D0

; save collected locations flag
    move.l  #1, D4
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
save_collected_locations_flag:
    jsr     fix_address
    move.b  D0, (A1)
    lsr.l   #8, D0
    subq.l  #1, A0
    dbf     D4, save_collected_locations_flag
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing

entity_table_loop_next:
    addi.w  #0x80, A4
    jmp     entity_table_loop
paused:
    move.b  (0x00FFFC04).l, D0         ; store buttons state in D0
    lsr.b   #5, D0                     ; isolate C button in D0
    andi.b  #1, D0                     ; ^
    cmpi.b  #1, D0                     ; checking if we pressed C button
    bne.b   ingame_loop_ret            ; if not then jump over
    move.b  #0x10, (0x00FFFF01).l      ; set menu type to main menu
    move.b  #0, (0x00FFFFFC).l         ; disable on final boss
ingame_loop_ret:
    rts


post_level_loop:
    lea     (0x0020000C).l, A0
    clr.l   D1                         ; reset D1 to 0 since D1 might not be clean at that point
    move.b  (0x00FFFF03).l, D1         ; move current stage to D1
    add     D1, A0                     ; used to set current stage to set cleared
    cmpi.b  #7, D1                     ; check if we just beat stage 8
    bne.b   not_final_boss             ; if not then swap back to main menu
    cmpi.b  #1, (0x00FFFFFC).l         ; check if we just beat final boss
    bne.b   not_final_boss             ; if not then swap back to main menu
    move.b  #0x24, (0x00FFFF01).l      ; set menu type to main menu
    move.l  #0x00200014, A0            ; set A0 to stage 9 clear
    jmp     final_boss_defeated
not_final_boss:
    cmpi.b  #7, D1                     ; check if we just beat stage 8
    beq.b   stage8_beaten              ; if yes then skip setting stage cleared since it's done in ingame loop
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
    jsr     fix_address
    move.b  #1, (A1)                   ; set stage cleared
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing
stage8_beaten:
    move.b  #0x10, (0x00FFFF01).l      ; set menu type to main menu
    jmp     post_level_loop_ret
final_boss_defeated:
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
    jsr     fix_address
    move.b  #1, (A1)                   ; set stage cleared
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing
post_level_loop_ret:
    move.b  #0, (0x00FFFFFC).l         ; disable on final boss
    rts


request_stage_change:
    cmpi.b  #0x8, D1                   ; if current stage > 8
    bgt.b   stage_unapproved           ; then stage_unapproved
; set requested stage for AP Client so we can give feedback to user
    addi.b  #1, D1                     ; temporarly add 1
    move.b  D1, (0x00FFFFFD).l         ; requested stage to connect to
    subi.b  #1, D1                     ; restore current stage
;
    lea     (0x00200028).l, A0         ; get stage_keys array
    add.l   D1, A0                     ; point to current stage
; read stage key status (1 => obtained, 0 => unobtained)
    jsr     fix_address
    move.b  #1, (0x00A130F1).l         ; enable SRAM reading/writing
    move.b  (A1), D0                   ; get stage key status
    move.b  #0, (0x00A130F1).l         ; disable SRAM reading/writing
;
    cmpi.b  #8, D1                     ; check if we are requesting for final boss
    beq.b   requested_final_boss       ; if yes then handle final boss key instead
    cmpi.b  #1, D0                     ; check if we have the key
    beq.b   has_key                    ; if we have the key then we can load the stage
    move.b  #0x22, (0x00FFFB0F).l      ; set menu state to stage select
    move.b  #0xBA, (0x00FFF00A).l      ; play menu select SFX
    jmp     end_of_request_stage       ; done with requesting a change
has_key:
    move.b  #1, (0x00FFFF18).l         ; set to 1 player mode
    cmpi.b  #7, D1                     ; check if we are requesting syndicate mansion
    bge.b   disable_police             ; if yes then disable police since it's not working there
    move.b  #1, (0x00FFFF21).l         ; set starting police to 1
    jmp     set_menu_to_select_char    ; then move to select char screen
disable_police:
    move.b  #0, (0x00FFFF21).l         ; set starting police to 0
    jmp     set_menu_to_select_char    ; then move to select char screen
set_menu_to_select_char:
    move.b  #0x20, (0x00FFFF01).l      ; set menu type to select a character
    jmp     end_of_request_stage       ; done with requesting a change
requested_final_boss:
    cmpi.b  #1, D0                     ; check if we have the key
    beq.b   has_final_boss_key         ; if we have the final boss key
    move.b  #0x10, (0x00FFFF01).l      ; set menu type to main menu
    jmp     end_of_request_stage       ; done with requesting a change
has_final_boss_key:
    move.b  #1, (0x00FFFFFC).l         ; enable on final boss
    jmp     end_of_request_stage
end_of_request_stage:
    rts

