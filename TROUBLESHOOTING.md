# ECHOAL Backend Troubleshooting Guide

## 🚨 Common Issues and Solutions

### 1. Server Startup Issues

**Problem**: Server fails to start or shows `KeyboardInterrupt`/`CancelledError`

**Solutions**:
```bash
# Method 1: Use the new start script
python start_server.py

# Method 2: Use the batch file (Windows)
start_server.bat

# Method 3: Direct Python execution
python main.py
```

### 2. Port Already in Use

**Problem**: `Address already in use` error

**Solutions**:
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
python -c "import uvicorn; uvicorn.run('main:app', port=8001)"
```

### 3. Import Errors

**Problem**: Module not found errors

**Solutions**:
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version (requires 3.7+)
python --version

# Verify installation
pip list | findstr fastapi
```

### 4. CORS Issues

**Problem**: Frontend can't connect to backend

**Solutions**:
- Check if server is running on `http://127.0.0.1:8000`
- Verify CORS origins in `main.py` include your frontend URL
- Use browser developer tools to check for CORS errors

### 5. Database Issues

**Problem**: Database-related errors

**Solutions**:
```bash
# For SQLite (default), ensure write permissions
# For other databases, check connection string in .env

# Reset database (if using main_with_db.py)
rm echoal.db  # Linux/Mac
del echoal.db  # Windows
```

## 🔧 Quick Fixes

### Restart Everything
```bash
# Stop any running servers (Ctrl+C)
# Then restart
python start_server.py
```

### Test Server
```bash
# Run quick test
python quick_test.py

# Or test manually
curl http://127.0.0.1:8000/health
```

### Check Logs
- Server logs appear in the terminal
- Look for error messages in red
- Check for import errors or missing dependencies

## 📋 Step-by-Step Startup

1. **Open terminal in project directory**
   ```bash
   cd F:\ECHOAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start server**
   ```bash
   python start_server.py
   ```

4. **Test server**
   ```bash
   python quick_test.py
   ```

5. **Open in browser**
   - API: http://127.0.0.1:8000
   - Docs: http://127.0.0.1:8000/docs

## 🆘 Still Having Issues?

### Check System Requirements
- Python 3.7 or higher
- Windows 10/11
- At least 4GB RAM
- Internet connection (for AI features)

### Common Error Messages

**`ModuleNotFoundError`**: Run `pip install -r requirements.txt`

**`Address already in use`**: Kill existing process or use different port

**`Permission denied`**: Run as administrator or check file permissions

**`Connection refused`**: Server not running, start with `python start_server.py`

### Get Help
1. Check this troubleshooting guide
2. Run `python quick_test.py` to diagnose issues
3. Check server logs for specific error messages
4. Verify all dependencies are installed

## ✅ Success Indicators

When everything is working, you should see:
- Server starts without errors
- "Application startup complete" message
- Server accessible at http://127.0.0.1:8000
- API documentation at http://127.0.0.1:8000/docs
- Health check returns 200 status
