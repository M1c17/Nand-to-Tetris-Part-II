@256
D=A
@SP
M=D
//push constant 111
@111
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 333
@333
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 888
@888
D=A
@SP
M=M+1
A=M-1
M=D
//pop Static 8
@SP
AM=M-1
D=M
M=0
@StaticTest.8
M=D
//pop Static 3
@SP
AM=M-1
D=M
M=0
@StaticTest.3
M=D
//pop Static 1
@SP
AM=M-1
D=M
M=0
@StaticTest.1
M=D
//push Static 3
@StaticTest.3
D=M
@SP
M=M+1
A=M-1
M=D
//push Static 1
@StaticTest.1
D=M
@SP
M=M+1
A=M-1
M=D
//sub
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=M-D
//push Static 8
@StaticTest.8
D=M
@SP
M=M+1
A=M-1
M=D
//add
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D+M
(END)
@END
0;JMP