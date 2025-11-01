# PowerShell script to check deployment readiness
# Run: .\check_deployment.ps1

Write-Host "`n🚀 Preparing for Render.com deployment...`n" -ForegroundColor Cyan

# Check if required files exist
Write-Host "✓ Checking required files..." -ForegroundColor Yellow
$files = @("requirements.txt", "Procfile", "runtime.txt", "app.py", ".gitignore", "render.yaml")
$allFilesExist = $true

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file missing!" -ForegroundColor Red
        $allFilesExist = $false
    }
}

# Check if .env is in .gitignore
if (Test-Path ".gitignore") {
    $content = Get-Content ".gitignore" -Raw
    if ($content -match "\.env") {
        Write-Host "✓ .env is protected in .gitignore" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: .env not in .gitignore" -ForegroundColor Yellow
    }
}

# Check if git is initialized
if (Test-Path ".git") {
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git not initialized. Run: git init" -ForegroundColor Yellow
}

# Check if API key is set
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DATA_GOV_API_KEY") {
        Write-Host "✓ API key configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: API key not found in .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Warning: .env file not found" -ForegroundColor Yellow
}

Write-Host "`n" -NoNewline
if ($allFilesExist) {
    Write-Host "✅ All required files present!" -ForegroundColor Green
} else {
    Write-Host "❌ Some files are missing!" -ForegroundColor Red
}

Write-Host "`n🎯 Next steps:`n" -ForegroundColor Cyan
Write-Host "1. Make sure you have a GitHub account" -ForegroundColor White
Write-Host "2. Create a new repository on GitHub" -ForegroundColor White
Write-Host "3. Run these commands:" -ForegroundColor White
Write-Host "   git init" -ForegroundColor Gray
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Ready for Render deployment'" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git remote add origin <YOUR_GITHUB_URL>" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host "4. Go to https://render.com" -ForegroundColor White
Write-Host "5. Sign up and connect your GitHub" -ForegroundColor White
Write-Host "6. Deploy your app!" -ForegroundColor White
Write-Host "`n📖 For detailed instructions, see: RENDER_DEPLOYMENT.md`n" -ForegroundColor Cyan
Write-Host "✅ Your app is ready for deployment!`n" -ForegroundColor Green
