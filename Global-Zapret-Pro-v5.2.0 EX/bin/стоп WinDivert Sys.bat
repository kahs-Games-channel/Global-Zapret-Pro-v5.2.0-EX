@echo off
chcp 65001 >nul

echo Останавливаю WinDivert,
sc query WinDivert >nul 2>&1
if %errorlevel% equ 0 (
    sc stop WinDivert
    if %errorlevel% equ 0 (
        echo Успех! Драйвер остановлен.
    ) else (
        echo Ой, ошибка при остановке. Проверь права админа или статус службы.
    )
) else (
    echo Служба WinDivert не найдена. Может, она не установлена? Давай я поищу для тебя, если нужно.
)

pause