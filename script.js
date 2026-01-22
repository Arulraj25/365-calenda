// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
let currentDate = new Date();
let selectedDate = new Date();
let specialDaysData = {};
let recentDays = [];

// Initialize the app
async function initApp() {
    try {
        const response = await fetch(`${API_BASE_URL}/days`);
        if (response.ok) {
            const data = await response.json();
            specialDaysData = processApiData(data.days);
            updateApiStatus(true);
            updateStats(data.days.length);
        } else {
            throw new Error('API not available');
        }
    } catch (error) {
        console.log('API Error:', error.message);
        // Load sample data
        specialDaysData = getSampleData();
        updateApiStatus(false);
        updateStats(Object.keys(specialDaysData).length);
    }
    
    setupEventListeners();
    renderCalendar(currentDate);
    updateTodayHighlight();
    updateUpcomingDays();
}

function processApiData(apiData) {
    const processed = {};
    apiData.forEach(day => {
        processed[day.date] = {
            title: day.day,
            description: day.description || generateDescription(day.day),
            icon: day.icon || getIconForDay(day.day),
            color: day.color || getColorForDay(day.day),
            animation: day.animation || getAnimationForDay(day.day)
        };
    });
    return processed;
}

function getSampleData() {
    return {
        "01-01": {
            title: "New Year's Day",
            description: "The first day of the year, celebrated worldwide with fireworks and resolutions.",
            icon: "fas fa-glass-cheers",
            color: "#FF6B6B",
            animation: "fireworks"
        },
        "02-01": {
            title: "Science Fiction Day",
            description: "Celebrate science fiction literature, movies, and imagination.",
            icon: "fas fa-flask",
            color: "#2196F3",
            animation: "science"
        },
        "03-01": {
            title: "Festival of Sleep Day",
            description: "Time to catch up on sleep and appreciate the importance of rest.",
            icon: "fas fa-bed",
            color: "#9C27B0",
            animation: "sleep"
        },
        "02-14": {
            title: "Valentine's Day",
            description: "Day of love and affection celebrated worldwide.",
            icon: "fas fa-heart",
            color: "#FF6B6B",
            animation: "hearts"
        },
        "03-14": {
            title: "Pi Day",
            description: "Celebrate the mathematical constant π (pi).",
            icon: "fas fa-pi",
            color: "#4CAF50",
            animation: "math"
        }
    };
}

function generateDescription(dayName) {
    const descriptions = {
        "New Year's Day": "The first day of the year, celebrated worldwide with fireworks, parties, and resolutions for a fresh start.",
        "Science Fiction Day": "A celebration of science fiction literature, movies, and the imaginative exploration of future possibilities.",
        "Festival of Sleep Day": "A day to catch up on sleep and appreciate the importance of rest for health and well-being."
    };
    
    return descriptions[dayName] || `Celebrate ${dayName}! A special day with unique significance.`;
}

function getIconForDay(dayName) {
    const lower = dayName.toLowerCase();
    if (lower.includes('new year')) return 'fas fa-glass-cheers';
    if (lower.includes('science')) return 'fas fa-flask';
    if (lower.includes('sleep')) return 'fas fa-bed';
    if (lower.includes('bird')) return 'fas fa-dove';
    if (lower.includes('heart') || lower.includes('love')) return 'fas fa-heart';
    if (lower.includes('pi') || lower.includes('math')) return 'fas fa-pi';
    if (lower.includes('star')) return 'fas fa-star';
    return 'fas fa-calendar-star';
}

function getColorForDay(dayName) {
    const lower = dayName.toLowerCase();
    if (lower.includes('new year')) return '#FF6B6B';
    if (lower.includes('science')) return '#2196F3';
    if (lower.includes('sleep')) return '#9C27B0';
    if (lower.includes('bird')) return '#4CAF50';
    if (lower.includes('heart') || lower.includes('love')) return '#FF6B6B';
    if (lower.includes('pi') || lower.includes('math')) return '#4CAF50';
    if (lower.includes('star')) return '#FFD700';
    return '#6a11cb';
}

