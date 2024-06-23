@ECHO OFF
:: NOME   :  ScriptNive
:: AUTOR  : Ryan Vinicius Carvalho Pereira
:: VERSAO : Enterprise Release Slim / Básica
REM change CHCP to UTF-8
CHCP 65001
CLS
title ScriptNive 1.5.9
color 9
echo ===================================
echo *   0-Entra      1-Sair           *
echo ===================================
set /p opcao= Desejo abrir o ScriptNive :
echo ------------------------------
if %opcao% equ 0 goto opcao0
if %opcao% equ 1 goto opcao1

:opcao0
"C:\Program Files (x86)\Nive\ScriptMus.vbs"
cls
goto menu

:opcao1
cls
exit

@echo off
cls
:menu
cls
color 9

echo Bem Vindo o ScriptNive 1.5.9

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

echo ====================================
echo *  ?.Informação Sobre ScriptNive   *
echo *  C. Crédito Do ScriptNive        *
echo *  E.Verificar diagnóstico de erro *
echo ====================================
                   
echo            MENU TAREFAS
echo ==========================================
echo * 1. Esvaziar a Lixeira                  *
echo * 2. Verifica Erro e Correção No HD      *
echo * 3. Reparador De Sistema                *
echo * 4. Limpar HD/Limpar Temp               *
echo * 5. Limpar o cache DNS                  *
echo * 6. Painel de Controle                  *
echo * 7. Iniciar o MRT                       *
echo * 8. Atualizador de Programas            *
echo * 9. Reparo completo do Windows          *
echo * 10. Sair                               *
echo ==========================================

set /p opcao= Escolha uma opcao: 
echo ------------------------------
if %opcao% equ C goto opcaoC 
if %opcao% equ c goto opcaoc
if %opcao% equ E goto opcaoE
if %opcao% equ e goto opcaoe
if %opcao% equ ? goto opcao?
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

:opcao?
cls
"C:\Program Files (x86)\Nive\Documentação-Técnica-do-ScriptNive-1.5.9.pdf"
goto menu

:opcaoC :opcaoc
goto Credito 

:opcaoE :opcaoe
start perfmon /rel
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
CHKDSK /R & Dism /Online /Cleanup-Image /ScanHealth & Dism /Online /Cleanup-Image /RestoreHealth & shutdown -r -t 30 
echo ===================================
echo *   Verificado com Sucesso        *
echo *   Erros do HD Corrigidas        *
echo ===================================
pause
goto menu

:opcao3
cls
sfc /scannow
pause
goto menu

:opcao4
cls
start cleanmgr.exe & del /q/f/s %Temp% & del /q/f/s "C:\Windows\Temp"
echo ==================================
echo *      Temp Limpo com sucesso  *  
echo *      HD  Limpo com sucesso   *
echo ==================================
pause
goto menu

:opcao5
cls
netsh winsock reset
netsh int ip reset
ipconfig /release 
ipconfig /renew 
ipconfig /flushdns 
pause
goto menu

:opcao6
cls
control.exe
pause
goto menu

:opcao7
cls  
powershell.exe -command "& {Start-Process 'C:\Windows\System32\MRT.exe' -Wait}"
pause
goto menu 

:opcao8
cls
winget upgrade & winget upgrade --all
pause
goto menu

:opcao9
cls
"C:\Program Files (x86)\Nive\Reparo completo do Windows\.bat" 
goto menu

:opcao10
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
echo                                  ╚════════════════╝                                            
echo  ̏                                                                                               ̏     
echo     ▐━━━DATA DE LANÇAMENTO━━━▌                                        
echo         ╔════════════════╗ 
echo         ║  10/Set./2022  ║
echo         ╚════════════════╝                               
echo  ̏                                                                                               ̏                                      
echo ===================
echo *  4.Menu Tarefas *
echo ===================
set /p opcao= Escolha uma opcao: 
echo ------------------------------
if %opcao% equ 1 goto opcao1
if %opcao% equ 2 goto opcao2
if %opcao% equ 3 goto opcao3
if %opcao% equ 4 goto opcao4

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
goto menu 

pause >nul                                                                                                        