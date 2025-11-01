# 🗣️ Our Voice, Our Rights — MGNREGA District Performance Tracker# MGNREGA MVP — Our Voice, Our Rights



A web application that makes MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Scheme) district-level performance data accessible to rural Indian citizens through an intuitive, low-literacy-friendly interface.

A minimal Flask-based MVP that fetches MGNREGA district data from data.gov.in (or uses cached/sample data), presents a simple bilingual (English/Hindi) UI suitable for low-literacy users, and caches responses in SQLite to avoid rate limits.

## 🎯 Features



- **75 Uttar Pradesh Districts**: Complete coverage of all UP districts## Setup

- **Visual Data Representation**: Large icons, color-coded metrics, and charts1. Create a virtualenv and install requirements:

- **Bilingual Interface**: Hindi & English support throughout

- **Smart Caching**: Resilient to API downtime with local data caching

- **Geolocation Detection**: Auto-detect user's district (optional)```bash

- **Mobile-First Design**: Responsive Bootstrap 5 interfacepython3 -m venv venv

- **Historical Trends**: 12-month performance visualizationsource venv/bin/activate

pip install -r requirements.txt

## 🚀 Quick Start```



### Prerequisites

2. Set environment variable for Data.gov API key (optional but recommended):

- Python 3.8+

- pip (Python package manager)

```bash

### Installationexport DATA_GOV_API_KEY="your_api_key_here"

```

1. **Install dependencies**

```bash

pip install -r requirements.txt3. Run the app locally:

```



2. **Set up environment variables** (optional)```bash

```bashpython app.py

# For real API access```

$env:DATA_GOV_API_KEY="your-api-key-here"

```

4. For production, use gunicorn:

3. **Run the application**

```bash

python app.py```bash

```gunicorn app:app --bind 0.0.0.0:8000

```

4. **Open your browser**

```

http://localhost:5000## Notes

```- The code contains a placeholder `DATA_GOV_URL` and a simple `fetch_from_api()` helper. Replace the `RESOURCE_ID` and query parameters with the official MGNREGA endpoint details as needed.

- For the bonus auto-detect district feature, the frontend sends lat/lon to `/api/geolookup`. That endpoint uses a small sample mapping included in `districts_sample.json`. Replace with a complete polygon lookup or a proper reverse-geocoding + district-shapefile solution for production.
## 📂 Project Structure

```
our_voice_app/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── mgnrega_cache.db      # SQLite cache (auto-created)
├── data/
│   └── districts.json    # All 75 UP districts
├── static/
│   ├── main.js           # Frontend JavaScript
│   ├── style.css         # Custom styles
│   └── chart.js          # (CDN loaded)
└── templates/
    └── index.html        # Main page template
```

## 🔧 Configuration

### API Integration

To connect to the real MGNREGA API:

1. Get an API key from [data.gov.in](https://data.gov.in)
2. Update `DATA_GOV_URL` in `app.py` with the actual resource ID
3. Set environment variable: `DATA_GOV_API_KEY=your-key`

Currently, the app uses synthetic data for demonstration purposes.

### Caching Settings

- Cache expires after 24 hours
- Stores last 12 months of data per district
- Falls back to old cache if API is unavailable

## 🎨 Design Principles

Built specifically for low-literacy rural users:

- ✅ Large fonts (18px base, 2.5rem for numbers)
- ✅ Visual icons for each metric (👨‍👩‍👧‍👦 💰 🏗️)
- ✅ Color-coded cards (green, blue, red)
- ✅ Simple Hindi translations
- ✅ Tooltips explaining each metric
- ✅ Minimal scrolling, card-based layout

## 📊 Data Metrics

The app displays three key metrics:

1. **परिवारों को रोजगार / Families Employed**
   - Number of households that received employment

2. **वेतन राशि / Wages Paid**
   - Total wages disbursed (in ₹)

3. **पूरी हुई परियोजनाएँ / Works Completed**
   - Number of completed projects

## 🚀 Production Deployment

### Option 1: Render.com (Recommended)

1. Push code to GitHub
2. Connect Render to your repository
3. Set environment variables in Render dashboard
4. Deploy with one click

### Option 2: Railway.app

```bash
railway login
railway init
railway up
```

### Option 3: Traditional VPS (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Set up application
pip3 install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/mgnrega
```

## 🧪 Testing

```bash
# Test locally
python app.py

# Access from mobile device on same network
# Find your local IP: ipconfig (Windows)
# Open: http://YOUR_LOCAL_IP:5000
```

## 📈 Future Enhancements

- [ ] Real MGNREGA API integration
- [ ] PostgreSQL for production (instead of SQLite)
- [ ] PWA support for offline access
- [ ] WhatsApp share functionality
- [ ] District comparison tool
- [ ] Voice input for district selection
- [ ] SMS alerts for updates

## 🤝 Contributing

This is a take-home project for demonstration purposes. For production use:

1. Replace synthetic data with real API
2. Add proper authentication
3. Implement rate limiting
4. Set up monitoring (Sentry, Uptime Robot)
5. Add comprehensive tests

## 📝 License

Educational/Demonstration Project

## 👤 Author

Built as part of the "Our Voice, Our Rights" take-home project assignment.

## 🙏 Acknowledgments

- Data source: [data.gov.in](https://data.gov.in)
- MGNREGA program by Government of India
- Bootstrap 5 for responsive design
- Chart.js for data visualization

---

**Made with ❤️ for rural India** 🇮🇳
