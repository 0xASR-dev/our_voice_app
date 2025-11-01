from flask import Flask, render_template, jsonify, request, g
import requests
import os
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'mgnrega_cache.db')
DATA_GOV_URL = os.environ.get('DATA_GOV_URL', 'https://api.data.gov.in/resource/ee03643a-ee4c-48c2-ac30-9f2ff26ab722')
API_KEY = os.environ.get('DATA_GOV_API_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# ---------------------- Database helpers ----------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district TEXT,
            year INTEGER,
            month INTEGER,
            data TEXT,
            last_updated TEXT
        )
    ''')
    # Add indexes for performance
    cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_district_date 
        ON cache(district, year DESC, month DESC)
    ''')
    cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_last_updated 
        ON cache(last_updated DESC)
    ''')
    db.commit()
    logger.info('Database initialized with indexes')

# Initialize DB on start
with app.app_context():
    init_db()

# ---------------------- Utility functions ----------------------

def get_cached_data(district):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT * FROM cache WHERE district = ? ORDER BY year DESC, month DESC LIMIT 12',
        (district,)
    )
    rows = cur.fetchall()
    if not rows:
        return None
    # assemble into list
    result = []
    for r in rows:
        result.append({
            'district': r['district'],
            'year': r['year'],
            'month': r['month'],
            'data': json.loads(r['data']),
            'last_updated': r['last_updated']
        })
    return result


def cache_data(district, year, month, data_obj):
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        INSERT INTO cache (district, year, month, data, last_updated)
        VALUES (?, ?, ?, ?, ?)
    ''', (district, year, month, json.dumps(data_obj), datetime.utcnow().isoformat()))
    db.commit()


def fetch_from_api(district):
    """
    Fetch data from data.gov.in MGNREGA API.
    The API returns monthly performance data for districts.
    """
    if not API_KEY:
        logger.warning(f'API_KEY not set, returning sample data for {district}')
        # Return synthetic sample data for demo
        sample = []
        now = datetime.utcnow()
        for i in range(0, 12):
            dt = now - timedelta(days=30 * i)
            sample.append({
                'district': district,
                'year': dt.year,
                'month': dt.month,
                'households_worked': max(0, 5000 + (hash(district) % 3000) - i * 50),
                'wages_paid': round(1200000 + (hash(district) % 500000) - i * 10000, 2),
                'works_completed': max(0, 200 + (hash(district) % 100) - i * 3)
            })
        return sample

    # Prepare API request
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 1000,  # Increased to get more records
        'offset': 0
    }
    
    # The data.gov.in API typically doesn't support filtering in the URL params
    # We'll fetch all records and filter in Python
    # If you know the specific filter syntax for this API, adjust here
    
    try:
        logger.info(f'Fetching data from API for district: {district}')
        logger.info(f'API URL: {DATA_GOV_URL}')
        logger.info(f'API params: {params}')
        
        resp = requests.get(DATA_GOV_URL, params=params, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
        
        logger.info(f'API Response keys: {payload.keys()}')
        
        # Parse the response structure
        records = []
        if 'records' in payload:
            records = payload['records']
        elif 'data' in payload:
            records = payload['data']
        elif isinstance(payload, list):
            records = payload
        
        logger.info(f'Found {len(records)} records in API response')
        
        if not records:
            logger.warning(f'No records found for district: {district}')
            # Return sample data as fallback
            return fetch_sample_data(district)
        
        # Log first record structure for debugging
        if records:
            logger.info(f'Sample record keys: {records[0].keys() if records[0] else "empty"}')
        
        # Process and normalize the records
        processed = []
        for r in records:
            try:
                # Try to extract district name from various possible fields
                record_district = (
                    r.get('district') or 
                    r.get('district_name') or 
                    r.get('districtname') or 
                    ''
                ).lower().replace(' ', '_')
                
                # Filter by district if we got data for multiple districts
                if district and record_district and district.lower() not in record_district:
                    continue
                
                # Extract year and month
                year = None
                month = None
                
                # Try various date field formats
                if 'year' in r:
                    year = int(r['year'])
                elif 'financial_year' in r:
                    fy = str(r['financial_year'])
                    year = int(fy[:4])
                elif 'fin_year' in r:
                    year = int(str(r['fin_year'])[:4])
                
                if 'month' in r:
                    month = int(r['month'])
                elif 'period' in r:
                    month = int(r['period'])
                
                # Use current date if not available
                if not year:
                    year = datetime.utcnow().year
                if not month:
                    month = datetime.utcnow().month
                
                # Extract metrics - try various field names
                households_worked = int(
                    r.get('households_worked') or 
                    r.get('hh_worked') or 
                    r.get('persondays_generated') or 
                    r.get('total_households') or 
                    0
                )
                
                wages_paid = float(
                    r.get('wages_paid') or 
                    r.get('total_wages') or 
                    r.get('expenditure') or 
                    r.get('total_expenditure') or 
                    0
                )
                
                works_completed = int(
                    r.get('works_completed') or 
                    r.get('completed_works') or 
                    r.get('total_works') or 
                    0
                )
                
                # Return data in nested format to match cache structure
                processed.append({
                    'district': district,
                    'year': year,
                    'month': month,
                    'data': {  # ← Nested structure
                        'households_worked': households_worked,
                        'wages_paid': wages_paid,
                        'works_completed': works_completed
                    },
                    'last_updated': datetime.utcnow().isoformat()
                })
            except Exception as e:
                logger.warning(f'Error processing record: {e}')
                continue
        
        if processed:
            logger.info(f'Successfully processed {len(processed)} records for {district}')
            return processed
        else:
            logger.warning(f'No valid records after processing for {district}')
            return fetch_sample_data(district)
            
    except requests.exceptions.Timeout:
        logger.error(f'API timeout for district: {district}')
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f'API request failed for {district}: {e}')
        return None
    except Exception as e:
        logger.error(f'Unexpected error fetching data for {district}: {e}', exc_info=True)
        return None


