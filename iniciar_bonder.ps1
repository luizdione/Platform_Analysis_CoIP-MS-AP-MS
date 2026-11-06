# =============================================================================
# iniciar_bonder.ps1 - inicia o dashboard e abre o navegador.
# Uma janela do Python (servidor) fica aberta; feche-a para encerrar o app.
# Alvo do atalho da Area de Trabalho criado por criar_atalho.ps1.
#
# Qual Python e usado, nesta ordem:
#   1. $env:BONDER_PYTHON  - caminho completo do python.exe (ex.: o de um env
#      conda especifico). Defina se o Python do PATH nao e o que tem as
#      dependencias instaladas.
#   2. o 'python' do PATH.
# =============================================================================
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

if ($env:BONDER_PYTHON) {
    $py = $env:BONDER_PYTHON
    if (-not (Test-Path $py)) {
        Write-Error ("BONDER_PYTHON aponta para um caminho que nao existe: '{0}'. " +
                     "Corrija a variavel ou remova-a para usar o 'python' do PATH." -f $py)
        exit 1
    }
} else {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $cmd) {
        Write-Error ("Python nao encontrado. Instale o Python 3.10+ e deixe-o no PATH, " +
                     "ou defina BONDER_PYTHON com o caminho completo do python.exe, ex.:`n" +
                     "  `$env:BONDER_PYTHON = 'C:\caminho\para\envs\meu-env\python.exe'`n" +
                     "Alternativa sem Python local: use o Docker (.\run.ps1).")
        exit 1
    }
    $py = $cmd.Source
}

# sobe o servidor em uma janela propria (nao bloqueia este script)
Start-Process -FilePath $py -ArgumentList "-m", "bonder.web.app" -WorkingDirectory $PSScriptRoot
# da tempo do servidor subir e abre o navegador
Start-Sleep -Seconds 4
Start-Process "http://localhost:8080"
