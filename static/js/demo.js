// =========================
// CHAT PAGE INIT
// =========================
document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chatMessagesContainer");
  const chatForm = document.getElementById("chatReplyForm");
  const chatInput = document.getElementById("chatInput");
  const replyToIdInput = document.getElementById("replyToId");
  const fileAttachment = document.getElementById("fileAttachment");
  const attachmentPreview = document.getElementById("attachmentPreview");
  const replyIndicator = document.getElementById("replyIndicator");
  const replyToNameSpan = document.getElementById("replyToName");
  const clearBtn = document.getElementById("clearReplyBtn");
  const chatSearchInput = document.getElementById("chatSearchInput");

  let replyToId = null;
  let lastTimestamp = null;
  let selectedGuest = null;

  if (replyIndicator) replyIndicator.style.display = "none";

  // =========================
  // Helper functions
  // =========================
  function getUserColor(userId) {
    const colors = [
      "bg-blue-lt text-white","bg-green-lt text-white","bg-orange-lt text-white",
      "bg-purple-lt text-white","bg-pink-lt text-white","bg-cyan-lt text-white",
      "bg-yellow-lt text-white","bg-red-lt text-white","bg-indigo-lt text-white",
      "bg-teal-lt text-white","bg-lime-lt text-white","bg-amber-lt text-white",
      "bg-fuchsia-lt text-white","bg-emerald-lt text-white","bg-violet-lt text-white",
      "bg-rose-lt text-white","bg-sky-lt text-white","bg-orange-200 text-white",
      "bg-purple-200 text-white","bg-pink-200 text-white"
    ];
    return colors[userId % colors.length];
  }

  // Assign user card colors
  document.querySelectorAll(".user-card").forEach(card => {
    const userId = parseInt(card.dataset.userid, 10);
    const colorClass = getUserColor(userId);
    card.classList.add(...colorClass.split(" "));
  });

  function setReply(id, name, message, guestCard = null) {
    replyToId = id;
    if (replyToIdInput) replyToIdInput.value = id;
    if (replyIndicator && replyToNameSpan) {
      replyIndicator.style.display = "flex";

      // Build guest visual block (if guestCard exists)
      let guestVisual = "";
      if (guestCard) {
        const visual = guestCard.picture
          ? `<img src="${guestCard.picture}" alt="${guestCard.name}" 
                  style="width:40px; height:40px; object-fit:cover; border-radius:6px; margin-right:8px;">`
          : `<div class="avatar bg-purple-lt d-inline-flex align-items-center justify-content-center fw-bold"
                  style="width:40px; height:40px; border-radius:6px; margin-right:8px;">
              ${guestCard.name ? guestCard.name[0].toUpperCase() : "?"}
            </div>`;

        guestVisual = `
          <div class="d-flex align-items-center gap-2 mb-1">
            ${visual}
            <div>
              <div class="fw-bold text-warning">${guestCard.title || ""} ${guestCard.name || ""}</div>
              <div class="text-muted">${guestCard.custom_id || ""}</div>
              <div>${
                guestCard.date_of_visit
                  ? new Date(guestCard.date_of_visit).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      year: "numeric"
                    })
                  : ""
              }</div>
            </div>
          </div>`;
      }

      replyToNameSpan.innerHTML = `
      <div class="text-muted text-green">${name}</div>
      <div class="fs-4 text-light">${message}</div>
      ${guestVisual}
    `;
    }
  }

  function clearReply() {
    replyToId = null;
    if (replyToIdInput) replyToIdInput.value = "";
    if (replyIndicator) replyIndicator.style.display = "none";
    if (replyToNameSpan) replyToNameSpan.textContent = "";
  }

  window.setReply = setReply;
  window.clearReply = clearReply;

  // =========================
  // HELPER FUNCTIONS
  // =========================
  function renderGuestDetails(guest) {
    let html = `
      <div class="text-center mb-4">
        <!-- Guest Avatar / Picture -->
        <div class="position-relative d-inline-block" style="width:100px; height:100px;">
          ${guest.picture
            ? `<span class="avatar avatar-xl rounded" 
                    style="background-image: url('${guest.picture}'); display:inline-block; width:100px; height:100px; border-radius:0.5rem; background-size:cover; background-position:center; box-shadow:0 2px 5px #008ca567,0 4px 10px #008ca567; transition: box-shadow 0.3s ease;"
                    onmouseover="this.style.boxShadow='0 6px 12px #ff7b0067,0 10px 25px #ff7b0067'"
                    onmouseout="this.style.boxShadow='0 2px 4px #4ecf0333,0 6px 10px #4ecf0333'">
              </span>`
            : `<span class="avatar avatar-xl bg-grey text-white d-inline-flex align-items-center justify-content-center" 
                    style="width:100px; height:100px; font-weight:bold; font-size:24px; line-height:1; border-radius:0.5rem;">
              ${guest.full_name ? guest.full_name[0].toUpperCase() : "?"}
              </span>`}
        </div>

        <h3 class="m-0 mb-2 text-warning mt-2 fs-2">${guest.title} ${guest.full_name || "Unknown"}</h3>
        <div class="text-muted text-warning fs-3 fw-bold" style="font-family: monospace;">
          ${guest.custom_id || "-"}
        </div>

        <!-- Phone icon -->
        ${guest.phone_number ? `
          <div class="mb-2 mt-2">
            <span class="avatar avatar-sm bg-green-lt">
              <a href="tel:${guest.phone_number}" class="text-green">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M3 3m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z" />
                  <path d="M8 4l2 0" /><path d="M9 17l0 .01" /><path d="M21 6l-2 3l2 3l-2 3l2 3" />
                </svg>
              </a>
            </span>
          </div>` : ""}

        <!-- Social media icons -->
        <div class="mb-4">
          ${guest.social_media_accounts?.map(account => {
            if (!account.platform || !account.handle) return '';
            const colors = { linkedin: "#037ae9ff", whatsapp: "#03f74cff", instagram: "#de08f1ff", twitter: "#1DA1F2", tiktok: "#25ECE6" };
            let svgPaths = '';
            switch(account.platform) {
              case 'linkedin':
                svgPaths = `
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M8 11v5"/>
                  <path d="M8 8v.01"/>
                  <path d="M12 16v-5"/>
                  <path d="M16 16v-3a2 2 0 1 0 -4 0"/>
                  <path d="M3 7a4 4 0 0 1 4 -4h10a4 4 0 0 1 4 4v10a4 4 0 0 1 -4 4h-10a4 4 0 0 1 -4 -4z"/>
                `;
                break;
              case 'whatsapp':
                svgPaths = `
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M3 21l1.65 -3.8a9 9 0 1 1 3.4 2.9l-5.05 .9"/>
                  <path d="M9 10a.5 .5 0 0 0 1 0v-1a.5 .5 0 0 0 -1 0v1a5 5 0 0 0 5 5h1a.5 .5 0 0 0 0 -1h-1a.5 .5 0 0 0 0 1"/>
                `;
                break;
              case 'instagram':
                svgPaths = `
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M4 8a4 4 0 0 1 4 -4h8a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h-8a4 4 0 0 1 -4 -4z"/>
                  <path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/>
                  <path d="M16.5 7.5v.01"/>
                `;
                break;
              case 'twitter':
                svgPaths = `
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M4 4l11.733 16h4.267l-11.733 -16z"/>
                  <path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772"/>
                `;
                break;
              case 'tiktok':
                svgPaths = `
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M21 7.917v4.034a9.948 9.948 0 0 1 -5 -1.951v4.5a6.5 6.5 0 1 1 -8 -6.326v4.326a2.5 2.5 0 1 0 4 2v-11.5h4.083a6.005 6.005 0 0 0 4.917 4.917z"/>
                `;
                break;
            }
            return `<a href="${account.handle}" target="_blank" class="text-white me-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="${colors[account.platform] || '#fff'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        ${svgPaths}
                      </svg>
                    </a>`;
          }).join('')}
        </div>
      </div>

      <!-- Timeline cards -->
      <div class="row g-4">`;

    guest.field_data.forEach((field, index) => {
      html += `
        <div class="col-12 col-md-6">
          <ul class="timeline">
            <li class="timeline-event">
              <div class="timeline-event-icon bg-x-lt d-flex align-items-center justify-content-center" style="width:32px; height:32px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  ${guest.svg_icons?.[field.icon] || ""}
                </svg>
              </div>
              <div class="card timeline-event-card">
                <div class="card-body">
                  <i><small class="text-muted">${field.verbose_name}</small></i>
                  ${field.name === "date_of_visit" && field.time_since ? `<div class="text-secondary float-end small">${field.time_since} ago</div>` : ""}
                  <p class="text-base text-warning fs-3">
                    ${field.choices && guest[field.name + "_display"] ? guest[field.name + "_display"] : field.value || ""}
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </div>`;

      // Close row every 2 columns
      if ((index + 1) % 2 === 0 && index + 1 !== guest.field_data.length) {
        html += `</div><div class="row g-4">`;
      }
    });

    html += `</div>`;
    return html;
  }

  // =========================
  // Append chat message
  // =========================
  function appendMessage(msg) {
    if (!chatContainer || document.getElementById("msg-" + msg.id)) return;

    // 1️⃣ Build msgEl first
    const msgEl = document.createElement("div");
    msgEl.id = "msg-" + msg.id;
    msgEl.className = msg.sender.id == window.currentUserId ? "text-end mb-2" : "text-start mb-2";

    // 2️⃣ Then handle date wrapper / divider
    const msgDate = new Date(msg.created_at).toDateString();

    // find or create wrapper for this date
    let dateWrapper = chatContainer.querySelector(`.date-wrapper[data-date="${msgDate}"]`);
    if (!dateWrapper) {
      dateWrapper = document.createElement("div");
      dateWrapper.className = "date-wrapper mb-3";
      dateWrapper.dataset.date = msgDate;

      const divider = document.createElement("div");
      divider.className = "date-divider text-center mb-2";
      divider.innerHTML = `
        <span class="date-divider-text text-warning">
          ${new Date(msg.created_at).toLocaleDateString(undefined, { month:"long", day:"numeric", year:"numeric" })}
        </span>
      `;

      dateWrapper.appendChild(divider);
      chatContainer.appendChild(dateWrapper);
    }

    const userLabel = msg.sender.id == window.currentUserId
      ? ""
      : `${msg.sender.title || ""} ${msg.sender.full_name || ""}`.trim();

    let replyInfo = "";
    if (msg.parent && msg.parent_message) {
      const parentSender = msg.parent_message.sender || {};
      const strongText = parentSender.id == window.currentUserId ? "You" : `${parentSender.title || ""} ${parentSender.full_name || ""}`.trim();
      const messageText = msg.parent_message.message || "";

      // if parent message had a guest_card, build its small preview
      let parentGuestCardHTML = "";
      if (msg.parent_message.guest_card) {
        const g = msg.parent_message.guest_card;
        const visual = g.picture
          ? `<img src="${g.picture}" alt="${g.name}" style="width:40px; height:40px; object-fit:cover; border-radius:6px; margin-right:8px;">`
          : `<div class="avatar bg-purple-lt d-inline-flex align-items-center justify-content-center fw-bold"
                  style="width:40px; height:40px; border-radius:6px; margin-right:8px;">
              ${g.name ? g.name[0].toUpperCase() : "?"}
            </div>`;

        parentGuestCardHTML = `
          <div class="d-flex align-items-center gap-2 mt-1">
            ${visual}
            <div>
              <div class="fw-bold text-warning">${g.title || ""} ${g.name || ""}</div>
              <div class="text-muted">${g.custom_id || ""}</div>
              <div>${
                g.date_of_visit
                  ? new Date(g.date_of_visit).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      year: "numeric"
                    })
                  : ""
              }</div>
            </div>
          </div>`;
      }

      replyInfo = `
        <div class="reply-preview-container mb-2 text-start">
          <div class="reply-preview small text-white px-2 py-1 rounded-2" 
                style="border-left: 8px solid #018f14ff; 
                      background-color: #93db9d34; font-style: normal;
                      box-shadow: 0 4px 8px #000000b0;">
            <div class="text-muted text-green">${strongText}</div>
            <div class="fs-4 text-light">${messageText}</div>
            ${parentGuestCardHTML}
          </div>
        </div>
      `;
    }

    // Click Behaviors
    let pressTimer;

    // long press → reply
    msgEl.addEventListener("mousedown", startPress);
    msgEl.addEventListener("touchstart", startPress);

    msgEl.addEventListener("mouseup", cancelPress);
    msgEl.addEventListener("mouseleave", cancelPress);
    msgEl.addEventListener("touchend", cancelPress);
    msgEl.addEventListener("touchcancel", cancelPress);

    // single click logic
    msgEl.addEventListener("click", e => {
      // if clicked inside reply preview → scroll to parent
      if (e.target.closest(".reply-preview")) {
        const parentId = msg.parent;
        if (parentId) {
          const parentEl = document.getElementById("msg-" + parentId);
          if (parentEl) {
            const bubble = parentEl.querySelector(".message-bubble");
            if (bubble) {
              bubble.classList.add("highlight");
              bubble.scrollIntoView({ behavior: "smooth", block: "center" });
              setTimeout(() => bubble.classList.remove("highlight"), 3000);
            }
          }
        }
        return;
      }
    });

    // helper funcs
    function startPress() {
      pressTimer = setTimeout(() => {
        const replyName = msg.sender.id === window.currentUserId
          ? "You"
          : `${msg.sender.title || ""} ${msg.sender.full_name || ""}`.trim();
        setReply(msg.id, replyName, msg.message, msg.guest_card || null);
      }, 500); // 500ms = long press
    }

    function cancelPress() {
      clearTimeout(pressTimer);
    }

    let seenTick = "";
    if (msg.sender.id == window.currentUserId) {
      seenTick = msg.is_seen_by_all
        ? `<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-checks text-green ms-1" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M7 12l5 5l10 -10"/><path d="M2 12l5 5m5 -5l5 -5"/></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-check text-muted ms-1" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 12l5 5l10 -10"/></svg>`;
    }

    const userColor = msg.sender.id == window.currentUserId ? "bg-green-lt text-white" : getUserColor(msg.sender.id);

    msgEl.innerHTML = `
      <div class="message-bubble d-inline-block px-3 py-2 rounded-3 text-start ${userColor}"
            style="box-shadow: 0 4px 8px #0000004d;">
        ${userLabel ? `<span class="text-secondary fs-5">${userLabel}</span><br>` : ""}
        ${replyInfo}
        ${msg.attachment ? `<br><img src="${msg.attachment}" style="max-width:120px; max-height:120px;" />` : ""}
        ${msg.guest_card ? `
          <div class="reply-preview-container mb-2 rounded-2" style="box-shadow: 0 4px 8px #000000b0;">
            <div class="chat-guest-card reply-preview small text-white px-2 py-2 rounded-2 d-flex align-items-center gap-3"  
                  data-guest-id="${msg.guest_card.id}"
                  style="cursor:pointer; border-left: 8px solid #018f14ff; 
                        background-color: #11182781;" 
                        transition: background-color 0.3s; font-style: normal;">
              ${msg.guest_card.picture
                ? `<img src="${msg.guest_card.picture}" alt="${msg.guest_card.name}" 
                        style="width:300px; height:300px; object-fit:cover; 
                        border-radius:6px; display:block; margin:0 auto;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);">`
                : `<div class="avatar bg-gray d-flex align-items-center justify-content-center fs-2 fw-bold"
                      style="width:100px; height:100px; border-radius:6px; margin:0 auto;">
                    ${msg.guest_card.name ? msg.guest_card.name[0].toUpperCase() : "?"}
                  </div>`}

              <div class="mt-2 text-center" style="font-style: normal;">
                <div class="fw-bold fs-3 text-warning">${msg.guest_card.title} ${msg.guest_card.name}</div>
                <div class="text-muted">${msg.guest_card.custom_id}</div>
                <div>${
                  msg.guest_card.date_of_visit 
                    ? new Date(msg.guest_card.date_of_visit).toLocaleDateString(undefined, { 
                        month: "short", 
                        day: "numeric", 
                        year: "numeric" 
                      }) 
                    : ""
                }</div>
              </div>
            </div>
          </div>
        ` : ""}
        <strong class="message-content text-white fs-2">${msg.message || ""}</strong>
        <br>
        <small class="text-muted">${new Date(msg.created_at).toLocaleTimeString()} ${seenTick}</small>
      </div>
    `;

    // append message to this day's wrapper
    dateWrapper.appendChild(msgEl);
    //chatContainer.appendChild(msgEl);
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
  }

  // Make guest cards highlight on hover
  document.addEventListener("mouseover", function(e) {
    const card = e.target.closest(".chat-guest-card");
    if (card) card.style.backgroundColor = "#191a181e";  // darker highlight
  });

  document.addEventListener("mouseout", function(e) {
    const card = e.target.closest(".chat-guest-card");
    if (card) card.style.backgroundColor = "#11182781";  // original
  });

  // =========================
  // File attachment preview
  // =========================
  if (fileAttachment) {
    fileAttachment.onchange = e => {
      const file = e.target.files[0];
      if (!file) return;

      if (attachmentPreview) attachmentPreview.innerHTML = "";

      const reader = new FileReader();
      reader.onload = event => {
        if (attachmentPreview) {
          attachmentPreview.innerHTML = `<div class="preview-file"> ${file.name}<br><img src="${event.target.result}" style="max-width:100px; max-height:100px;"></div>`;
        }
      };
      reader.readAsDataURL(file);
    };
  }

  // =========================
  // Send chat
  // =========================
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      });
    }
    return cookieValue;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatReplyForm");
    if (chatForm) {
      chatForm.onsubmit = async e => {
        e.preventDefault();
        if (!chatInput.value.trim() && !replyToId && !fileAttachment.files[0] && !selectedGuest) return;

        const formData = new FormData();
        formData.append("message", chatInput.value);
        formData.append("parent_id", replyToId || "");
        if (fileAttachment.files[0]) formData.append("attachment", fileAttachment.files[0]);
        if (selectedGuest) formData.append("guest_id", selectedGuest.id);

        const csrftoken = getCookie("csrftoken");

        // ✅ Clear inputs right away (instant UX response)
        chatInput.value = "";
        fileAttachment.value = "";
        selectedGuest = null;
        attachmentPreview.innerHTML = "";
        clearReply();

        try {
          const res = await fetch(window.chatUrls.send, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": csrftoken }
          });
          if (!res.ok) throw new Error("Failed to send message");
          const msg = await res.json();
          appendMessage(msg);
          lastTimestamp = new Date(msg.created_at).toISOString();
        } catch (err) {
          console.error("Error sending message:", err);
        }
      };
    }
  });

  // =========================
  // Fetch messages periodically
  // =========================
  async function fetchMessages() {
    if (!chatContainer) return;
    let url = window.chatUrls.fetch;
    if (lastTimestamp) url += `?after=${lastTimestamp}`;

    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to fetch messages");
      const data = await res.json();
      if (!data.messages.length) return;

      lastTimestamp = new Date(data.messages[data.messages.length - 1].created_at).toISOString();
      data.messages.forEach(msg => appendMessage(msg));
    } catch (err) {
      console.error("Error fetching chat messages:", err);
    }
  }

  function startChatPolling() {
    if (chatInterval) return; // Already running
    fetchMessages();
    chatInterval = setInterval(fetchMessages, 10000);
  }

  function stopChatPolling() {
    clearInterval(chatInterval);
    chatInterval = null;
  }

  // =========================
  // Live search
  // =========================
  if (chatSearchInput) {
    chatSearchInput.addEventListener("input", () => {
      const query = chatSearchInput.value.toLowerCase();
      const allMessages = chatContainer.querySelectorAll(".text-start, .text-end");
      const allDividers = chatContainer.querySelectorAll(".date-divider");
      allDividers.forEach(div => div.style.display = "none");
      const visibleDividers = new Set();

      allMessages.forEach(msgWrapper => {
        const bubble = msgWrapper.querySelector(".message-bubble");
        if (!bubble) return;
        const matches = bubble.textContent.toLowerCase().includes(query);
        msgWrapper.style.display = matches ? "" : "none";
        if (matches) {
          const divider = msgWrapper.previousElementSibling;
          if (divider && divider.classList.contains("date-divider")) visibleDividers.add(divider);
        }
      });

      visibleDividers.forEach(div => div.style.display = "");
    });
  }

    // =========================
    // Guest selection & clear
    // =========================
    document.querySelectorAll(".guest-item").forEach(item => {
      item.addEventListener("click", e => {
        e.preventDefault();
        selectedGuest = {
          id: item.dataset.guestid,
          title: item.dataset.title,
          full_name: item.dataset.fullname,
          phone: item.dataset.phone,
          picture: item.dataset.picture,
          custom_id: item.dataset.customid,
          date_of_visit: item.dataset.date
        };

        const guestInitial = selectedGuest.full_name
          ? selectedGuest.full_name[0].toUpperCase()
          : "?";

        const guestVisual = selectedGuest.picture
          ? `<img src="${selectedGuest.picture}" alt="${selectedGuest.full_name}" style="width:60px; height:60px; object-fit:cover; border-radius:6px;">`
          : `<div class="avatar bg-gray d-flex align-items-center justify-content-center fs-3 fw-bold" style="width:60px; height:60px; border-radius:6px;">${guestInitial}</div>`;

        attachmentPreview.innerHTML = `
          <div class="reply-preview-container mb-2 ms-4 me-1">
            <div class="reply-preview text-white px-2 py-2 rounded-2 d-flex align-items-center justify-content-between gap-3"
                style="border-left: 8px solid #018f14ff; 
                background-color: #11182781; font-style: normal;
                box-shadow: 0 4px 8px #0000004d;">
              <div class="d-flex align-items-center gap-3">
                ${guestVisual}
                <div>
                  <div class="fw-bold text-warning">${selectedGuest.title} ${selectedGuest.full_name}</div>
                  <div class="text-muted">${selectedGuest.custom_id}</div>
                  <div>${
                    selectedGuest.date_of_visit
                      ? new Date(selectedGuest.date_of_visit).toLocaleDateString(
                          undefined,
                          { month: "short", day: "numeric", year: "numeric" }
                        )
                      : ""
                  }</div>
                </div>
              </div>
              <button type="button" class="btn p-0 border-0 d-flex align-items-center justify-content-center clear-guest" style="width:16px; height:16px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                </svg>
              </button>
            </div>
          </div>
        `;
      });
    });

    // =========================
    // Clear guest & reply
    // =========================
    document.addEventListener("click", e => {
      if (e.target.closest(".clear-guest")) {
        selectedGuest = null;
        attachmentPreview.innerHTML = "";
      }
      if (e.target.closest("#clearReplyBtn")) clearReply();
    });

    // if clicked inside guest card → open chat guest modal
    document.addEventListener("click", function (e) {
      const guestCard = e.target.closest(".chat-guest-card");
      if (!guestCard) return;

      const guestId = guestCard.getAttribute("data-guest-id");
      if (!guestId) return;

      fetch(`/guest/${guestId}/detail/`) // use your correct endpoint
        .then(res => res.json())
        .then(guest => {
          document.getElementById("chatGuestModalBody").innerHTML = renderGuestDetails(guest);
          const modalEl = document.getElementById("chatGuestModal");
          const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
          modal.show();
        })
        .catch(err => console.error("Failed to load guest details", err));
    });
  });

  document.querySelectorAll(".user-card").forEach(card => {
    const userId = parseInt(card.dataset.userid, 10);
    const phoneNumber = card.dataset.phone;
    const overlay = card.querySelector(".user-card-longpress-overlay");

    const canViewGuests = card.dataset.canViewGuests === "true"; 
    let pressTimer;

    function startPress(e) {
      // prevent the <a> default navigation temporarily
      e.preventDefault();

      card.dataset.longpress = false;
      if (overlay) overlay.classList.add("show");

      pressTimer = setTimeout(() => {
        card.dataset.longpress = true;

        if (phoneNumber) {
          // Trigger call
          window.location.href = `tel:${phoneNumber}`;
        }
      }, 500); // 500ms for long press
    }

    function cancelPress() {
      clearTimeout(pressTimer);
      if (overlay) overlay.classList.remove("show");
    }

    // Long press events
    card.addEventListener("mousedown", startPress);
    card.addEventListener("touchstart", startPress);

    card.addEventListener("mouseup", cancelPress);
    card.addEventListener("mouseleave", cancelPress);
    card.addEventListener("touchend", cancelPress);
    card.addEventListener("touchcancel", cancelPress);

    // Single click
    card.addEventListener("click", (e) => {
      if (!card.dataset.longpress) {
        if (canViewGuests) {
          const dropdown = new bootstrap.Dropdown(card);
          dropdown.toggle();
        } else {
          // regular users cannot view guests
          e.preventDefault();
        }
      }
      card.dataset.longpress = false;
    });
  });

  // if clicked inside guest card → open chat guest modal
  //const guestCard = e.target.closest(".chat-guest-card");
  //if (!guestCard) return;

  //const guestId = guestCard.getAttribute("data-guest-id");
  //if (!guestId) return;

  //fetch(`/guests/guest/${guestId}/detail/`)
  //  .then(res => res.json())
  //  .then(guest => {
  //    const modalBody = document.getElementById("chatGuestModalBody");
  //    modalBody.innerHTML = renderGuestDetails(guest);

  //    const modalEl = document.getElementById("chatGuestModal");
  //    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
  //    modal.show();
  //  })
  //  .catch(err => console.error("Failed to load guest details", err));

