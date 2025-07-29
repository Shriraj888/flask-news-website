@echo off
REM Production deployment script for Flask News Website (Windows)
REM Make sure to run this script from the project root directory

echo 🚀 Flask News Website - Production Deployment
echo ==============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check environment variables
echo 🔧 Checking environment configuration...
if not exist ".env" (
    echo ⚠️ .env file not found. Copying from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file with your configuration before running in production!
)

echo.
echo 🎉 Deployment preparation complete!
echo.
echo 📋 Next steps:
echo    1. Configure your .env file with API keys
echo    2. Set up a reverse proxy (nginx) if needed  
echo    3. Configure SSL certificates
echo    4. Start the application with: gunicorn -c gunicorn.conf.py app:app
echo.
echo 🔗 Local URLs:
echo    Development: http://localhost:5000
echo    Production:  Configure your domain
echo.
echo 📚 For more information, see README.md
echo ==============================================

pause
