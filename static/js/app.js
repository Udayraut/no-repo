/**
 * Skyniya Growth OS - Frontend JavaScript
 * Apple-inspired interactions, charts, alerts, modals
 */

document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    initTooltips();
    initDismissibleAlerts();
});

/**
 * Mobile sidebar toggle handling
 */
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (sidebarToggle && sidebar && sidebarOverlay) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.add('show');
            sidebarOverlay.classList.add('show');
        });
    }

    const closeSidebar = () => {
        if (sidebar && sidebarOverlay) {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        }
    };

    if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar);
}

/**
 * Bootstrap Tooltip initialization
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach((el) => {
        new bootstrap.Tooltip(el);
    });
}

/**
 * Auto-fade alerts after 5 seconds
 */
function initDismissibleAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 6000);
    });
}

/**
 * Chart helper for uniform Apple-styled minimal charts
 */
window.createSkyniyaChart = function(canvasId, type, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: options.showLegend ?? true,
                position: 'top',
                labels: {
                    boxWidth: 10,
                    boxHeight: 10,
                    usePointStyle: true,
                    font: { family: 'Inter', size: 12 },
                    color: '#6e6e73'
                }
            },
            tooltip: {
                backgroundColor: 'rgba(29, 29, 31, 0.9)',
                titleFont: { family: 'Inter', size: 12, weight: '600' },
                bodyFont: { family: 'Inter', size: 12 },
                padding: 10,
                cornerRadius: 8,
                displayColors: false
            }
        },
        scales: type === 'pie' || type === 'doughnut' ? {} : {
            x: {
                grid: { display: false },
                ticks: { font: { family: 'Inter', size: 11 }, color: '#aeaeb2' }
            },
            y: {
                grid: { color: '#f2f2f7' },
                ticks: { font: { family: 'Inter', size: 11 }, color: '#aeaeb2' },
                beginAtZero: true
            }
        }
    };

    return new Chart(ctx, {
        type: type,
        data: data,
        options: { ...defaultOptions, ...options }
    });
};
