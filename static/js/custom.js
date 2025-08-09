document.addEventListener('DOMContentLoaded', function () {
  /* 0. FLATPICKR DATEPICKER INIT */
  const isoInput = document.getElementById('date_of_visit');
  const displayInput = document.getElementById('date_of_visit_display');

  if (isoInput && displayInput) {
    // If isoInput has a valid YYYY-MM-DD value, convert to DD/MM/YYYY for displayInput
    if (isoInput.value && /^\d{4}-\d{2}-\d{2}$/.test(isoInput.value)) {
      const [year, month, day] = isoInput.value.split('-');
      displayInput.value = `${day}/${month}/${year}`;
    }

    flatpickr(displayInput, {
      dateFormat: "d/m/Y",
      allowInput: true,
      defaultDate: displayInput.value || new Date(),
      onChange(selectedDates, dateStr, instance) {
        if (selectedDates.length > 0) {
          isoInput.value = instance.formatDate(selectedDates[0], "Y-m-d");
        } else {
          const today = new Date();
          isoInput.value = instance.formatDate(today, "Y-m-d");
          displayInput.value = instance.formatDate(today, "d/m/Y");
        }
      }
    });
  }

  /* 1. DROPDOWN BEHAVIOR */
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

  document.querySelectorAll('.dropdown-menu .dropend > .dropdown-toggle').forEach(el => {
    el.addEventListener('click', function (e) {
      if (window.innerWidth < 768) {
        e.preventDefault();
        e.stopPropagation();
        this.nextElementSibling?.classList.toggle('show');
      }
    });
  });

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

  /* 2. TOOLTIP INIT */
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el);
  });

  /* 3. TOP SERVICES PROGRESS BARS (AJAX) */
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

      // Re-initialize tooltips on new elements
      document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
      });
    })
    .catch(err => console.error('Failed to fetch top services:', err));

  /* 4. ANIMATED COUNTERS */
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

  /* 5. CHANNEL OF VISIT TABLE (AJAX) */
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
});