function getAnimationForDay(dayName) {
    const lower = dayName.toLowerCase();
    if (lower.includes('new year')) return 'fireworks';
    if (lower.includes('science')) return 'science';
    if (lower.includes('sleep')) return 'sleep';
    if (lower.includes('heart') || lower.includes('love')) return 'hearts';
    if (lower.includes('bird')) return 'birds';
    return 'default';
}

function updateApiStatus(connected) {
    const status = document.getElementById('api-status');
    if (connected) {
        status.className = 'api-status connected';
        status.innerHTML = '<i class="fas fa-wifi"></i> <span>Connected to API</span>';
    } else {
        status.className = 'api-status disconnected';
        status.innerHTML = '<i class="fas fa-exclamation-triangle"></i> <span>Using Local Data</span>';
    }
}

function updateStats(count) {
    document.getElementById('special-days').innerHTML = 
        `<i class="fas fa-star"></i> <span>Special Days: ${count}</span>`;
}

function renderCalendar(date) {
    const month = date.getMonth();
    const year = date.getFullYear();
    
    // Update month/year display
    const monthNames = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"];
    document.getElementById('current-month-year').textContent = `${monthNames[month]} ${year}`;
    
    // Get first day of month and total days
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // Clear calendar
    const calendarDays = document.getElementById('calendar-days');
    calendarDays.innerHTML = '';
    
    // Add empty days for first week
    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'day';
        emptyDay.style.visibility = 'hidden';
        calendarDays.appendChild(emptyDay);
    }
    
    // Add days of the month
    const today = new Date();
    
    for (let i = 1; i <= daysInMonth; i++) {
        const dayDate = new Date(year, month, i);
        const dayElement = createDayElement(i, dayDate, month, today);
        calendarDays.appendChild(dayElement);
    }
}

function createDayElement(dayNum, dayDate, month, today) {
    const dayElement = document.createElement('div');
    dayElement.className = 'day';
    
    // Check if it's today
    if (today.getDate() === dayNum && 
        today.getMonth() === month && 
        today.getFullYear() === dayDate.getFullYear()) {
        dayElement.classList.add('today');
    }
    
    // Check if it's selected
    if (selectedDate.getDate() === dayNum && 
        selectedDate.getMonth() === month && 
        selectedDate.getFullYear() === dayDate.getFullYear()) {
        dayElement.classList.add('selected');
    }
    
    // Get special day data
    const monthStr = String(month + 1).padStart(2, '0');
    const dayStr = String(dayNum).padStart(2, '0');
    const key = `${monthStr}-${dayStr}`;
    const specialDay = specialDaysData[key];
    
    // Calculate day of year
    const dayOfYear = getDayOfYear(dayDate);
    
    dayElement.innerHTML = `
        <div class="day-count">${dayOfYear}</div>
        <div class="day-number">${dayNum}</div>
        <div class="day-theme">${specialDay ? specialDay.title.split(' ')[0] : ''}</div>
        <div class="theme-indicator"></div>
    `;
    
    // Add click event
    dayElement.addEventListener('click', () => {
        selectedDate = dayDate;
        renderCalendar(currentDate);
        updateThemeInfo(key, specialDay);
        addToRecentDays(key, specialDay, dayDate);
        createAnimation(specialDay?.animation || 'default');
        recordView(key);
    });
    
    return dayElement;
}

function getDayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
}

function updateThemeInfo(dateKey, specialDay) {
    const titleElement = document.getElementById('theme-title');
    const descriptionElement = document.getElementById('theme-description');
    const dateElement = document.getElementById('current-date');
    
    // Format date
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateElement.textContent = selectedDate.toLocaleDateString('en-US', options);
    
    if (specialDay) {
        titleElement.textContent = specialDay.title;
        descriptionElement.textContent = specialDay.description;
    } else {
        titleElement.textContent = `Day ${getDayOfYear(selectedDate)}`;
        descriptionElement.textContent = "No specific special day today, but every day is special! Make it your own celebration!";
    }
}

