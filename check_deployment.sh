#!/bin/bash
# Quick deployment script for Render.com
# Run this before pushing to GitHub

echo "🚀 Preparing for Render.com deployment..."

# Check if required files exist
echo "✓ Checking required files..."
files=("requirements.txt" "Procfile" "runtime.txt" "app.py" ".gitignore")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing!"
        exit 1
    fi
done

# Check if .env is in .gitignore
if grep -q "\.env" .gitignore; then
    echo "✓ .env is protected in .gitignore"
else
    echo "⚠️  Warning: .env not in .gitignore"
fi

# Check if git is initialized
if [ -d ".git" ]; then
    echo "✓ Git repository initialized"
else
    echo "⚠️  Git not initialized. Run: git init"
fi

echo ""
echo "🎯 Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Ready for Render deployment'"
echo "3. git push origin main"
echo "4. Go to https://render.com and deploy!"
echo ""
echo "✅ Your app is ready for deployment!"
