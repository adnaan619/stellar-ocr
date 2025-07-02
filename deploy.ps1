# Stellar OCR - Automated Deployment Script
# This script helps you deploy your OCR application to the cloud

Write-Host "🚀 Stellar OCR - Cloud Deployment Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Check if Git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Step 1: Initialize Git Repository
Write-Host "`n📂 Step 1: Setting up Git repository..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Green
    git init
    
    # Create .gitignore
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Docker
.dockerignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Step 2: Stage and commit files
Write-Host "`n📝 Step 2: Staging files for commit..." -ForegroundColor Yellow

git add .
git status

$commitMessage = "🚀 Initial commit: Stellar OCR application with CI/CD"
git commit -m "$commitMessage"

Write-Host "✅ Files committed successfully" -ForegroundColor Green

# Step 3: Prepare deployment files
Write-Host "`n🔧 Step 3: Preparing deployment configuration..." -ForegroundColor Yellow

# Copy production frontend to index.html for easier Vercel deployment
Copy-Item "frontend/production.html" "frontend/index.html" -Force
Write-Host "✅ Production frontend configured" -ForegroundColor Green

# Step 4: Display next steps
Write-Host "`n🌟 Step 4: Next Steps for Cloud Deployment" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Yellow

Write-Host "`n1. 📂 CREATE GITHUB REPOSITORY:" -ForegroundColor Cyan
Write-Host "   - Go to https://github.com/new" -ForegroundColor White
Write-Host "   - Repository name: stellar-ocr" -ForegroundColor White
Write-Host "   - Make it PUBLIC (required for free Vercel)" -ForegroundColor White
Write-Host "   - Don't initialize with README (we already have files)" -ForegroundColor White

Write-Host "`n2. 🔗 CONNECT TO GITHUB:" -ForegroundColor Cyan
$username = Read-Host "   Enter your GitHub username"
if ($username) {
    $repoUrl = "https://github.com/$username/stellar-ocr.git"
    Write-Host "   Run these commands:" -ForegroundColor White
    Write-Host "   git remote add origin $repoUrl" -ForegroundColor Green
    Write-Host "   git branch -M main" -ForegroundColor Green
    Write-Host "   git push -u origin main" -ForegroundColor Green
    
    # Option to run automatically
    $autoSetup = Read-Host "`n   Would you like me to run these commands now? (y/n)"
    if ($autoSetup -eq "y" -or $autoSetup -eq "Y") {
        try {
            git remote add origin $repoUrl
            git branch -M main
            Write-Host "   Pushing to GitHub..." -ForegroundColor Yellow
            git push -u origin main
            Write-Host "   ✅ Successfully pushed to GitHub!" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ Failed to push. Please run the commands manually." -ForegroundColor Red
        }
    }
}

Write-Host "`n3. 🚂 DEPLOY BACKEND TO RAILWAY:" -ForegroundColor Cyan
Write-Host "   - Go to https://railway.app" -ForegroundColor White
Write-Host "   - Sign up with GitHub" -ForegroundColor White
Write-Host "   - Click 'New Project' → 'Deploy from GitHub'" -ForegroundColor White
Write-Host "   - Select your stellar-ocr repository" -ForegroundColor White
Write-Host "   - Set environment variables:" -ForegroundColor White
Write-Host "     FLASK_ENV=production" -ForegroundColor Green
Write-Host "     PORT=5000" -ForegroundColor Green

Write-Host "`n4. ⚡ DEPLOY FRONTEND TO VERCEL:" -ForegroundColor Cyan
Write-Host "   - Go to https://vercel.com" -ForegroundColor White
Write-Host "   - Sign up with GitHub" -ForegroundColor White
Write-Host "   - Click 'New Project' → Import your repository" -ForegroundColor White
Write-Host "   - Set build settings:" -ForegroundColor White
Write-Host "     Output Directory: frontend" -ForegroundColor Green
Write-Host "     Build Command: (leave empty)" -ForegroundColor Green

Write-Host "`n5. 🔄 CI/CD PIPELINE:" -ForegroundColor Cyan
Write-Host "   - GitHub Actions is already configured!" -ForegroundColor White
Write-Host "   - Every push to 'main' will automatically deploy" -ForegroundColor White
Write-Host "   - Check the 'Actions' tab in your GitHub repo" -ForegroundColor White

Write-Host "`n🎯 EXPECTED URLS AFTER DEPLOYMENT:" -ForegroundColor Magenta
Write-Host "   Frontend: https://stellar-ocr.vercel.app" -ForegroundColor Green
Write-Host "   Backend:  https://stellar-ocr-backend.up.railway.app" -ForegroundColor Green

Write-Host "`n📚 DOCUMENTATION:" -ForegroundColor Cyan
Write-Host "   - Full guide: DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host "   - Troubleshooting: Check the guide for common issues" -ForegroundColor White

Write-Host "`n🎉 DEPLOYMENT PREPARATION COMPLETE!" -ForegroundColor Green
Write-Host "Follow the steps above to deploy your OCR app to the cloud!" -ForegroundColor Green

# Optional: Open relevant URLs
$openUrls = Read-Host "`nWould you like me to open the deployment websites? (y/n)"
if ($openUrls -eq "y" -or $openUrls -eq "Y") {
    Start-Process "https://github.com/new"
    Start-Process "https://railway.app"
    Start-Process "https://vercel.com"
    Write-Host "✅ Opened deployment websites in your browser" -ForegroundColor Green
}

Write-Host "`n🚀 Happy Deploying!" -ForegroundColor Cyan
