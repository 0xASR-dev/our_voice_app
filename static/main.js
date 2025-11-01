// Utility functions
function showLoading() {
  document.getElementById('loadingMsg').classList.remove('d-none');
  document.getElementById('dashboard').classList.add('d-none');
  document.getElementById('errorMsg').classList.add('d-none');
}

function hideLoading() {
  document.getElementById('loadingMsg').classList.add('d-none');
}

function showError(message) {
  const errorEl = document.getElementById('errorMsg');
  errorEl.textContent = message;
  errorEl.classList.remove('d-none');
  hideLoading();
}

function formatNumber(num) {
  if (num >= 10000000) return (num / 10000000).toFixed(2) + ' Cr';
  if (num >= 100000) return (num / 100000).toFixed(2) + ' Lakh';
  if (num >= 1000) return (num / 1000).toFixed(2) + 'K';
  return num.toString();
}

// API functions
async function fetchDistricts() {
  try {
    const res = await fetch('/api/districts');
    if (!res.ok) throw new Error('Failed to load districts');
    const list = await res.json();
    const sel = document.getElementById('districtSelect');
    list.forEach(d => {
      const opt = document.createElement('option');
      opt.value = d.id;
      opt.textContent = `${d.name_en} — ${d.name_hi}`;
      sel.appendChild(opt);
    });
  } catch (e) {
    showError('जिलों की सूची लोड नहीं हो सकी / Failed to load districts list');
  }
}

