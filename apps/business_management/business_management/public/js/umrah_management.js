// Umrah Management Website Customizations
// Support for Multitheme (Light/Dark), Multilingual (EN/AR/UR), and Multicurrency (SAR/USD/PKR) globally

const translations = {
    en: {
        home: "Home",
        about_us: "ABOUT US",
        ceo_message: "CEO MESSAGE",
        our_experties: "OUR EXPERTIES",
        our_services: "OUR SERVICES",
        contact_us: "CONTACT US",
        career: "CAREER",
        brand: "IICC Umrah",
        hero_title: "Divine Journey of a Lifetime",
        hero_subtitle: "Experience peaceful pilgrimage with IICC's trusted and premium Umrah packages.",
        view_packages: "Explore Packages",
        learn_more: "IICC Portal",
        packages_heading: "Our Umrah Packages",
        active_badge: "Premium",
        nights_makkah: "Nights Makkah",
        nights_madinah: "Nights Madinah",
        accommodations: "Accommodations",
        makkah_hotel: "🕋 Makkah Hotel:",
        madinah_hotel: "🕌 Madinah Hotel:",
        price_sharing: "Sharing Room",
        price_quad: "Quad Room",
        price_triple: "Triple Room",
        price_double: "Double Room",
        book_now: "Book Now"
    },
    ar: {
        home: "الرئيسية",
        about_us: "من نحن",
        ceo_message: "رسالة الرئيس التنفيذي",
        our_experties: "خبراتنا",
        our_services: "خدماتنا",
        contact_us: "اتصل بنا",
        career: "التوظيف",
        brand: "إي آي سي سي للعمرة",
        hero_title: "رحلة إيمانية للعمر",
        hero_subtitle: "استمتع برحلة حج هادئة مع باقات عمرة موثوقة ومميزة من إي آي سي سي.",
        view_packages: "استكشف الباقات",
        learn_more: "بوابة الشركة",
        packages_heading: "باقات العمرة لدينا",
        active_badge: "مميز",
        nights_makkah: "ليالي مكة",
        nights_madinah: "ليالي المدينة",
        accommodations: "السكن والإقامة",
        makkah_hotel: "🕋 فندق مكة:",
        madinah_hotel: "🕌 فندق المدينة:",
        price_sharing: "غرفة مشتركة",
        price_quad: "غرفة رباعية",
        price_triple: "غرفة ثلاثية",
        price_double: "غرفة ثنائية",
        book_now: "احجز الآن"
    },
    ur: {
        home: "ہوم",
        about_us: "ہمارے بارے میں",
        ceo_message: "سی ای او کا پیغام",
        our_experties: "ہماری مہارت",
        our_services: "ہماری خدمات",
        contact_us: "ہم سے رابطہ کریں",
        career: "کیریئر",
        brand: "آئی آئی سی سی عمرہ",
        hero_title: "عمر بھر کا روحانی سفر",
        hero_subtitle: "آئی آئی سی سی کے قابل اعتماد اور پریمیم عمرہ پیکجز کے ساتھ پرسکون زیارت کا تجربہ کریں۔",
        view_packages: "پیکجز دیکھیں",
        learn_more: "کمپنی پورٹل",
        packages_heading: "ہمارے عمرہ پیکجز",
        active_badge: "پریمیم",
        nights_makkah: "مکہ راتیں",
        nights_madinah: "مدینہ راتیں",
        accommodations: "رہائش گاہیں",
        makkah_hotel: "🕋 مکہ ہوٹل:",
        madinah_hotel: "🕌 مدینہ ہوٹل:",
        price_sharing: "مشترکہ کمرہ",
        price_quad: "چار بستروں والا کمرہ",
        price_triple: "تین بستروں والا کمرہ",
        price_double: "دو بستروں والا کمرہ",
        book_now: "ابھی بک کریں"
    }
};

let currentLang = localStorage.getItem('umrah_lang') || 'en';
let currentCurrency = localStorage.getItem('umrah_currency') || 'SAR';
let currentRate = parseFloat(localStorage.getItem('umrah_rate')) || 1.0;
let currentSymbol = localStorage.getItem('umrah_symbol') || 'SAR';
let currentTheme = localStorage.getItem('umrah_theme') || 'light';

function injectNavbarControls() {
    if (document.getElementById('umrah-navbar-controls')) return;
    
    const navbarNav = document.querySelector('.navbar-collapse .ml-auto.navbar-nav');
    if (!navbarNav) return;
    
    const controlsHtml = `
        <li class="nav-item dropdown umrah-nav-control" id="umrah-currency-nav">
            <a class="nav-link dropdown-toggle" href="#" id="umrahCurrencyDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <span id="active-currency-label-nav">SAR (﷼)</span>
            </a>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="umrahCurrencyDropdown">
                <a class="dropdown-item" href="#" onclick="window.changeCurrency('SAR', 1.0, '﷼'); return false;">SAR (﷼)</a>
                <a class="dropdown-item" href="#" onclick="window.changeCurrency('USD', 0.27, '$'); return false;">USD ($)</a>
                <a class="dropdown-item" href="#" onclick="window.changeCurrency('PKR', 74.50, 'Rs'); return false;">PKR (Rs)</a>
            </div>
        </li>
        <li class="nav-item dropdown umrah-nav-control" id="umrah-lang-nav">
            <a class="nav-link dropdown-toggle" href="#" id="umrahLangDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <span id="active-lang-label-nav">English</span>
            </a>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="umrahLangDropdown">
                <a class="dropdown-item" href="#" onclick="window.changeLanguage('en'); return false;">English</a>
                <a class="dropdown-item" href="#" onclick="window.changeLanguage('ar'); return false;">العربية</a>
                <a class="dropdown-item" href="#" onclick="window.changeLanguage('ur'); return false;">اردو</a>
            </div>
        </li>
        <li class="nav-item umrah-nav-control" id="umrah-theme-nav">
            <button class="btn btn-link nav-link theme-toggle-btn-nav" onclick="window.toggleTheme(); return false;" aria-label="Toggle Theme" style="border: none; background: transparent; padding: 8px 15px;">
                <span id="theme-btn-icon-nav">🌙</span>
            </button>
        </li>
        <span id="umrah-navbar-controls" style="display:none;"></span>
    `;
    
    navbarNav.insertAdjacentHTML('beforeend', controlsHtml);
}

