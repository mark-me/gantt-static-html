// Status Filter Module - No Framework Dependencies
var activeFilters = new Set(['completed', 'in_progress', 'pending']);
var originalTaskCount = 0;

function initFilterModule(chart) {
    updateFilterInfo();
}

function shouldShowTask(task) {
    if (!task) return true;
    if (task.is_epic) return true;
    if (!task.status) return true;
    return activeFilters.has(task.status);
}

function filterByStatus(buttonElement) {
    var status = buttonElement.dataset.status;

    buttonElement.classList.toggle('active');

    if (buttonElement.classList.contains('active')) {
        activeFilters.add(status);
    } else {
        activeFilters.delete(status);
    }

    // Re-render if chart available
    if (typeof window.renderGanttView === 'function') {
        window.renderGanttView();
    }

    updateFilterInfo();
}

function resetFilters() {
    activeFilters.clear();
    activeFilters.add('completed');
    activeFilters.add('in_progress');
    activeFilters.add('pending');

    document.querySelectorAll('.status-btn').forEach(function(btn) {
        btn.classList.add('active');
    });

    // Full reset: also clear epic visibility filters and expand collapsed epics
    if (typeof window.resetEpicFilters === 'function') {
        window.resetEpicFilters();
    }
    if (window.collapsedEpics && typeof window.collapsedEpics.clear === 'function') {
        window.collapsedEpics.clear();
    }

    if (typeof window.renderGanttView === 'function') {
        window.renderGanttView();
    }

    updateFilterInfo();
}

function updateFilterInfo() {
    var infoEl = document.getElementById('filterInfo');
    if (!infoEl) return;

    var allTasks = window.projectData || [];
    var visibleCount = allTasks.filter(function(t) {
        return t && !t.is_epic && window.isFeatureVisible(t);
    }).length;

    var totalCount = allTasks.filter(function(t) {
        return t && !t.is_epic;
    }).length;

    originalTaskCount = totalCount;

    if (visibleCount !== totalCount) {
        infoEl.style.display = 'block';
        var filteredCount = totalCount - visibleCount;
        infoEl.textContent = visibleCount + '/' + totalCount + ' tasks shown (' + filteredCount + ' hidden by filters/collapse)';
    } else {
        infoEl.style.display = 'none';
    }
}

window.FilterManager = {
    init: initFilterModule,
    filterByStatus: filterByStatus,
    reset: resetFilters
};

window.filterByStatus = filterByStatus;
window.resetFilters = resetFilters;