async function fetchDataFor(districtId) {
  const res = await fetch(`/api/data/${districtId}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to fetch data');
  }
  return res.json();
}

// Render functions
function renderCards(items) {
  const cardsRow = document.getElementById('cardsRow');
  cardsRow.innerHTML = '';
  
  // Validate items
  if (!items || items.length === 0) {
    console.error('No items to render cards');
    cardsRow.innerHTML = '<div class="col-12 text-center text-muted">No data available</div>';
    return;
  }
  
  const latest = items[0];
  
  // Validate latest data - but don't throw, just log and return
  if (!latest) {
    console.error('No latest item');
    cardsRow.innerHTML = '<div class="col-12 text-center text-muted">No data available</div>';
    return;
  }
  
  if (!latest.data) {
    console.error('No data in latest item:', latest);
    cardsRow.innerHTML = '<div class="col-12 text-center text-muted">Invalid data format</div>';
    return;
  }
  
  // Metrics configuration with icons and tooltips
  const metrics = [
    {
      title: 'परिवारों को रोजगार',
      titleEn: 'Families Employed',
      icon: '👨‍👩‍👧‍👦',
      key: 'households_worked',
      value: latest.data.households_worked || 0,
      tooltip: 'इस महीने कितने परिवारों को काम मिला',
      cssClass: 'metric-employment'
    },
    {
      title: 'वेतन राशि',
      titleEn: 'Wages Paid',
      icon: '💰',
      key: 'wages_paid',
      value: latest.data.wages_paid || 0,
      tooltip: 'कुल कितना वेतन दिया गया',
      cssClass: 'metric-wages',
      isRupee: true
    },
    {
      title: 'पूरी हुई परियोजनाएँ',
      titleEn: 'Works Completed',
      icon: '🏗️',
      key: 'works_completed',
      value: latest.data.works_completed || 0,
      tooltip: 'कितने काम पूरे हुए',
      cssClass: 'metric-works'
    }
  ];
  
  metrics.forEach(m => {
    const col = document.createElement('div');
    col.className = 'col-md-4 mb-3';
    const displayValue = m.isRupee ? '₹ ' + formatNumber(m.value) : formatNumber(m.value);
    col.innerHTML = `
      <div class="card card-metric ${m.cssClass} p-3 text-center" title="${m.tooltip}">
        <div class="metric-icon">${m.icon}</div>
        <h5>${m.title}<br><small class="text-muted">${m.titleEn}</small></h5>
        <div class="display-6">${displayValue || '—'}</div>
      </div>
    `;
    cardsRow.appendChild(col);
  });
}

let chartInstance = null;
function renderChart(items) {
  // Destroy existing chart first
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
  
  // Validate data before rendering
  if (!items || items.length === 0) {
    console.error('No items to render chart');
    return;
  }
  
  // Validate each item has required data
  const validItems = items.filter(item => {
    return item && 
           item.data && 
           typeof item.data.households_worked !== 'undefined' &&
           typeof item.data.wages_paid !== 'undefined' &&
           item.month && 
           item.year;
  });
  
  if (validItems.length === 0) {
    console.error('No valid items with required data fields');
    return;
  }
  
  const ctx = document.getElementById('trendChart').getContext('2d');
  const labels = validItems.map(i => `${i.month}/${i.year}`).reverse();
  const households = validItems.map(i => i.data.households_worked).reverse();
  const wages = validItems.map(i => i.data.wages_paid / 100000).reverse();
  
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'परिवारों को रोजगार / Families Employed', 
          data: households, 
          borderColor: '#27ae60',
          backgroundColor: 'rgba(39, 174, 96, 0.1)',
          tension: 0.3,
          fill: true
        },
        { 
          label: 'वेतन (लाख में) / Wages (in Lakhs)', 
          data: wages, 
          borderColor: '#3498db',
          backgroundColor: 'rgba(52, 152, 219, 0.1)',
          tension: 0.3,
          fill: true,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: { 
          display: true,
          position: 'bottom',
          labels: {
            font: { size: 14 },
            padding: 15
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) label += ': ';
              if (context.parsed.y !== null) {
                label += formatNumber(context.parsed.y);
              }
              return label;
            }
          }
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Families'
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Wages (Lakhs)'
          },
          grid: {
            drawOnChartArea: false,
          }
        }
      }
    }
  });
}

// Event handlers
async function onDistrictChange() {
  const sel = document.getElementById('districtSelect');
  const district = sel.value;
  
  if (!district) {
    // Hide dashboard if no district selected
    document.getElementById('dashboard').classList.add('d-none');
    return;
  }
  
  // Clear previous state
  document.getElementById('dashboard').classList.add('d-none');
  document.getElementById('errorMsg').classList.add('d-none');
  showLoading();
  
  try {
    const resp = await fetchDataFor(district);
    
    // Basic validation
    if (!resp) {
      console.error('No response received');
      throw new Error('No response from server');
    }
    
    const items = resp.items || [];
    
    if (items.length === 0) {
      console.warn('No items in response');
      throw new Error('No data available for this district');
    }
    
    const districtName = sel.options[sel.selectedIndex].text;
    document.getElementById('districtTitle').textContent = districtName;
    
    // Safely handle last_updated
    if (items[0] && items[0].last_updated) {
      const lastUpdated = items[0].last_updated;
      const dateObj = new Date(lastUpdated);
      document.getElementById('lastUpdated').textContent = 
        `अंतिम अपडेट: ${dateObj.toLocaleDateString('hi-IN')}`;
    } else {
      document.getElementById('lastUpdated').textContent = '';
    }
    
    // Render cards and chart
    renderCards(items);
    renderChart(items);
    
    // Show dashboard only after successful rendering
    hideLoading();
    document.getElementById('dashboard').classList.remove('d-none');
  } catch (e) {
    console.error('Error in onDistrictChange:', e);
    showError(`❌ ${e.message}\n\nकृपया दूसरा जिला चुनें या बाद में कोशिश करें`);
  }
}

async function tryDetectLocation() {
  if (!navigator.geolocation) {
    alert('आपका ब्राउज़र स्थान खोज का समर्थन नहीं करता / Geolocation not supported');
    return;
  }
  
  const btn = document.getElementById('detectBtn');
  btn.textContent = '🔍 खोज रहे हैं...';
  btn.disabled = true;
  
  navigator.geolocation.getCurrentPosition(async (pos) => {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    
    try {
      const res = await fetch('/api/geolookup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({lat, lon})
      });
      const data = await res.json();
      
      if (data && data.district_id) {
        const sel = document.getElementById('districtSelect');
        sel.value = data.district_id;
        await onDistrictChange();
      } else {
        alert('आपके स्थान से जिला नहीं मिला। कृपया सूची से चुनें।\nCould not identify district from location.');
      }
    } catch (e) {
      alert('स्थान खोज विफल / Geo lookup failed');
    } finally {
      btn.textContent = '📍 मेरी जिला खोजें';
      btn.disabled = false;
    }
  }, (err) => {
    alert('स्थान की अनुमति नहीं मिली या उपलब्ध नहीं है\nLocation permission denied or unavailable');
    btn.textContent = '📍 मेरी जिला खोजें';
    btn.disabled = false;
  });
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', async () => {
  await fetchDistricts();
  document.getElementById('districtSelect').addEventListener('change', onDistrictChange);
  document.getElementById('detectBtn').addEventListener('click', tryDetectLocation);
});
