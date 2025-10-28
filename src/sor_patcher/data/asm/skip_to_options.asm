    ORG    $000015ea
	cmpi.b #1, 0xfffffa09
	nop
    move.b #1, (0x427b, A0) ; enable debug mode to activate level select
    move.b #2, (0x0041, A0) ; set options as menu selection
    move.b #0, (0x0043, A0) ; ???
    move.b #4, (0x430f, A0) ; validate menu selection