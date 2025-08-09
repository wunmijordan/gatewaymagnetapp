document.addEventListener('DOMContentLoaded', function () {

  /* --------------------------------------------------------------------
   * 0. FLATPICKR DATEPICKER INIT
   * ------------------------------------------------------------------ */
  const isoInput = document.getElementById('date_of_visit');
  const displayInput = document.getElementById('date_of_visit_display');

  if (isoInput && displayInput) {
    // Pre-fill visible input if hidden ISO date exists and is valid
    if (isoInput.value) {
      const parts = isoInput.value.split('-');
      if (parts.length === 3) {
        displayInput.value = `${parts[2]}/${parts[1]}/${parts[0]}`;
      }
    }

    flatpickr(displayInput, {
      dateFormat: "d/m/Y",
      allowInput: true,
      defaultDate: displayInput.value || new Date(),
      onChange: function (selectedDates, dateStr, instance) {
        if (selectedDates.length > 0) {
          isoInput.value = instance.formatDate(selectedDates[0], "Y-m-d");
        } else {
          // Prevent empty ISO value: fallback to today’s date
          const today = new Date();
          isoInput.value = instance.formatDate(today, "Y-m-d");
          // Also update displayInput so user sees a date
          displayInput.value = instance.formatDate(today, "d/m/Y");
        }
      }
    });
  }

  /* --------------------------------------------------------------------
   * 1. DROPDOWN BEHAVIOR
   * ------------------------------------------------------------------ */
  document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(toggle => {
    toggle.addEventListener('click', function () {
      const dropdown = toggle.closest('.dropdown');
      const menu = dropdown?.querySelector('.dropdown-menu');
      if (!dropdown || !menu) return;

      setTimeout(() => {
        const rect = dropdown.getBoundingClientRect();
        const spaceBelow = (window.innerHeight || document.documentElement.clientHeight) - rect.bottom;
        dropdown.classList.toggle('dropup', spaceBelow < 200);
      }, 10);
    });
  });

  // Dropend submenu (mobile click toggle)
  document.querySelectorAll('.dropdown-menu .dropend > .dropdown-toggle').forEach(el => {
    el.addEventListener('click', function (e) {
      if (window.innerWidth < 768) {
        e.preventDefault();
        e.stopPropagation();
        this.nextElementSibling?.classList.toggle('show');
      }
    });
  });

  // Dropend hover (desktop)
  document.querySelectorAll('.dropend').forEach(dropend => {
    const toggle = dropend.querySelector('[data-bs-toggle="dropdown"]');
    if (!toggle) return;

    dropend.addEventListener('mouseenter', () => {
      if (window.innerWidth >= 992) bootstrap.Dropdown.getOrCreateInstance(toggle).show();
    });

    dropend.addEventListener('mouseleave', () => {
      if (window.innerWidth >= 992) bootstrap.Dropdown.getInstance(toggle)?.hide();
    });
  });

  /* --------------------------------------------------------------------
   * 2. TOOLTIP INIT
   * ------------------------------------------------------------------ */
  function initTooltips() {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
      new bootstrap.Tooltip(el);
    });
  }
  initTooltips();

  /* --------------------------------------------------------------------
   * 3. TOP SERVICES PROGRESS BARS (AJAX)
   * ------------------------------------------------------------------ */
  fetch(window.APP_CONFIG.urls.topServicesData)
    .then(res => res.json())
    .then(data => {
      const services = data.services || [];
      const progressContainer = document.getElementById('topServicesProgress');
      const labelsContainer = document.getElementById('topServicesLabels');
      if (!progressContainer || !labelsContainer) return;

      progressContainer.innerHTML = '';
      labelsContainer.innerHTML = '';

      const colors = ['primary', 'info', 'success', 'danger', 'warning', 'secondary', 'dark', 'muted', 'teal', 'pink'];

      services.forEach((service, i) => {
        const colorClass = `bg-${colors[i % colors.length]}`;

        const progressBar = document.createElement('div');
        progressBar.className = `progress-bar ${colorClass}`;
        progressBar.style.width = `${service.percent}%`;
        progressBar.setAttribute('role', 'progressbar');
        progressBar.setAttribute('aria-valuenow', service.percent);
        progressBar.setAttribute('aria-valuemin', '0');
        progressBar.setAttribute('aria-valuemax', '100');
        progressBar.setAttribute('data-bs-toggle', 'tooltip');
        progressBar.title = `${service.service_attended || "No Service"}: ${service.count} guests`;

        progressContainer.appendChild(progressBar);

        const labelCol = document.createElement('div');
        labelCol.className = 'col-auto d-flex align-items-center';

        const legendBox = document.createElement('span');
        legendBox.className = `legend me-2 ${colorClass}`;

        const labelText = document.createElement('span');
        labelText.textContent = service.service_attended || "No Service";

        const countText = document.createElement('span');
        countText.className = 'd-none d-md-inline d-lg-none d-xxl-inline ms-2 text-secondary';
        countText.textContent = `${service.count} guests`;

        labelCol.append(legendBox, labelText, countText);
        labelsContainer.appendChild(labelCol);
      });

      initTooltips();
    })
    .catch(err => console.error('Failed to fetch top services:', err));

  /* --------------------------------------------------------------------
   * 4. ANIMATED COUNTERS
   * ------------------------------------------------------------------ */
  document.querySelectorAll('[data-count]').forEach(el => {
    let endValue = parseInt(el.getAttribute('data-count'), 10);
    let startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / 1500, 1);
      el.textContent = Math.floor(progress * endValue);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });

  /* --------------------------------------------------------------------
   * 5. CHANNEL OF VISIT TABLE (AJAX)
   * ------------------------------------------------------------------ */
  fetch(window.APP_CONFIG.urls.channelBreakdown)
    .then(res => res.json())
    .then(data => {
      const tbody = document.getElementById('channelProgressTableBody');
      if (!tbody) return;

      tbody.innerHTML = '';

      if (!data.length) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No data available</td></tr>';
        return;
      }

      data.forEach(({ label, count, percent }) => {
        tbody.innerHTML += `
          <tr>
            <td>${label}</td>
            <td>${count}</td>
            <td class="w-50">
              <div class="progress progress-xs">
                <div class="progress-bar bg-primary" style="width: ${percent}%"></div>
              </div>
            </td>
          </tr>`;
      });
    })
    .catch(err => console.error('Channel table load error:', err));

}); // DOMContentLoaded end

