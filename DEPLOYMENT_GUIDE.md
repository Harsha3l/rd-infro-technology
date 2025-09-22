# ECHOAL Deployment Guide

## 🚀 **Complete Deployment Instructions**

### **Frontend (Vercel) - Already Deployed ✅**
- **URL**: https://echoai-git-main-harsha-tri-lakshmis-projects.vercel.app
- **Status**: Working ✅

### **Backend (Render) - Needs Fix 🔧**
- **URL**: https://echoai-5n2z.onrender.com
- **Status**: 502 Error (Needs redeployment)

## 🔧 **Backend Fix Steps**

### **Step 1: Update Your Repository**
```bash
# Add the new deployment files
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### **Step 2: Redeploy on Render**

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Find your service**: "echoai" or similar
3. **Click "Manual Deploy"** → **"Deploy latest commit"**
4. **Wait for deployment** (2-3 minutes)

### **Step 3: Verify Backend is Working**

After deployment, test your backend:
```bash
python test_production_connection.py
```

## 📁 **Files Added for Render Deployment**

1. **`render.yaml`** - Render service configuration
2. **`Procfile`** - Process file for web service
3. **`runtime.txt`** - Python version specification
4. **Updated `main.py`** - Environment-aware host/port configuration
5. **Updated `requirements.txt`** - Fixed dependencies

## 🔗 **Frontend-Backend Connection**

### **Frontend Integration Code**
Use this in your Vercel frontend:

```javascript
// Production API configuration
const API_BASE_URL = 'https://echoai-5n2z.onrender.com';

// Example API call
async function sendMessage(content) {
    const response = await fetch(`${API_BASE_URL}/api/chat/send`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: content,
            conversation_id: null
        })
    });
    return await response.json();
}
```

### **CORS Configuration**
The backend is configured to accept requests from:
- `https://echoai-git-main-harsha-tri-lakshmis-projects.vercel.app` (your frontend)
- `https://echoai-5n2z.onrender.com` (your backend)
- Local development URLs

## 🧪 **Testing the Connection**

### **Quick Test**
```bash
# Test backend health
curl https://echoai-5n2z.onrender.com/health

# Test chat functionality
curl -X POST https://echoai-5n2z.onrender.com/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from production!", "conversation_id": null}'
```

### **Full Test Suite**
```bash
python test_production_connection.py
```

## 🚨 **Troubleshooting**

### **If Backend Still Shows 502 Error:**

1. **Check Render Logs**:
   - Go to your Render service dashboard
   - Click "Logs" tab
   - Look for error messages

2. **Common Issues**:
   - **Port binding**: Make sure using `0.0.0.0` host
   - **Dependencies**: Check if all packages installed
   - **Python version**: Ensure using Python 3.11

3. **Redeploy**:
   - Try manual redeploy
   - Check if all files are in repository

### **If Frontend Can't Connect:**

1. **Check CORS**: Verify frontend URL is in allowed origins
2. **Check Network**: Use browser dev tools to see errors
3. **Test Backend**: Make sure backend is responding first

## 📊 **Expected Results**

After successful deployment:

✅ **Backend Health**: `https://echoai-5n2z.onrender.com/health` returns 200
✅ **API Docs**: `https://echoai-5n2z.onrender.com/docs` shows FastAPI docs
✅ **Chat API**: `https://echoai-5n2z.onrender.com/api/chat/send` works
✅ **Frontend**: Can connect to backend and send messages

## 🔄 **Update Process**

To update your deployed backend:

1. **Make changes locally**
2. **Test locally**: `python main.py`
3. **Commit changes**: `git add . && git commit -m "Update" && git push`
4. **Render auto-deploys** (or manual deploy)
5. **Test production**: `python test_production_connection.py`

## 📞 **Support**

If you encounter issues:

1. **Check Render logs** for backend errors
2. **Check Vercel logs** for frontend errors
3. **Use the test script** to diagnose issues
4. **Verify all files** are in your repository

Your ECHOAL AI Assistant should be fully functional once the backend is redeployed! 🎉
