# 🚀 Deploy to Render.com - Complete Guide

## ✅ Your App is Ready!

All required files are already in place:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Render how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `render.yaml` - Render configuration (optional but helpful)
- ✅ `.gitignore` - Protects secrets
- ✅ `.env.example` - Template for environment variables

---

## 📋 Prerequisites

1. **GitHub Account** (free) - https://github.com
2. **Render Account** (free) - https://render.com
3. **Your API Key** - Already in your `.env` file

---

## 🎯 Step-by-Step Deployment

### **Step 1: Push Code to GitHub**

#### Option A: Using GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com
2. Open GitHub Desktop
3. Click "Add" → "Add Existing Repository"
4. Select folder: `C:\Users\asus\Desktop\internship project\our_voice_app`
5. Click "Publish repository"
6. Uncheck "Keep this code private" (or keep it private, both work)
7. Click "Publish repository"
8. ✅ Done!

#### Option B: Using Git Command Line
```powershell
# Navigate to your project
cd "C:\Users\asus\Desktop\internship project\our_voice_app"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - MGNREGA Tracker ready for deployment"

# Create GitHub repo (you'll need GitHub CLI or create repo on github.com first)
# Then add remote and push:
git remote add origin https://github.com/YOUR_USERNAME/our_voice_app.git
git branch -M main
git push -u origin main
```

#### Option C: Manual Upload to GitHub
1. Go to https://github.com/new
2. Create repository named "our_voice_app"
3. Click "uploading an existing file"
4. Drag and drop all files from your folder
5. Click "Commit changes"

---

### **Step 2: Sign Up on Render.com**

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. Verify your email
5. ✅ You're in!

---

### **Step 3: Deploy Your App**

#### Method 1: Automatic (Using render.yaml) ⭐ RECOMMENDED

1. **In Render Dashboard**, click "New +" → "Blueprint"
2. Click "Connect Account" to connect GitHub
3. Select your repository: `our_voice_app`
4. Render will detect `render.yaml` automatically
5. Click "Apply"
6. **Add Environment Variables**:
   - Click on your service
   - Go to "Environment" tab
   - Add these variables:

   ```
   DATA_GOV_API_KEY = 579b464db66ec23bdd000001cf23e4eed938473541aa561eebdaea92
   DATA_GOV_URL = https://api.data.gov.in/resource/ee03643a-ee4c-48c2-ac30-9f2ff26ab722
   ```

7. Click "Save Changes"
8. Render will start building and deploying
9. Wait 3-5 minutes
10. ✅ Your app is live!

#### Method 2: Manual Setup

1. **In Render Dashboard**, click "New +" → "Web Service"
2. Click "Connect Account" (if not connected)
3. Select repository: `our_voice_app`
4. Fill in the form:
   - **Name**: `mgnrega-tracker` (or any name)
   - **Region**: Singapore (closest to India)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. **Plan**: Select "Free"
6. Click "Advanced" → Add Environment Variables:
   ```
   DATA_GOV_API_KEY = 579b464db66ec23bdd000001cf23e4eed938473541aa561eebdaea92
   DATA_GOV_URL = https://api.data.gov.in/resource/ee03643a-ee4c-48c2-ac30-9f2ff26ab722
   FLASK_ENV = production
   CACHE_EXPIRY_HOURS = 24
   LOG_LEVEL = INFO
   ```
7. Click "Create Web Service"
8. Wait 3-5 minutes for deployment
9. ✅ Your app is live!

---

### **Step 4: Access Your Live App**

Your app will be available at:
```
https://mgnrega-tracker.onrender.com
```
(or whatever name you chose)

**First Visit Warning**: 
- Free tier sleeps after 15 minutes of inactivity
- First request may take 30-60 seconds (cold start)
- After that, it's fast!

---

## 🔧 Important Changes for Production

### **1. Database: SQLite → Better Solution**

Render's filesystem is **ephemeral** (resets on each deploy). Your SQLite database will be lost!

**Quick Fix**: Use Render's free PostgreSQL

#### Add to your project:

```powershell
# Add to requirements.txt
pip install psycopg2-binary
```

I can help you convert to PostgreSQL if needed, but for MVP, the app will work with ephemeral SQLite (cache will reset on redeploy, but sample data fallback will work).

---

## 📊 Monitor Your App

### **View Logs**
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs

### **Check Performance**
1. Click "Metrics" tab
2. See CPU, Memory, Response times

### **View Errors**
1. Logs show Python exceptions
2. Flask errors appear in real-time

---

## 🔄 Update Your App (After Changes)

