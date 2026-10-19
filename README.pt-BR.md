# DayZ World64 — solução temporária experimental

Este projeto aumenta de **32 MiB para 64 MiB** a área de memória estática do módulo **World** no servidor dedicado Windows x64, exclusivamente na versão cujo hash está documentado no [README principal](README.md).

O ajuste altera um byte do argumento de capacidade do alocador. As verificações de limite permanecem intactas. GameLib, Game, Mission e os clientes não são alterados. Isso não aumenta o uso de núcleos da CPU nem promete ganho de FPS.

## Como gerar

Com Python 3.10 ou superior, abra PowerShell na pasta extraída do repositório:

```powershell
py -3 .\patch_world64.py --source "C:\DayZServer\DayZServer_x64.exe" --output ".\DayZServer_x64.world64.exe"
Get-FileHash .\DayZServer_x64.world64.exe -Algorithm SHA256
```

O original permanece intacto. O destino deve ser novo e sua pasta deve existir. O programa recusa outros builds, arquivos já modificados e destinos existentes. O hash de saída deve ser:

`e5575fdeeeb4649432841f768d47f637a2ad34286eed11482d42601a85273ab6`

Teste primeiro em uma instância separada. Faça backup do executável, persistência, perfis e dados dos mods. Pare a instância e seu relançamento automático antes de substituir apenas seu executável, preservando nome, proprietário e permissões. Confira compilação, conexão, gameplay, salvamento e reinício. Para reverter, pare a instância e restaure o executável original. Isso não reverte alterações de dados ocorridas durante o jogo.

## O que foi comprovado

No teste nativo com o mesmo PBO de 140 mil métodos, o original falhou na compilação de World; a cópia modificada ultrapassou o limite antigo, registrou `42318/67108 kB` e verificou todos os métodos. O teste encerrou antes da missão completa e usou `-noBE`, portanto não valida BattlEye nem gameplay completo. Não desative proteções para instalar em produção.

Houve relato posterior do operador de inicialização e conexão normal com cliente sem alteração. Isso não comprova estabilidade prolongada, persistência ou compatibilidade universal. O principal risco pendente são falhas em caminhos da engine não cobertos pelo teste, com possível interrupção de salvamentos ou perda de progresso. A assinatura Authenticode original deixa de corresponder ao executável modificado.

Não é um PBO de Workshop nem correção oficial. Outros módulos e os limites próprios do cliente continuam existindo. Atualizações exigem nova análise: nunca force a aplicação em outro hash. Consulte a [análise técnica](docs/TECHNICAL.md) e o [registro de validação](docs/VALIDATION.json).

## Doações

Se o trabalho ajudar seu servidor, você pode apoiar voluntariamente pelo **PayPal: gabrielrszj@icloud.com**. As doações apoiam investigação, testes e documentação. O código permanece gratuito e a doação não representa garantia de estabilidade ou suporte prioritário.
