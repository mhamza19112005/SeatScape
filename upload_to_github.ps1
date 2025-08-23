# SeatScape GitHub Upload Helper
# This script will help you prepare and upload your project to GitHub

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "    SeatScape GitHub Upload Helper" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Your project is ready for upload!" -ForegroundColor Green
Write-Host ""

Write-Host "📁 Upload folder contents:" -ForegroundColor Yellow
Get-ChildItem "upload" -Recurse | ForEach-Object {
    $indent = "  " * ($_.FullName.Split('\').Count - $PWD.Path.Split('\').Count - 1)
    if ($_.PSIsContainer) {
        Write-Host "$indent📁 $($_.Name)/" -ForegroundColor Blue
    } else {
        Write-Host "$indent📄 $($_.Name)" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "🚀 READY TO UPLOAD TO GITHUB!" -ForegroundColor Green
Write-Host ""
Write-Host "Follow these steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open your browser and go to:" -ForegroundColor White
Write-Host "   https://github.com/mhamza19112005/SeatScape" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Click the green 'Code' button" -ForegroundColor White
Write-Host ""
Write-Host "3. Click 'Add file' → 'Upload files'" -ForegroundColor White
Write-Host ""
Write-Host "4. Drag and drop the ENTIRE 'upload' folder contents" -ForegroundColor White
Write-Host "   (Make sure you see all folders and files listed above)" -ForegroundColor White
Write-Host ""
Write-Host "5. Add commit message:" -ForegroundColor White
Write-Host "   'Add complete Django event booking system with unified authentication'" -ForegroundColor Cyan
Write-Host ""
Write-Host "6. Click 'Commit changes'" -ForegroundColor White
Write-Host ""
Write-Host "7. Wait for upload to complete" -ForegroundColor White
Write-Host ""
Write-Host "✅ After upload, your repository will have:" -ForegroundColor Green
Write-Host "   - Complete Django project structure" -ForegroundColor White
Write-Host "   - Unified authentication system" -ForegroundColor White
Write-Host "   - Event booking platform" -ForegroundColor White
Write-Host "   - Modern UI with glassmorphism design" -ForegroundColor White
Write-Host "   - Comprehensive documentation" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Users can then clone and run:" -ForegroundColor Yellow
Write-Host "   git clone https://github.com/mhamza19112005/SeatScape.git" -ForegroundColor Cyan
Write-Host "   cd SeatScape" -ForegroundColor Cyan
Write-Host "   python setup.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open your GitHub repository..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open GitHub repository in default browser
Start-Process "https://github.com/mhamza19112005/SeatScape"