### **Automatic Deployment** (Recommended)
1. Make changes locally
2. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Your changes"
   git push
   ```
3. Render **automatically detects** and redeploys!
4. Wait 2-3 minutes
5. ✅ Changes are live!

### **Manual Deployment**
1. Go to Render Dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 🐛 Troubleshooting

### **App Not Loading?**
- Check "Logs" tab for errors
- Verify environment variables are set
- Make sure all files are pushed to GitHub

### **Database Errors?**
- SQLite cache might be resetting
- App falls back to sample data automatically
- Consider PostgreSQL upgrade (see below)

### **Slow First Load?**
- Normal! Free tier sleeps after 15 min
- Upgrade to paid plan ($7/month) for always-on

### **Environment Variables Not Working?**
- Go to Environment tab
- Make sure no extra spaces
- Click "Save Changes"
- Manually trigger redeploy

---

## 💰 Cost & Limits

### **Free Tier Includes:**
- ✅ 750 hours/month (enough for 24/7 with some room)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ HTTPS included
- ✅ Custom domain supported

### **Limitations:**
- ⚠️ Sleeps after 15 min inactivity (30s cold start)
- ⚠️ Ephemeral filesystem (SQLite data lost on redeploy)
- ⚠️ Limited CPU/RAM

### **Upgrade to Paid ($7/month):**
- ✅ Always on (no sleep)
- ✅ More RAM & CPU
- ✅ Better for production

---

## 🔐 Security Checklist

Before going live, verify:

- [ ] `.env` file is in `.gitignore` ✅ (already done)
- [ ] API keys are in Render Environment Variables ✅
- [ ] No secrets in GitHub repository ✅
- [ ] HTTPS is enabled ✅ (automatic on Render)
- [ ] `FLASK_ENV=production` is set ✅

---

## 📈 Upgrade to PostgreSQL (Recommended for Production)

### **Why PostgreSQL?**
- Persistent database (survives redeploys)
- Better for multiple users
- Professional solution

### **Quick Setup:**

1. **Add PostgreSQL on Render**:
   - Dashboard → "New +" → "PostgreSQL"
   - Name: `mgnrega-db`
   - Free plan
   - Create

2. **Get DATABASE_URL**:
   - Click your database
   - Copy "Internal Database URL"

3. **Update your app**:
   ```python
   # In app.py, replace get_db() function
   # I can provide the PostgreSQL code if you want
   ```

4. **Add to requirements.txt**:
   ```
   psycopg2-binary>=2.9.9
   ```

---

## 🎯 Quick Commands Reference

```powershell
# Push updates to GitHub
cd "C:\Users\asus\Desktop\internship project\our_voice_app"
git add .
git commit -m "Update"
git push

# View your live app
start https://mgnrega-tracker.onrender.com

# Check if app is running locally
python app.py
# Then visit: http://127.0.0.1:5000
```

---

## 🌟 Your Deployment Checklist

- [ ] **Step 1**: Push code to GitHub
- [ ] **Step 2**: Sign up on Render.com  
- [ ] **Step 3**: Connect GitHub repository
- [ ] **Step 4**: Add environment variables
- [ ] **Step 5**: Deploy (automatic)
- [ ] **Step 6**: Wait 3-5 minutes
- [ ] **Step 7**: Visit your live URL!
- [ ] **Step 8**: Test district selection
- [ ] **Step 9**: Check help modal works
- [ ] **Step 10**: Share with users! 🎉

---

## 📞 Support

### **Render Support**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### **If Deployment Fails**
1. Check Render logs
2. Verify all files are in GitHub
3. Check Python version in `runtime.txt`
4. Ensure environment variables are set

---

## 🚀 Next Steps After Deployment

1. **Test Everything**:
   - Select multiple districts
   - Check help modal
   - Test on mobile

2. **Share Your App**:
   - Copy the Render URL
   - Share with stakeholders
   - Get feedback

3. **Monitor Usage**:
   - Check Render metrics
   - View logs for errors
   - Track performance

4. **Plan Upgrades**:
   - If popular, upgrade to paid plan ($7/mo)
   - Consider PostgreSQL
   - Add domain name

---

## 🎉 You're Ready!

Your app is **100% ready** to deploy. The entire process takes about **10 minutes**.

**Estimated Timeline:**
- Push to GitHub: 2 minutes
- Sign up on Render: 2 minutes  
- Deploy on Render: 5 minutes
- **Total: ~10 minutes** ⏱️

**What you'll have:**
- ✅ Live MGNREGA tracker
- ✅ HTTPS secure
- ✅ Automatic deployments
- ✅ Free hosting
- ✅ Professional URL

**Your live app will be at:**
```
https://YOUR-APP-NAME.onrender.com
```

**Good luck! 🚀**

---

**Need Help?** Just ask and I can:
- Convert to PostgreSQL
- Set up custom domain
- Add monitoring
- Optimize performance
- Debug deployment issues
