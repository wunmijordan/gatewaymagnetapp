document.addEventListener('DOMContentLoaded', () => {

  /* =========================
     1️⃣ DROPDOWN Z-INDEX MANAGEMENT
     ========================= */
  function updateDropdownZIndex(dropdown) {
    if (!dropdown) return;

    const navbar = document.querySelector('.navbar');
    const pageHeader = document.querySelector('.page-header');

    let baseZ = 1050; // Default guest card dropdowns

    if (navbar && navbar.contains(dropdown)) {
      baseZ = 2000; // Navbar dropdowns on top
    } else if (pageHeader && pageHeader.contains(dropdown)) {
      baseZ = 1110; // Page header filters above cards
    }

    const menu = dropdown.querySelector('.dropdown-menu');
    if (menu) menu.style.zIndex = baseZ.toString();
  }

  document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(toggle => {
    const dropdown = toggle.closest('.dropdown');
    toggle.addEventListener('show.bs.dropdown', () => updateDropdownZIndex(dropdown));
  });

  window.addEventListener('resize', () => {
    document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(toggle => {
      const dropdown = toggle.closest('.dropdown');
      updateDropdownZIndex(dropdown);
    });
  });

  /* =========================
     2️⃣ DROPDOWN BEHAVIOR & DROPEND
     ========================= */
  document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const dropdown = toggle.closest('.dropdown');
      const menu = dropdown ? dropdown.querySelector('.dropdown-menu') : null;
      if (!dropdown || !menu) return;
      setTimeout(() => {
        const rect = dropdown.getBoundingClientRect();
        const spaceBelow = (window.innerHeight || document.documentElement.clientHeight) - rect.bottom;
        dropdown.classList.toggle('dropup', spaceBelow < 200);
      }, 10);
    });
  });

  document.querySelectorAll('.dropdown-menu .dropend > .dropdown-toggle').forEach(el => {
    el.addEventListener('click', e => {
      if (window.innerWidth < 768) {
        e.preventDefault();
        e.stopPropagation();
        const parentMenu = el.closest('.dropdown-menu');
        parentMenu.querySelectorAll('.dropdown-menu.show').forEach(submenu => {
          if (submenu !== el.nextElementSibling) submenu.classList.remove('show');
        });
        if (el.nextElementSibling) el.nextElementSibling.classList.toggle('show');
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

  /* =========================
     2️⃣a HEADER FILTER DROPDOWN FLOATING FIX
     ========================= */
  document.querySelectorAll('.page-header .dropdown-toggle').forEach(toggle => {
    const dropdown = toggle.closest('.dropdown');
    const menu = dropdown ? dropdown.querySelector('.dropdown-menu') : null;
    if (!dropdown || !menu) return;
    toggle.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      document.body.appendChild(menu);
      menu.style.position = 'absolute';
      menu.style.minWidth = `${dropdown.offsetWidth}px`;
      const rect = toggle.getBoundingClientRect();
      menu.style.top = `${rect.bottom + window.scrollY}px`;
      menu.style.left = `${rect.left + window.scrollX}px`;
      menu.classList.toggle('show');
      function closeMenu(event) {
        const target = event.target;
        if (!menu.contains(target) && !toggle.contains(target)) {
          menu.classList.remove('show');
          dropdown.appendChild(menu);
          document.removeEventListener('click', closeMenu);
        }
      }
      document.addEventListener('click', closeMenu);
    });
  });

  /* =========================
     3️⃣ TOOLTIP INIT
     ========================= */
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));

  /* =========================
     4️⃣ TOP SERVICES PROGRESS BARS (AJAX)
     ========================= */
  fetch(window.APP_CONFIG.urls.topServicesData)
    .then(res => res.json())
    .then(data => {
      const services = data.services || [];
      const progressContainer = document.getElementById('topServicesProgress');
      const labelsContainer = document.getElementById('topServicesLabels');
      if (!progressContainer || !labelsContainer) return;
      progressContainer.innerHTML = '';
      labelsContainer.innerHTML = '';
      const colors = ['primary','info','success','danger','warning','secondary','dark','muted','teal','pink'];
      services.forEach((service, i) => {
        const colorClass = `bg-${colors[i % colors.length]}`;
        const progressBar = document.createElement('div');
        progressBar.className = `progress-bar ${colorClass}`;
        progressBar.style.width = `${service.percent}%`;
        progressBar.setAttribute('role','progressbar');
        progressBar.setAttribute('aria-valuenow',service.percent);
        progressBar.setAttribute('aria-valuemin','0');
        progressBar.setAttribute('aria-valuemax','100');
        progressBar.setAttribute('data-bs-toggle','tooltip');
        progressBar.title = `${service.service_attended||'No Service'}: ${service.count} guests`;
        progressContainer.appendChild(progressBar);
        const labelCol = document.createElement('div');
        labelCol.className = 'col-auto d-flex align-items-center';
        const legendBox = document.createElement('span');
        legendBox.className = `legend me-2 ${colorClass}`;
        const labelText = document.createElement('span');
        labelText.textContent = service.service_attended || 'No Service';
        const countText = document.createElement('span');
        countText.className = 'd-none d-md-inline d-lg-none d-xxl-inline ms-2 text-secondary';
        countText.textContent = `${service.count} guests`;
        labelCol.append(legendBox,labelText,countText);
        labelsContainer.appendChild(labelCol);
      });
      document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
    })
    .catch(err => console.error('Failed to fetch top services:', err));

  /* =========================
     5️⃣ ANIMATED COUNTERS
     ========================= */
  document.querySelectorAll('[data-count]').forEach(el => {
    const endValue = parseInt(el.getAttribute('data-count')||'0',10);
    let startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp-startTime)/1500,1);
      el.textContent = Math.floor(progress*endValue).toString();
      if (progress<1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });

  /* =========================
     6️⃣ CHANNEL OF VISIT TABLE (AJAX)
     ========================= */
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
      data.forEach(({label,count,percent}) => {
        tbody.innerHTML += `
          <tr>
            <td>${label}</td>
            <td>${count}</td>
            <td class="w-50">
              <div class="progress progress-xs">
                <div class="progress-bar bg-primary" style="width:${percent}%"></div>
              </div>
            </td>
          </tr>`;
      });
    })
    .catch(err => console.error('Channel table load error:', err));

  /* =========================
     7️⃣ SOCIAL MEDIA FIELD HANDLING
     ========================= */
  const baseUrls = {
    linkedin: 'https://www.linkedin.com/in/',
    whatsapp: 'https://wa.me/',
    instagram: 'https://www.instagram.com/',
    twitter: 'https://twitter.com/',
    tiktok: 'https://www.tiktok.com/@',
  };
  const socialMediaIcons = {
    linkedin: '<i class="bi bi-linkedin"></i>',
    whatsapp: '<i class="bi bi-whatsapp"></i>',
    instagram: '<i class="bi bi-instagram"></i>',
    twitter: '<i class="bi bi-twitter"></i>',
    tiktok: '<i class="bi bi-tiktok"></i>',
  };
  const container = document.getElementById('socialMediaFieldsContainer');
  const addButton = document.getElementById('addSocialMediaField');
  const form = document.querySelector('form');
  if (container && addButton) {
    addButton.style.display = 'none';
    addButton.addEventListener('click', () => {
      const firstChild = container.firstElementChild;
      if (!firstChild) return;
      const newField = firstChild.cloneNode(true);
      const handleInput = newField.querySelector('input[name="social_media_handle[]"]');
      const typeInput = newField.querySelector('input[name="social_media_type[]"]');
      const dropdownBtn = newField.querySelector('button.socialMediaDropdown');
      if (handleInput) { handleInput.value=''; handleInput.placeholder='Enter handle/link'; }
      if (typeInput) typeInput.value='';
      if (dropdownBtn) {
        dropdownBtn.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 5m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /><path d="M5 19m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /><path d="M19 19m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /><path d="M12 14m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" /><path d="M12 7l0 4" /><path d="M6.7 17.8l2.8 -2" /><path d="M17.3 17.8l-2.8 -2" /></svg><span class="visually-hidden">Toggle Dropdown</span>`;
      }
      container.appendChild(newField);
    });
    container.addEventListener('click', e => {
      const optionEl = e.target.closest('.social-media-option');
      if (!optionEl) return;
      e.preventDefault();
      const selectedType = optionEl.getAttribute('data-type') || '';
      const selectedIconSVG = optionEl.getAttribute('data-icon') || '';
      const fieldGroup = optionEl.closest('.social-media-field');
      const typeInput = fieldGroup.querySelector('input[name="social_media_type[]"]');
      const handleInput = fieldGroup.querySelector('input[name="social_media_handle[]"]');
      const dropdownBtn = fieldGroup.querySelector('button.socialMediaDropdown');
      if (typeInput) typeInput.value=selectedType;
      if (dropdownBtn) dropdownBtn.innerHTML=selectedIconSVG+'<span class="visually-hidden">Toggle Dropdown</span>';
      if (handleInput) {
        let handle = handleInput.value.trim();
        for (const [type,url] of Object.entries(baseUrls)) if(handle.startsWith(url)) handle=handle.slice(url.length);
        handleInput.value = handle;
        handleInput.placeholder = selectedType && baseUrls[selectedType] ? baseUrls[selectedType] : 'Enter handle/link';
        handleInput.focus();
      }
      addButton.style.display = selectedType ? 'inline-block' : 'none';
    });
    if(form) {
      form.addEventListener('submit', () => {
        const allTypeInputs=form.querySelectorAll('input[name="social_media_type[]"]');
        const allHandleInputs=form.querySelectorAll('input[name="social_media_handle[]"]');
        allTypeInputs.forEach((typeInput,i)=>{
          const type=typeInput.value;
          let handle=allHandleInputs[i].value.trim();
          if(type && baseUrls[type] && !handle.startsWith(baseUrls[type])) allHandleInputs[i].value=baseUrls[type]+handle;
        });
      });
    }
  }

  /* =========================
     8️⃣ GUEST DETAIL MODAL (BULLETPROOF)
     ========================= */
  const modalEl = document.getElementById('guestDetailModal');
  if(modalEl){
    const modal = new bootstrap.Modal(modalEl);
    const modalBody = modalEl.querySelector('.modal-body');
    document.querySelectorAll('.guest-name-link').forEach(link=>{
      link.addEventListener('click', e=>{
        e.preventDefault();
        const url = link.dataset.detailUrl || '';
        modalBody.innerHTML='<div class="text-center py-5">Loading...</div>';
        modal.show(); // Ensure modal always opens immediately

        if(!url){
          modalBody.innerHTML='<div class="text-center text-muted py-5">No data available</div>';
          return;
        }

        fetch(url)
          .then(res=>res.text())
          .then(html=>{
            modalBody.innerHTML=html || '<div class="text-center text-muted py-5">No data available</div>';
          })
          .catch(err=>{
            console.error('Modal load error:',err);
            modalBody.innerHTML='<div class="text-center text-danger py-5">Failed to load guest details</div>';
          });
      });
    });
  }

});
