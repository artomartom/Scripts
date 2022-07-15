#!/bin/bash


clang $@ -std=c++20 -lstdc++ -o $1.exe

#clang++ -S -mllvm --x86-asm-syntax=intel -O -std=c++20 -lstdc++  $@  -o $1.exe
