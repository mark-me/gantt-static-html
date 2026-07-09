// Theme Management Module - No Framework Dependencies
var THEME_KEY = 'gantt-chart-theme';
var themeToggle = null;
var themeIcon = null;

function initThemeModule() {
    themeToggle = document.getElementById('themeToggle');
    themeIcon = document.getElementById('themeIcon');

    if (!themeToggle) return;

    initTheme();
    themeToggle.addEventListener('click', toggleTheme);

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem(THEME_KEY)) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

function initTheme() {
    var savedTheme = localStorage.getItem(THEME_KEY);
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme) {
        setTheme(savedTheme);
    } else if (prefersDark) {
        setTheme('dark');
    }
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);

    if (themeIcon) {
        themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

function toggleTheme() {
    var currentTheme = document.documentElement.getAttribute('data-theme');
    var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

window.ThemeManager = {
    init: initThemeModule,
    setTheme: setTheme,
    toggle: toggleTheme
};