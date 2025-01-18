@ECHO OFF
:: NOME   :  ScriptNive
:: AUTOR  : Ryan Vinicius Carvalho Pereira
:: VERSAO : Enterprise Release Slim / Básica
REM change CHCP to UTF-8
@echo off
CHCP 65001
title ScriptNive 1.6.2
cls
:menu
cls
color 9

echo Bem Vindo o ScriptNive 1.6.2

echo                  _________-----_____
echo        ____------           __      ----_
echo  ___----             ___------              \
echo     ----________        ----                 \
echo                -----__    ^|             _____)
echo                     __-                /     \
echo         _______-----    ___--          \    /)\
echo   ------_______      ---____            \__/  /
echo                -----__    \ --    _          /\
echo                       --__--__     \_____/   \_/\
echo                               ---^|   /          ^|
echo                                  ^| ^|___________^|
echo                                  ^| ^| ((_(_)^| )_)
echo                                  ^|  \_((_(_)^|/(_)
echo                                   \             (
echo                                    \_____________)


date /t     
time /t 

echo Computador: %computername%        Usuario: %username%

echo ==========================================
echo *  S.Informação Sobre ScriptNive         *
echo *  I.Informações gerais do Computador    *
echo *  C.Crédito Do ScriptNive               *
echo *  E.Verificar diagnóstico de erro       *
echo *  O.Otimizar Windows                    *
echo ==========================================
                   
echo            MENU TAREFAS
echo =========================================
echo * 1. Esvaziar a Lixeira                  *
echo * 2. Ativar GodMode no PC                *
echo * 3. Solucionar erros no HD/SSD          *
echo * 4. Verificar Erros na RAM              *
echo * 5. Reparador Do Sistema                *
echo * 6. Limpar Arquivos Temporários e HD    *
echo * 7. Limpar o cache DNS                  *
echo * 8. Painel de Controle                  *
echo * 9. Iniciar o MRT                       *
echo * 10. Atualizador de Programas           *
echo * 11. Resolvendo Problemas de Som        *
echo * 12. Reparo completo do Windows         *
echo * 13. Sair                               *
echo ==========================================

set /p opcao= Escolha uma opcao: 
echo ------------------------------
if %opcao% equ C goto opcaoC 
if %opcao% equ c goto opcaoc
if %opcao% equ I goto opcaoI
if %opcao% equ i goto opcaoi
if %opcao% equ E goto opcaoE
if %opcao% equ e goto opcaoe
if %opcao% equ S goto opcaoS
if %opcao% equ s goto opcaos
if %opcao% equ O goto opcaoO 
if %opcao% equ o goto opcaoo
if %opcao% equ 1 goto opcao1
if %opcao% equ 2 goto opcao2
if %opcao% equ 3 goto opcao3
if %opcao% equ 4 goto opcao4
if %opcao% equ 5 goto opcao5
if %opcao% equ 6 goto opcao6 
if %opcao% equ 7 goto opcao7
if %opcao% equ 8 goto opcao8
if %opcao% equ 9 goto opcao9
if %opcao% equ 10 goto opcao10
if %opcao% equ 11 goto opcao11
if %opcao% equ 12 goto opcao12
if %opcao% equ 13 goto opcao13

:opcaoS :opcaos
cls
"C:\Program Files (x86)\Nive\Documentação-Técnica-do-ScriptNive.pdf"
goto menu

:opcaoI :opcaoi
cls
start INFPC.bat
goto menu

:opcaoC :opcaoc
goto Credito 

:opcaoE :opcaoe
cls
start perfmon /rel
goto menu

:opcaoO :opcaoo
cls 
"C:\Program Files (x86)\Nive\NiveBoost.bat" || start NiveBoost.bat 
exit
goto menu

:opcao1
cls
rd /S /Q c:\$Recycle.bin
echo ===================================
echo *      Lixeira Esvaziada          *
echo ===================================
pause
goto menu

:opcao2
cls
set "folderName=GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"
set "desktopPath=%USERPROFILE%\Desktop"
mkdir "%desktopPath%\%folderName%"
echo A pasta "GodMode" foi criada na Área de Trabalho.
pause
goto menu


:opcao3
cls
WMIC diskdrive get status & WMIC diskdrive get model,status
CHKDSK /R & shutdown -r -t 30 
echo ===================================
echo *   Verificado com Sucesso        *
echo *   Erros do HD Corrigidas        *
echo ===================================
pause
goto menu

:opcao4
cls
mdsched
pause
goto menu 

:opcao5
cls
sfc /scannow &  Dism /Online /Cleanup-Image /ScanHealth & Dism /Online /Cleanup-Image /RestoreHealth & shutdown -r -t 30 
pause
goto menu

:opcao6
cls
start cleanmgr.exe & del /q /f /s "%temp%\*" & del /q/f/s "C:\Windows\Temp\*" & del /q /f /s "%windir%\Prefetch\*" & del /q /f /s "%appdata%\Microsoft\Windows\Recent\*"
echo ==================================
echo *      Temp Limpo com sucesso  *  
echo *      HD  Limpo com sucesso   *
echo ==================================
pause
goto menu

:opcao7
cls
netsh winsock reset
netsh int ip reset
ipconfig /release 
ipconfig /renew 
ipconfig /flushdns 
ipconfig /registerdns
pause
goto menu

:opcao8
cls
control.exe
pause
goto menu

:opcao9
cls  
powershell.exe -command "& {Start-Process 'C:\Windows\System32\MRT.exe' -Wait}"
pause
goto menu 

:opcao10
cls
winget upgrade & winget upgrade --all
pause
goto menu

:opcao11
CLS
echo Reiniciando o Serviço de Áudio...
net stop audiosrv & timeout /t 5 & net start audiosrv

echo Verificando o Status dos Serviços de Áudio...
for %%S in (audiosrv AudioEndpointBuilder wuauserv) do net start %%S

echo Processo Concluído. Verifique se os problemas de áudio foram resolvidos.
pause
goto menu

:opcao12
cls
"C:\Program Files (x86)\Nive\Reparo completo do Windows\.bat" 
goto menu

:opcao13
cls
exit


@echo off
cls
:Credito
cls
color 4                                                                                                   
echo                                   .  .                                                             
echo                                  .^.::                      .~^:                                   
echo                           ...:^7!7~^:                       ..:?!~7^::                             
echo                           ^^7!7?~^:                            .^~?77?~~                           
echo                        .:?77?7!~:.                               .~!!?777.                         
echo                    .   !!?7J7!~:                                  ^~~?!!?!!...                     
echo                  :.^..:!777J?^^                                    ^~?!!?7!~...                    
echo                  :^?^:.!!77!?^^                                    .:?!!?!!^:^7.                   
echo                .:7!?..^!!77??.                                      .?!!?!! ^!?!!                  
echo               ..~??7!~~!!77J?                                       .?!!77J^~!7!Y~.                
echo               ^~?7!77~.!!77J?:.                                     .?!!?!!^!77!J?^.               
echo               .:77!77~~!!77!?:.                                    ::7!!?!!!!777J7^.               
echo               :^?7!?7!?7!77??!~                                    .:?!!?!7?!77!Y7^^               
echo               ~~77!?7!77J77J?~~           .^.            ^         ^~?!!?!7?!77!Y7.                
echo              .::!7!77!?77777?^:          :~:. ... ...  ::^         :^7!!?!!?!77!7~.                
echo             .~~^:!!?7!?!!7!!7^:          ..?~!^.:  :::~?~~         ..7!!?!!?!7?~~.^!               
echo             .~7!7^^77!?7!77!7::^           !~7?~~!^^7!?7^.        ^..~!!?!!?!7~..!!7               
echo             .^!!?!~~~~?7J77?!~~^.          ~~7?~!7~!7!7~:         ^::^!!?!7?^:!~7?!7               
echo               7!77!?!~!!777J7~!?^:.         :77~!^^7!~7..      ..:?^^7!!?!!^~!?!Y7!7               
echo               ~~?7!77!?!!77!?^^?!~^..       .:^~77!?!^:      ..^!!?::?!!?!7?777!77~~               
echo               :^?7!77?77?77?7~~!!7?^^:        ~^7~~7!:       ^^?7!~:^?!!?!777J7!J?^~               
echo                .~7!7?J77J77Y77?!~!?!7~::^.    ^^7:^7^.    ::7???^^!77?!!77J7!Y?!J~.                
echo                 ::^!7!77J?7J?!7?~!!!7?!7!^:.  .^?!~?:.  .^7!?7!^~!?!!?!!?!777?!^~:                 
echo                  ..:^^^^^!~!!!!7777~!7!7?~~^  7~77!77: :^?7!?!~77!J7!7!!7^~^:^^                    
echo                    :!~?~!~~!~~!?!7?!77!77!J7^!?!7?!77!!7!7?777!?7!J7!7~~!~~?^^.                    
echo                     ^^77??7Y?7J?!7?!7?!77!J?!57!77!77!?7!7?J?7!?7!?77?77?77~::                     
echo                       ^^^?!77!7?~!?!7?!77!77!J7!77!77!77!77777!7!!?!!?!!?~~:                       
echo                        ..^~!7777!!^^~7!7?!77!Y7!77!77!77!?7!!7~^!!?777~~~                          
echo                           .::~~!!!~..:^~!!77!57!77!77!?7!!~^^:^!7!!~^:..                           
echo                             .  ::~?^:^. :~77!J7!77!77~~~::^..~~?~^^  .                             
echo                                    .:      ~~77!77!77~~    .:::                                    
echo                                            .^77!77!77^.                                            
echo                                            ?!?7!?7!77~?                                            
echo                                         ::~?!57!57!77!?~^:                                         
echo                                         ^~77~J7!J7!7??7?~^                                         
echo                                        .?!77!77!77!77!7!!?:.                                       
echo                                       :^7~~?!??!77!77!?:^?:.                                       
echo                                       ..7^^7!Y!~77~~7!7~^7..                                       
echo                                         ^~77!Y^^77~~7!77~^                                         
echo                                         .~77!Y~~77~^7!77~^                                         
echo                                         ^~!7!7^^77~^7!77~^                                         
echo                                          .^7!7^^77^^7~7~:.                                         
echo                                            !~!^^77^ 7~~                                            
echo                                             :~ :!7: ~::                                            
echo                                             .: .^^. :.                                             
echo                                                .^^.                                                
echo                                                 ...      
echo ̏                                                                                               ̏ 
echo ▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄Créditos▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄
echo ̏                                                                                               ̏
echo     ▐━━━Criador do ScripNive━━━▌            ▐━━━Criador do Reparo completo do Windows━━━▌
echo           ╔═════════════╗                                 ╔════════╗
echo           ╠Ryan Vinicius╣                                 ╠Ivo Dias╣ 
echo           ╚═════════════╝                                 ╚════════╝    
echo ̏                                                                                               ̏  
echo                       ▐━━━Sites Utilizando Para Criar o ScripNive━━━▌
echo                                  ╔════════════════╗
echo                                  ║1.Primeiro Site ║
echo                                  ║2.Segundo Site  ║
echo                                  ║3.Terceiro Site ║
echo                                  ║4.Quarto Site   ║
echo                                  ╚════════════════╝                                            
echo  ̏                                                                                               ̏     
echo     ▐━━━DATA DE LANÇAMENTO━━━▌                                        
echo         ╔════════════════╗ 
echo         ║  10/Set./2022  ║
echo         ╚════════════════╝                               
echo  ̏                                                                                               ̏                                      
echo ===================
echo *  5.Menu Tarefas *
echo ===================
set /p opcao= Escolha uma opcao: 
echo ------------------------------
if %opcao% equ 1 goto opcao1
if %opcao% equ 2 goto opcao2
if %opcao% equ 3 goto opcao3
if %opcao% equ 4 goto opcao4
if %opcao% equ 5 goto opcao5

:opcao1
start https://docs.microsoft.com/pt-br/windows-server/administration/windows-commands/cmd
goto Credito

:opcao2
start https://www.dostips.com/
goto Credito

:opcao3
start https://www.text-image.com/
goto Credito

:opcao4
start https://github.com/RIZONCIO/Script-Nive
goto Credito

:opcao5
cls
goto menu 

pause >nul                                                                                                        