def fetch_sample_data(district):
    """Generate sample data for a district with correct nested structure"""
    sample = []
    now = datetime.utcnow()
    for i in range(0, 12):
        dt = now - timedelta(days=30 * i)
        sample.append({
            'district': district,
            'year': dt.year,
            'month': dt.month,
            'data': {  # ← Nested data structure to match cache format
                'households_worked': max(0, 5000 + (hash(district) % 3000) - i * 50),
                'wages_paid': round(1200000 + (hash(district) % 500000) - i * 10000, 2),
                'works_completed': max(0, 200 + (hash(district) % 100) - i * 3)
            },
            'last_updated': datetime.utcnow().isoformat()
        })
    return sample


# ---------------------- Endpoints ----------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/districts')
def districts():
    # Load all 75 Uttar Pradesh districts from JSON file
    districts_file = os.path.join(BASE_DIR, 'data', 'districts.json')
    try:
        with open(districts_file, 'r', encoding='utf-8') as f:
            districts_list = json.load(f)
        return jsonify(districts_list)
    except Exception as e:
        app.logger.error('Failed to load districts: %s', e)
        return jsonify({"error": "Failed to load districts"}), 500


@app.route('/api/data/<district_id>')
def get_district_data(district_id):
    logger.info(f'Request for district data: {district_id}')
    
    # Try cache first
    cached = get_cached_data(district_id)
    if cached:
        # If cached data was updated in the last 24 hours, return it
        last_times = [datetime.fromisoformat(item['last_updated']) for item in cached if item.get('last_updated')]
        if last_times and (datetime.utcnow() - max(last_times)) < timedelta(hours=24):
            logger.info(f'Returning fresh cached data for {district_id}')
            return jsonify({"source": "cache", "items": cached})

    # Else try to fetch from API
    logger.info(f'Cache stale or missing, fetching from API for {district_id}')
    api_data = fetch_from_api(district_id)
    if api_data:
        # cache up to 12 records - store just the nested 'data' part
        for item in api_data[:12]:
            cache_data(
                district_id, 
                item.get('year', datetime.utcnow().year), 
                item.get('month', 1), 
                item.get('data', {})  # ← Pass only the nested data object
            )
        logger.info(f'Cached {len(api_data[:12])} records for {district_id}')
        return jsonify({"source": "api", "items": api_data[:12]})

    # fallback to whatever cache exists (even if old)
    if cached:
        logger.warning(f'API failed, returning stale cache for {district_id}')
        return jsonify({"source": "cache_old", "items": cached})

    logger.error(f'No data available for {district_id}')
    return jsonify({"error": "No data available for this district"}), 503


