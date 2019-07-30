@256
D=A
@SP
M=D
// call Sys.init locals: 0
@Sys.init_0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// go Sys.init
@Sys.init
0; JMP
// label Sys.init_0
(Sys.init_0)

// declare Sys.init with locals 0
// label Sys.init
(Sys.init)
//push constant 4000
@4000
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 0
@SP
AM=M-1
D=M
M=0
@R3
M=D
//push constant 5000
@5000
D=A
@SP
M=M+1
A=M-1
M=D
//pop pointer 1
@SP
AM=M-1
D=M
M=0
@R4
M=D
// call Sys.main locals: 0
@Sys.main_0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// go Sys.main
@Sys.main
0; JMP
// label Sys.main_0
(Sys.main_0)
//pop temp 1
@SP
AM=M-1
D=M
M=0
@R6
M=D
// label LOOP
(LOOP)
// go LOOP
@LOOP
0; JMP
