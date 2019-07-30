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
//push constant 4
@4
D=A
@SP
M=M+1
A=M-1
M=D
// call Main.fibonacci locals: 1
@Main.fibonacci_0
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
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// go Main.fibonacci
@Main.fibonacci
0; JMP
// label Main.fibonacci_0
(Main.fibonacci_0)
// label WHILE
(WHILE)
// go WHILE
@WHILE
0; JMP
(END)
@END
0;JMP