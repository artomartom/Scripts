#!/usr/bin/env pwsh

[CmdletBinding()]
param(
    [string[]]$cpp,
    [switch]$Dbg = $false
)
$name = Split-Path $cpp[0] -Leaf;
$ext = Split-Path  $name  -Extension;
$name = $name.Replace( $ext, '.exe');

if($IsWindows){

    $compiler=  cl.exe;
    $BuildArgs_MSVC = @(
        '-nologo',
        '-EHsc',
        '/std:c++20',
        "/Fe$($name)"
    );
    if ($dbg) {
        $BuildArgs += '/Zi';
    }
}elseif ($IsLinux  ){
    $compiler = clang;

    $BuildArgs_CLANG = @(
        '-std=c++20',
        '-lstdc++',
        "-o $($name)"
    );
    if ($dbg) {
        $BuildArgs += '-g';
    }

}else{
    throw "where am I?";
}

"$($compiler) $cpp $BuildArgs" ;
$compilerOutput =    "$compiler $cpp $BuildArgs" ;
if ($LASTEXITCODE -ne 0) {
    throw $compilerOutput;
}
Write-Output @{
    Executable = [string]$name
    Status     = $LASTEXITCODE
};