window.toggleTheme = function() {
    if (document.body.classList.contains('theme-dark')) {
        window.applyTheme('light');
    } else {
        window.applyTheme('dark');
    }
}

window.applyTheme = function(theme) {
    const btnIconNav = document.getElementById('theme-btn-icon-nav');
    const btnIconHome = document.getElementById('theme-btn-icon');
    const portal = document.getElementById('umrah-portal');
    
    if (theme === 'dark') {
        document.body.classList.remove('theme-light');
        document.body.classList.add('theme-dark');
        if (portal) {
            portal.classList.remove('theme-light');
            portal.classList.add('theme-dark');
        }
        if (btnIconNav) btnIconNav.innerText = '☀️';
        if (btnIconHome) btnIconHome.innerText = '☀️';
        localStorage.setItem('umrah_theme', 'dark');
    } else {
        document.body.classList.remove('theme-dark');
        document.body.classList.add('theme-light');
        if (portal) {
            portal.classList.remove('theme-dark');
            portal.classList.add('theme-light');
        }
        if (btnIconNav) btnIconNav.innerText = '🌙';
        if (btnIconHome) btnIconHome.innerText = '🌙';
        localStorage.setItem('umrah_theme', 'light');
    }
}

window.changeCurrency = function(currency, rate, symbol) {
    window.applyCurrency(currency, rate, symbol);
}

window.applyCurrency = function(currency, rate, symbol) {
    currentCurrency = currency;
    currentRate = rate;
    currentSymbol = symbol;
    
    localStorage.setItem('umrah_currency', currency);
    localStorage.setItem('umrah_rate', rate);
    localStorage.setItem('umrah_symbol', symbol);
    
    const activeLabelNav = document.getElementById('active-currency-label-nav');
    const activeLabelHome = document.getElementById('active-currency-label');
    
    if (activeLabelNav) activeLabelNav.innerText = `${currency} (${symbol})`;
    if (activeLabelHome) activeLabelHome.innerText = `${currency} (${symbol})`;
    
    document.querySelectorAll('.price-value').forEach(el => {
        const sarPrice = parseFloat(el.getAttribute('data-sar'));
        const converted = (sarPrice * rate).toFixed(2);
        el.innerText = `${symbol} ${converted}`;
    });
}

window.changeLanguage = function(lang) {
    window.applyLanguage(lang);
}

window.applyLanguage = function(lang) {
    currentLang = lang;
    localStorage.setItem('umrah_lang', lang);
    
    const langLabels = { en: 'English', ar: 'العربية', ur: 'اردو' };
    
    const activeLabelNav = document.getElementById('active-lang-label-nav');
    const activeLabelHome = document.getElementById('active-lang-label');
    
    if (activeLabelNav) activeLabelNav.innerText = langLabels[lang];
    if (activeLabelHome) activeLabelHome.innerText = langLabels[lang];
    
    // Toggle direction and layout
    if (lang === 'ar' || lang === 'ur') {
        document.documentElement.setAttribute('dir', 'rtl');
    } else {
        document.documentElement.setAttribute('dir', 'ltr');
    }
    
    // Translate navbar links
    window.translateNavbar(lang);
    
    // Translate all template elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            el.innerText = translations[lang][key];
        }
    });
}

window.translateNavbar = function(lang) {
    const navLinks = document.querySelectorAll('.navbar .nav-link, .navbar .navbar-brand span');
    navLinks.forEach(el => {
        const text = el.innerText.trim();
        let key = null;
        if (text === "Home" || text === "الرئيسية" || text === "ہوم") key = "home";
        else if (text === "ABOUT US" || text === "من نحن" || text === "ہمارے بارے میں") key = "about_us";
        else if (text === "CEO MESSAGE" || text === "رسالة الرئيس التنفيذي" || text === "سی ای او کا پیغام") key = "ceo_message";
        else if (text === "OUR EXPERTIES" || text === "خبراتنا" || text === "ہماری مہارت") key = "our_experties";
        else if (text === "OUR SERVICES" || text === "خدماتنا" || text === "ہماری خدمات") key = "our_services";
        else if (text === "CONTACT US" || text === "اتصل بنا" || text === "ہم سے رابطہ کریں") key = "contact_us";
        else if (text === "CAREER" || text === "التوظيف" || text === "کیریئر") key = "career";
        
        if (key && translations[lang] && translations[lang][key]) {
            el.innerText = translations[lang][key];
        }
    });
}

// Initialize on DOMContentLoaded and on fast route updates
function initializeUmrahPortal() {
    injectNavbarControls();
    window.applyLanguage(currentLang);
    window.applyCurrency(currentCurrency, currentRate, currentSymbol);
    window.applyTheme(currentTheme);
}

document.addEventListener('DOMContentLoaded', initializeUmrahPortal);
// Support Ajax loading pages if any
$(document).on('page-change', initializeUmrahPortal);
