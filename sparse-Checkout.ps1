
[CmdletBinding()]
[OutputType([void])]
param(
    [Parameter(
        Position = 0,
        Mandatory = $true,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true)
    ]
    [string]$URL,
    [switch]$Add=$false,
    [switch]$DontPull=$false
)

$Repo = & "$PSScriptRoot//parse-GitHubURL.ps1" -URL $URL;


if (  $null -eq $Repo.Owner -or `
        $null -eq $Repo.Name -or `
        $null -eq $Repo.Branch -or `
        $null -eq $Repo.Path
) {
    Write-Error 'URL is incomplete' ;
    return ;
};

if(!$Add){

    git clone "https://github.com/$($Repo.Owner)/$($Repo.Name)" --no-checkout  --depth 1;
    Set-Location  $Repo.Name;
    git sparse-checkout init;
}

$Repo.Path | Out-File -FilePath ".\.git\info\sparse-checkout" -Append;
git sparse-checkout list;

if(!$DontPull){
    git checkout "origin/$($Repo.Branch)";
}