@app.route('/api/geolookup', methods=['POST'])
def geolookup():
    """Simple lat/lon -> district lookup using a tiny sample mapping.
    Replace with a robust solution (shapefile spatial lookup or reverse geocoding) in production.
    """
    body = request.json or {}
    lat = body.get('lat')
    lon = body.get('lon')
    if lat is None or lon is None:
        return jsonify({"error": "lat/lon required"}), 400

    # sample mapping: (very naive) — just bounding boxes for demo
    sample_map = {
        'gwalior': {'name_hi': 'ग्वालियर', 'bbox': [25.0, 26.0, 78.0, 80.0]},
        'lucknow': {'name_hi': 'लखनऊ', 'bbox': [26.0, 27.5, 80.5, 82.0]},
        'agra': {'name_hi': 'आगरा', 'bbox': [26.5, 27.5, 77.5, 78.5]},
        'varanasi': {'name_hi': 'वाराणसी', 'bbox': [24.5, 25.5, 82.5, 83.5]}
    }

    for did, info in sample_map.items():
        min_lat, max_lat, min_lon, max_lon = info['bbox'][0], info['bbox'][1], info['bbox'][2], info['bbox'][3]
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            return jsonify({"district_id": did, "name_hi": info['name_hi']})

    return jsonify({"district_id": None}), 200


@app.route('/api/debug/raw-api')
def debug_raw_api():
    """Debug endpoint to see raw API response structure"""
    if not API_KEY:
        return jsonify({"error": "API_KEY not configured"}), 500
    
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 10  # Get 10 records for debugging
    }
    
    try:
        resp = requests.get(DATA_GOV_URL, params=params, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
        
        # Extract detailed information
        result = {
            "success": True,
            "url": DATA_GOV_URL,
            "response_type": type(payload).__name__,
            "response_keys": list(payload.keys()) if isinstance(payload, dict) else None,
        }
        
        # Check for records
        records = []
        if isinstance(payload, dict):
            if 'records' in payload:
                records = payload['records']
                result['records_location'] = 'payload["records"]'
            elif 'data' in payload:
                records = payload['data']
                result['records_location'] = 'payload["data"]'
            result['total_count'] = payload.get('total', payload.get('count', len(records)))
        elif isinstance(payload, list):
            records = payload
            result['records_location'] = 'payload (direct list)'
        
        result['record_count'] = len(records)
        
        # Show field information from first few records
        if records:
            result['first_record_keys'] = list(records[0].keys()) if isinstance(records[0], dict) else "not a dict"
            result['sample_records'] = records[:3]  # Show first 3 records
            
            # Try to identify district field
            district_fields = []
            for key in records[0].keys() if isinstance(records[0], dict) else []:
                if 'district' in key.lower():
                    district_fields.append(key)
            result['district_fields_found'] = district_fields
            
            # Show unique districts if found
            if district_fields:
                unique_districts = set()
                for r in records[:50]:  # Check first 50 records
                    for field in district_fields:
                        if field in r and r[field]:
                            unique_districts.add(str(r[field]))
                result['sample_districts'] = list(unique_districts)[:10]
        else:
            result['message'] = 'No records found in API response'
            result['full_response'] = payload
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "url": DATA_GOV_URL
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