function createAnimation(type) {
    const container = document.getElementById('animation-container');
    container.innerHTML = '';
    
    switch(type) {
        case 'fireworks':
            createFireworks(container);
            break;
        case 'science':
            createScienceAnimation(container);
            break;
        case 'hearts':
            createHeartsAnimation(container);
            break;
        default:
            createDefaultAnimation(container);
    }
}

function createFireworks(container) {
    for (let i = 0; i < 20; i++) {
        const dot = document.createElement('div');
        dot.style.position = 'absolute';
        dot.style.width = '6px';
        dot.style.height = '6px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = getRandomColor();
        dot.style.left = `${Math.random() * 90 + 5}%`;
        dot.style.top = `${Math.random() * 90 + 5}%`;
        dot.style.animation = `firework 1s infinite`;
        dot.style.animationDelay = `${Math.random() * 2}s`;
        container.appendChild(dot);
    }
}

function createScienceAnimation(container) {
    container.innerHTML = `
        <div style="position: relative; width: 100px; height: 100px;">
            <div style="position: absolute; width: 30px; height: 30px; background: #2196F3; border-radius: 50%;"></div>
            <div style="position: absolute; width: 20px; height: 20px; background: #FF5722; border-radius: 50%; top: 60px; left: 20px; animation: orbit 3s linear infinite;"></div>
            <div style="position: absolute; width: 15px; height: 15px; background: #4CAF50; border-radius: 50%; top: 20px; left: 60px; animation: orbit 2s linear infinite reverse;"></div>
        </div>
    `;
    
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes orbit {
            0% { transform: rotate(0deg) translateX(40px) rotate(0deg); }
            100% { transform: rotate(360deg) translateX(40px) rotate(-360deg); }
        }
    `;
    document.head.appendChild(style);
}

function createHeartsAnimation(container) {
    for (let i = 0; i < 15; i++) {
        const heart = document.createElement('div');
        heart.innerHTML = '<i class="fas fa-heart"></i>';
        heart.style.position = 'absolute';
        heart.style.color = '#FF6B6B';
        heart.style.fontSize = `${Math.random() * 25 + 20}px`;
        heart.style.left = `${Math.random() * 85 + 5}%`;
        heart.style.animation = `float ${Math.random() * 3 + 2}s infinite ease-in-out`;
        heart.style.animationDelay = `${Math.random() * 2}s`;
        container.appendChild(heart);
    }
}

function createDefaultAnimation(container) {
    const icon = document.createElement('div');
    icon.innerHTML = '<i class="fas fa-calendar-star" style="font-size: 4rem; color: #6a11cb;"></i>';
    icon.style.animation = 'bounce 2s infinite';
    container.appendChild(icon);
}

function getRandomColor() {
    const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#6A0572', '#1A535C'];
    return colors[Math.floor(Math.random() * colors.length)];
}

async function recordView(dateKey) {
    try {
        await fetch(`${API_BASE_URL}/view/${dateKey}`, {
            method: 'POST'
        });
    } catch (error) {
        // Silently fail if API is not available
    }
}

function updateTodayHighlight() {
    const today = new Date();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const key = `${month}-${day}`;
    const specialDay = specialDaysData[key];
    
    const container = document.getElementById('today-highlight');
    
    if (specialDay) {
        container.innerHTML = `
            <div class="theme-preview" onclick="selectDate('${key}')">
                <div class="preview-title">${specialDay.title}</div>
                <div class="preview-date">Today</div>
            </div>
        `;
    } else {
        container.innerHTML = `
            <div class="theme-preview" onclick="selectDate('${key}')">
                <div class="preview-title">Day ${getDayOfYear(today)}</div>
                <div class="preview-date">Today</div>
            </div>
        `;
    }
}

function updateUpcomingDays() {
    const container = document.getElementById('upcoming-days');
    container.innerHTML = '';
    
    const today = new Date();
    let count = 0;
    
    for (let i = 1; i <= 30 && count < 5; i++) {
        const futureDate = new Date(today);
        futureDate.setDate(today.getDate() + i);
        const month = String(futureDate.getMonth() + 1).padStart(2, '0');
        const day = String(futureDate.getDate()).padStart(2, '0');
        const key = `${month}-${day}`;
        const specialDay = specialDaysData[key];
        
        if (specialDay) {
            const preview = document.createElement('div');
            preview.className = 'theme-preview';
            preview.onclick = () => selectDate(key);
            preview.innerHTML = `
                <div class="preview-title">${specialDay.title}</div>
                <div class="preview-date">${futureDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
            `;
            container.appendChild(preview);
            count++;
        }
    }
}

function selectDate(dateKey) {
    const [month, day] = dateKey.split('-').map(Number);
    selectedDate = new Date(currentDate.getFullYear(), month - 1, day);
    currentDate = new Date(currentDate.getFullYear(), month - 1, 1);
    renderCalendar(currentDate);
    updateThemeInfo(dateKey, specialDaysData[dateKey]);
    addToRecentDays(dateKey, specialDaysData[dateKey], selectedDate);
    createAnimation(specialDaysData[dateKey]?.animation || 'default');
    recordView(dateKey);
}

function addToRecentDays(dateKey, specialDay, date) {
    if (!specialDay) return;
    
    // Remove if already in recent
    recentDays = recentDays.filter(item => item.key !== dateKey);
    
    // Add to beginning
    recentDays.unshift({
        key: dateKey,
        title: specialDay.title,
        date: date
    });
    
    // Keep only last 5
    if (recentDays.length > 5) {
        recentDays.pop();
    }
    
    updateRecentDays();
}

function updateRecentDays() {
    const container = document.getElementById('recent-days');
    container.innerHTML = '';
    
    recentDays.forEach(item => {
        const preview = document.createElement('div');
        preview.className = 'theme-preview';
        preview.onclick = () => selectDate(item.key);
        preview.innerHTML = `
            <div class="preview-title">${item.title}</div>
            <div class="preview-date">${item.date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
        `;
        container.appendChild(preview);
    });
}

function setupEventListeners() {
    // Navigation buttons
    document.getElementById('prev-month').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });
    
    document.getElementById('next-month').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });
    
    document.getElementById('today-nav-btn').addEventListener('click', goToToday);
    document.getElementById('today-btn').addEventListener('click', goToToday);
    
    // Random button
    document.getElementById('random-btn').addEventListener('click', () => {
        const keys = Object.keys(specialDaysData);
        if (keys.length > 0) {
            const randomKey = keys[Math.floor(Math.random() * keys.length)];
            selectDate(randomKey);
        }
    });
    
    // Search functionality
    document.getElementById('search-btn').addEventListener('click', performSearch);
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

function goToToday() {
    currentDate = new Date();
    selectedDate = new Date();
    renderCalendar(currentDate);
    updateTodayHighlight();
    updateThemeInfo('', null);
    createDefaultAnimation(document.getElementById('animation-container'));
}

async function performSearch() {
    const query = document.getElementById('search-input').value.toLowerCase().trim();
    if (!query) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        if (response.ok) {
            const results = await response.json();
            if (results.length > 0) {
                selectDate(results[0].date);
            } else {
                alert('No results found');
            }
        }
    } catch (error) {
        // Fallback to local search
        const keys = Object.keys(specialDaysData);
        const foundKey = keys.find(key => {
            const day = specialDaysData[key];
            return day.title.toLowerCase().includes(query);
        });
        
        if (foundKey) {
            selectDate(foundKey);
        } else {
            alert('No results found');
        }
    }
}

// Make selectDate available globally for onclick events
window.selectDate = selectDate;

// Initialize the app when page loads
document.addEventListener('DOMContentLoaded', initApp);