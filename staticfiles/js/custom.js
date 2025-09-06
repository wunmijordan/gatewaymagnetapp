document.addEventListener('DOMContentLoaded', () => {

  /* =========================
     1️⃣ DROPDOWN Z-INDEX MANAGEMENT & SMOOTH DROPUP
     ========================= */
  function updateDropdownZIndex(dropdown) {
    if (!dropdown) return;
    const navbar = document.querySelector('.navbar');
    const pageHeader = document.querySelector('.page-header');
    let baseZ = 1050;
    if (navbar && navbar.contains(dropdown)) baseZ = 2000;
    else if (pageHeader && pageHeader.contains(dropdown)) baseZ = 1110;
    const menu = dropdown.querySelector('.dropdown-menu');
    if (menu) menu.style.zIndex = baseZ.toString();
  }

  function handleDropdownBehavior(dropdown, toggle) {
    if (!dropdown || !toggle) return;
    const menu = dropdown.querySelector('.dropdown-menu');
    if (!menu) return;

    function adjustDropup() {
      const rect = dropdown.getBoundingClientRect();
      const spaceBelow = (window.innerHeight || document.documentElement.clientHeight) - rect.bottom;
      dropdown.classList.toggle('dropup', spaceBelow < 200);
    }

    toggle.addEventListener('click', () => requestAnimationFrame(adjustDropup));
  }

  document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(toggle => {
    const dropdown = toggle.closest('.dropdown');
    toggle.addEventListener('show.bs.dropdown', () => updateDropdownZIndex(dropdown));
    handleDropdownBehavior(dropdown, toggle);
  });

  window.addEventListener('resize', () => {
    document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(toggle => {
      const dropdown = toggle.closest('.dropdown');
      updateDropdownZIndex(dropdown);
    });
  });

  /* =========================
     2️⃣ Dropend hover behavior for desktop
     ========================= */
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
     3️⃣ HEADER FILTER DROPDOWN FLOATING FIX
     ========================= */
  document.querySelectorAll('.page-header .dropdown-toggle').forEach(toggle => {
    const dropdown = toggle.closest('.dropdown');
    const menu = dropdown?.querySelector('.dropdown-menu');
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
     4️⃣ TOOLTIP INIT
     ========================= */
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));

  /* =========================
     5️⃣ TOP SERVICES PROGRESS BARS
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
     6️⃣ ANIMATED COUNTERS
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
     7️⃣ CHANNEL OF VISIT TABLE
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
     8️⃣ SOCIAL MEDIA FIELD HANDLING
     ========================= */
  (function(){
    const baseUrls = {
      linkedin: 'https://www.linkedin.com/in/',
      whatsapp: 'https://wa.me/',
      instagram: 'https://www.instagram.com/',
      twitter: 'https://twitter.com/',
      tiktok: 'https://www.tiktok.com/@',
    };

    const container = document.getElementById('socialMediaFieldsContainer');
    const addButton = document.getElementById('addSocialMediaField');
    const form = document.querySelector('form');
    if(!container || !addButton) return;

    function updateDropdownLogo(field){
      const typeInput = field.querySelector('input[name="social_media_type[]"]');
      const dropdownBtn = field.querySelector('button.socialMediaDropdown');
      if(typeInput?.value){
        const option = field.querySelector(`.dropdown-item[data-type="${typeInput.value}"]`);
        if(option) dropdownBtn.innerHTML = option.getAttribute('data-icon') + '<span class="visually-hidden">Toggle Dropdown</span>';
      }
    }

    function toggleAddButton(){
      const allFields = container.querySelectorAll('.social-media-field');
      let anySelected = false;
      allFields.forEach(f=>{
        const typeInput = f.querySelector('input[name="social_media_type[]"]');
        if(typeInput?.value) anySelected=true;
      });
      addButton.style.display = anySelected ? 'inline-block' : 'none';
    }

    container.querySelectorAll('.social-media-field').forEach(updateDropdownLogo);
    toggleAddButton();

    addButton.addEventListener('click', () => {
      const firstChild = container.firstElementChild;
      if(!firstChild) return;
      const newField = firstChild.cloneNode(true);
      const handleInput = newField.querySelector('input[name="social_media_handle[]"]');
      const typeInput = newField.querySelector('input[name="social_media_type[]"]');
      const dropdownBtn = newField.querySelector('button.socialMediaDropdown');
      if(handleInput) handleInput.value=''; handleInput.placeholder='Enter handle/link';
      if(typeInput) typeInput.value='';
      if(dropdownBtn) dropdownBtn.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 5m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /><path d="M5 19m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /><path d="M19 19m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /><path d="M12 14m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" /><path d="M12 7l0 4" /><path d="M6.7 17.8l2.8 -2" /><path d="M17.3 17.8l-2.8 -2" /></svg><span class="visually-hidden">Toggle Dropdown</span>`;
      container.appendChild(newField);
      toggleAddButton();
    });

    container.addEventListener('click', e=>{
      const optionEl = e.target.closest('.social-media-option');
      if(!optionEl) return;
      e.preventDefault();
      const selectedType = optionEl.getAttribute('data-type') || '';
      const selectedIconSVG = optionEl.getAttribute('data-icon') || '';
      const fieldGroup = optionEl.closest('.social-media-field');
      const typeInput = fieldGroup.querySelector('input[name="social_media_type[]"]');
      const handleInput = fieldGroup.querySelector('input[name="social_media_handle[]"]');
      const dropdownBtn = fieldGroup.querySelector('button.socialMediaDropdown');
      if(typeInput) typeInput.value = selectedType;
      if(dropdownBtn) dropdownBtn.innerHTML = selectedIconSVG + '<span class="visually-hidden">Toggle Dropdown</span>';
      if(handleInput){
        let handle = handleInput.value.trim();
        for(const [type,url] of Object.entries(baseUrls)) if(handle.startsWith(url)) handle=handle.slice(url.length);
        handleInput.value = handle;
        handleInput.placeholder = selectedType && baseUrls[selectedType] ? baseUrls[selectedType] : 'Enter handle/link';
        handleInput.focus();
      }
      toggleAddButton();
    });

    if(form){
      form.addEventListener('submit', ()=>{
        const allTypeInputs = form.querySelectorAll('input[name="social_media_type[]"]');
        const allHandleInputs = form.querySelectorAll('input[name="social_media_handle[]"]');
        allTypeInputs.forEach((typeInput,i)=>{
          const type=typeInput.value;
          let handle = allHandleInputs[i].value.trim();
          if(type && baseUrls[type] && !handle.startsWith(baseUrls[type])) allHandleInputs[i].value=baseUrls[type]+handle;
        });
      });
    }

  })();

  /* =========================
     9️⃣ GUEST DETAIL MODAL
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
        modal.show();
        if(!url){
          modalBody.innerHTML='<div class="text-center text-muted py-5">No data available</div>';
          return;
        }
        fetch(url).then(r=>r.text())
          .then(html=>{ modalBody.innerHTML = html||'<div class="text-center text-muted py-5">No data available</div>'; })
          .catch(err=>{ console.error('Modal load error:',err); modalBody.innerHTML='<div class="text-center text-danger py-5">Failed to load guest details</div>'; });
      });
    });
  }

  /* =========================
     🔟 PWA SERVICE WORKER
     ========================= */
  if('serviceWorker' in navigator){
    window.addEventListener('load', ()=>{
      navigator.serviceWorker.getRegistrations()
        .then(regs=>regs.forEach(r=>r.unregister()))
        .finally(()=>navigator.serviceWorker.register("/static/js/sw.js")
          .then(reg=>console.log('Service Worker registered:',reg))
          .catch(err=>console.error('SW registration failed:',err)));
    });
  }

  /* =========================
     1️⃣1️⃣ NOTIFICATIONS
     ========================= */
  (() => {
    let lastNotifIds = new Set();

    const notifSound = document.getElementById("notifSound");
    const previewAudio = document.getElementById("previewSound");
    const { userSound, soundMap } = window.djangoData || {};
    let audioUnlocked = false;

    // Unlock audio on first user interaction
    function unlockAudio() {
      if (audioUnlocked) return;
      [notifSound, previewAudio].forEach(audio => {
        audio.volume = 0;
        audio.play()
          .then(() => { audio.pause(); audio.currentTime = 0; audio.volume = 1; })
          .catch(() => {});
      });
      audioUnlocked = true;
      console.log("✅ Audio unlocked");
    }

    ["click", "keydown", "touchstart"].forEach(evt => document.addEventListener(evt, unlockAudio, { once: true }));

    function setNotificationSound(soundKey) {
      const src = soundMap[soundKey] || Object.values(soundMap)[0];
      notifSound.src = src;
      notifSound.load();
    }
    setNotificationSound(userSound);

    function playNotifSound() {
      if (!audioUnlocked) return;
      notifSound.currentTime = 0;
      notifSound.play().catch(err => console.warn("🔇 Notification blocked:", err));
    }

    // ====== Fetch and Poll Notifications ======
    const notifCsrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    async function fetchUnreadNotifications(playSound = true) {
      try {
        const res = await fetch("/notifications/api/unread/");
        const data = await res.json();
        const notifList = document.getElementById("notif-list");
        let badge = document.getElementById("notif-badge");
        if (!notifList) return;

        notifList.innerHTML = data.length ? '' : '<div class="list-group-item">No new notifications</div>';

        if (data.length && !badge) {
          const bell = document.querySelector('.nav-link[data-bs-toggle="dropdown"]');
          if (bell) {
            badge = document.createElement("span");
            badge.id = "notif-badge";
            badge.className = "badge bg-red text-light";
            bell.appendChild(badge);
          }
        }

        let newIds = new Set(data.map(n => n.id));
        let hasNew = [...newIds].some(id => !lastNotifIds.has(id));
        lastNotifIds = newIds;

        data.forEach(n => {
          const item = document.createElement("div");
          item.className = "list-group-item notif-item";
          item.dataset.id = n.id;
          item.innerHTML = `
            <div class="row align-items-center">
              <div class="col-auto">
                <span class="status-dot status-dot-animated ${n.is_urgent ? 'bg-red' : n.is_success ? 'bg-green' : 'bg-gray'} d-block"></span>
              </div>
              <div class="col">
                <a href="${n.link || '#'}" class="text-body d-block notif-link text-truncate">${n.title}</a>
                <div class="d-block text-secondary mt-n1 notif-description" data-full="${n.description}">
                  ${n.description.length > 150 ? n.description.slice(0, 150) + ' <a href="#" class="show-more">...more</a>' : n.description}
                </div>
              </div>
            </div>
          `;
          notifList.appendChild(item);
          item.querySelector(".notif-link")?.addEventListener("click", async e => {
            e.preventDefault();
            try {
              const res = await fetch(`/notifications/mark-read/${n.id}/`, {
                method: "POST",
                headers: { "X-CSRFToken": notifCsrfToken }
              });
              if (res.ok) {
                item.remove();
                if (!notifList.children.length) {
                  notifList.innerHTML = '<div class="list-group-item">No new notifications</div>';
                  badge?.remove();
                }
                if (n.link) window.location.href = n.link;
              }
            } catch (err) { console.error("Failed to mark notification as read", err); }
          });
        });

        if (badge) badge.textContent = data.length;

        if (playSound && audioUnlocked && hasNew) playNotifSound();

      } catch (err) { console.error("Failed to fetch notifications", err); }
    }

    let notificationInterval = null;

    function startPolling() {
      if (notificationInterval) return;

      // First fetch without sound to populate existing notifications
      fetchUnreadNotifications(false);

      // Start interval for subsequent polls with sound
      notificationInterval = setInterval(() => fetchUnreadNotifications(true), 10000);
    }

    function stopPolling() {
      if (notificationInterval) {
        clearInterval(notificationInterval);
        notificationInterval = null;
      }
    }

    document.addEventListener("visibilitychange", () => {
      document.hidden ? stopPolling() : startPolling();
    });
    startPolling();

    document.getElementById("mark-all-read-btn")?.addEventListener("click", async () => {
      try {
        const res = await fetch("/notifications/mark-all-read/", {
          method: "POST",
          headers: { "X-CSRFToken": notifCsrfToken }
        });
        if (res.ok) fetchUnreadNotifications(false);
      } catch (err) { console.error("Failed to mark all read", err); }
    });
  })();

});
