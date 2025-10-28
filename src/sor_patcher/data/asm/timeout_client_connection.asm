    ORG     $0007FF10

    movem.l D0-D1, -(SP)              ; backup D0 and D1 to stack
    cmpi.b  #0, (0x00FFFFFE).l        ; are we even connected?!
    beq     end_of_timeout_func       ; nope we aren't so skip reset connection flag
    clr.l   D0                        ; make sure that D0 is 0
    clr.l   D1                        ; make sure that D1 is 0
    move.w  (0x00FFFFF8).l, D0        ; move last timed out frame to D0
    move.w  (0x00FFFB08).l, D1        ; move current frame to D1
    sub.w   D0, D1                    ; D0 - D1
    cmpi.w  #300, D1                  ; check delta
    bge.b   disconnect_AP             ; if delta > 5 seconds
    jmp     end_of_timeout_func       ; continue to randomizer loop
disconnect_AP:
    move.b  #0, (0x00FFFFFE).l        ; reset AP connected state
    move.w  (0x00FFFB08).l, D1        ; move current frame to D1
    move.w  D1, (0x00FFFFF8).l        ; save last frame that we timed out
    move.l  #120, D0                  ; 120 CPU cycles
wait_for_reconnect:
    cmpi.b  #1, (0x00FFFFFE).l        ; check if connected
    beq.b   end_of_timeout_func       ; if we're connected then resume
    dbf     D0, wait_for_reconnect    ; loop until CPU cycles done or connected
end_of_timeout_func:
    movem.l  (SP)+, D1-D0              ; restore D0 and D1 from stack
	rts