/* ----------------------------------------------------------------------
 * 6. PASSWORD TOGGLE
 * -------------------------------------------------------------------- */
const togglePassword = document.querySelector('.toggle-password');
const passwordInput = document.getElementById('passwordInput');
const eyeIcon = document.getElementById('eyeIcon');

if (togglePassword && passwordInput && eyeIcon) {
  const eye = `<path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0"></path>
               <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6"></path>`;
  const eyeOff = `<path d="M3 3l18 18"></path>
                  <path d="M10.584 10.587a2 2 0 0 0 2.83 2.83"></path>
                  <path d="M9.366 5.653a9.05 9.05 0 0 1 11.087 6.347c-.717 2.43 -2.19 4.2 -4.364 5.295"></path>
                  <path d="M6.79 6.793c-1.825 1.108 -3.06 2.766 -3.79 4.707a9.053 9.053 0 0 0 9 5.5c1.477 0 2.867 -.36 4.1 -1"></path>`;

  togglePassword.addEventListener('click', function (e) {
    e.preventDefault();
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    eyeIcon.classList.toggle('rotate');
    eyeIcon.innerHTML = (type === 'password') ? eye : eyeOff;
  });
}

/* ----------------------------------------------------------------------
 * 7. MINIMAL SERVICE WORKER REGISTRATION
 * -------------------------------------------------------------------- */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/serviceworker.js')
      .then(reg => console.log('SW registered:', reg.scope))
      .catch(err => console.error('SW registration failed:', err));
  });
}
