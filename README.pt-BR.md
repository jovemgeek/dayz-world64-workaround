# Comece aqui — guia em português

Este ajuste é para **administradores de servidor DayZ no Windows** que encontram **Out of static buffer memory no módulo World**. Ele aumenta o espaço desse módulo de 32 MiB para 64 MiB, apenas no executável compatível. Não resolve qualquer tipo de crash e não é uma correção oficial.

Você não precisa saber programar nem digitar comandos para gerar a cópia. Precisa ter o executável original e permissão para substituí-lo na hospedagem. Teste em uma instância separada primeiro.

## O que você vai fazer

**Baixar a ferramenta → selecionar seu original → gerar uma cópia corrigida → parar o servidor → instalar a cópia → conferir os logs.**

O assistente só gera o arquivo. Ele **não instala na host, não inicia o servidor e não troca mods**. Os jogadores não precisam baixar esta ferramenta; os limites próprios dos clientes continuam existindo.

## 1. Baixe e extraia

**[Clique aqui para baixar o ZIP](https://github.com/jovemgeek/dayz-world64-workaround/archive/refs/heads/main.zip).**

Clique com o botão direito no ZIP e escolha **Extrair Tudo**. Abra a pasta extraída. Não execute de dentro do ZIP e não baixe somente o BAT: ele precisa dos arquivos Python ao lado.

## 2. Instale o Python uma vez

Se já tem Python 3.10 ou superior com launcher `py` e Tcl/Tk, pule esta etapa.

Baixe uma versão estável para Windows no [site oficial do Python](https://www.python.org/downloads/windows/). Inclua o **launcher py** e **Tcl/Tk**, usado pelas janelas de seleção. Não precisa instalar bibliotecas extras nem alterar proteções do Windows.

## 3. Gere a cópia corrigida

1. Dê dois cliques em **INICIAR-AQUI.bat**, na pasta extraída. Se o Windows esconder extensões, aparecerá apenas **INICIAR-AQUI**.
2. Leia a mensagem e clique em **OK**.
3. Selecione o **DayZServer_x64.exe original**, da instalação do servidor. Não escolha `DayZ_x64.exe`, que é o cliente, nem um executável já modificado.
4. Escolha onde salvar, por exemplo, Downloads. Será criada uma nova subpasta **World64-...**.
5. Aguarde **COPIA CRIADA E VERIFICADA**. A mensagem mostra o caminho completo.

Na nova pasta haverá:

| Arquivo | Uso |
| --- | --- |
| DayZServer_x64.exe | A cópia corrigida para instalar |
| DayZServer_x64.manifest.json | Registro da alteração e dos hashes; guarde para conferência |

**O original permanece intacto.** A ferramenta confere automaticamente o original e o resultado. Se aparecer erro, não instale arquivos daquela tentativa.

Se o servidor está na host, você pode baixar **o original daquela instância**, gerar a cópia no seu PC e enviar o resultado de volta. Não misture versões da host e do PC.

## 4. Faça backup e pare a instância

Guarde o executável original em uma pasta separada, por exemplo como `DayZServer_x64.original.exe`. Faça também backup de **profiles**, **mpmissions** e dos armazenamentos adicionais usados pelos mods.

No painel da host, pare **a instância correta** e impeça o relançamento automático durante a troca. Espere o processo encerrar. Use a parada normal do gerenciador para permitir o salvamento dos jogadores e do mundo.

## 5. Instale a cópia

Substitua apenas **DayZServer_x64.exe**, na pasta principal da instância parada, pelo arquivo de mesmo nome da nova pasta **World64-...**. O nome instalado precisa continuar sendo exatamente **DayZServer_x64.exe**. Preserve as permissões de acesso do arquivo na host.

Não envie para `addons` nem para a pasta do jogo do cliente. Não adicione nada em `-mod` ou `-serverMod`: **não é um PBO de Workshop**. Mantenha as listas de mods e suas dependências de servidor.

Se a hospedagem não permite substituir o executável, solicite suporte a ela. Este guia não contorna essa restrição.

## 6. Inicie e confira

Inicie pelo gerenciador com suas proteções e parâmetros habituais. Nos logs novos, normalmente em `profiles` ou na área de logs do painel, procure:

```text
Module: World; ... used XXXXX/67108 kB ... of static memory
```

**/67108 kB** indica a nova capacidade de 64 MiB; **/33554 kB** é a antiga. O número antes da barra varia conforme os mods. Alguns modos de log não mostram essa linha: nesse caso, confira o hash instalado ou peça ajuda ao administrador. A ausência da linha, sozinha, não comprova falha.

Confira também que World e Mission compilam, o servidor fica online, um jogador consegue entrar e os itens/persistência continuam corretos após uma parada e reinicialização normal. Uma janela aberta, sozinha, não comprova essas etapas. Acompanhe os primeiros ciclos; estabilidade prolongada não é garantida.

Se aparecer `Unknown type`, `Can't find variable` ou dependência ausente, confira o primeiro erro e os mods carregados. Mais memória não instala dependências nem corrige código de mods.

## Como desfazer

Pare a instância e seu relançamento automático. Restaure o backup original com o nome **DayZServer_x64.exe** e inicie novamente.

Restaurar o executável não desfaz alterações dos jogadores no mundo. Os backups de persistência são separados e só devem ser restaurados quando necessário.

## Problemas comuns

| O que aparece | O que fazer |
| --- | --- |
| Mensagem pedindo Python | Instale Python 3.10+ com launcher py e Tcl/Tk; abra o BAT novamente. |
| Unsupported executable | Outro build, cliente ou arquivo já modificado. Use o original suportado; não force alterando hashes. |
| Output or manifest already exists | No modo de comandos, escolha outro nome de saída. O assistente cria uma pasta nova automaticamente. |
| Acesso negado | Gere em uma pasta onde pode escrever; para instalar na host, use acesso autorizado ou suporte. |
| Continua /33554 kB | Confira a pasta da instância e se a atualização automática restaurou o EXE original. |
| Outro módulo sem memória | Apenas World muda; Game, Mission e GameLib mantêm seus limites. |
| Após atualizar, o patch não aceita | Outro build exige nova análise. Não reutilize o offset nem force a aplicação. |

## Qual versão funciona?

Somente **DayZ Server Windows x64**, versão de produto **1.30.164078.38**, tamanho **24.849.464 bytes**, com o hash original abaixo. A versão sozinha não basta; a ferramenta verifica a identidade automaticamente.

```text
Original: 67dea3d44a5956cc4f57e9ecce91a64c9e7ee9cdfff0de52a65e4cae46f7ff20
Corrigido: e5575fdeeeb4649432841f768d47f637a2ad34286eed11482d42601a85273ab6
```

## Por que não baixar o DayZServer já corrigido?

Seria mais simples, mas o executável pertence à Bohemia. A [licença do DayZ Server](https://store.steampowered.com/eula/223350_eula_0) restringe a redistribuição e também modificações e engenharia reversa. Não obtivemos autorização da Bohemia. Distribuir apenas nossa ferramenta não significa que seu uso esteja autorizado pela licença.

Aqui distribuímos nossas ferramentas e documentação; você fornece seu original e gera a cópia localmente. A alteração também faz a assinatura digital original deixar de corresponder ao arquivo. Não há garantia de aceitação pelo anti-cheat ou pela hospedagem.

## Testes e doações

Veja a [explicação técnica](README.md) e o [registro de validação](docs/VALIDATION.json), incluindo o teste A/B com 140 mil métodos e suas limitações. Esse teste não garante estabilidade em todos os servidores.

Se o trabalho ajudar seu servidor, apoie voluntariamente pelo **PayPal: gabrielrszj@icloud.com**. As doações apoiam investigação, testes e documentação. O código permanece gratuito e a doação não representa garantia de estabilidade ou suporte prioritário.
