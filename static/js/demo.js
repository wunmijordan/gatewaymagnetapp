${isMe ? `<div class="ms-2">${avatarHTML}</div>` : ""}

📌


function appendMessage(msg) {
    console.log("Appending message:", msg);
    console.log("chatContainer:", chatContainer);
    console.log("msg.id:", msg.id);
    console.log("msg.created_at:", msg.created_at, "->", new Date(msg.created_at));

    if (!chatContainer) {
      console.warn("❌ No chatContainer found");
      return;
    }
    if (document.getElementById("msg-" + msg.id)) {
      console.warn("❌ Duplicate message ID detected:", msg.id);
      return;
    }


    const msgEl = document.createElement("div");
    msgEl.id = "msg-" + msg.id;
    msgEl.className = msg.sender.id == window.currentUserId ? "text-end mb-2" : "text-start mb-2";

    // === Handle date divider + wrapper ===
    const msgDate = new Date(msg.created_at).toDateString();
    let dividerWrapper = chatContainer.querySelector(`.date-wrapper[data-date="${msgDate}"]`);

    if (!dividerWrapper) {
      // Create divider
      const divider = document.createElement("div");
      divider.className = "date-divider text-center mb-2";
      divider.dataset.date = msgDate;
      divider.innerHTML = `<span class="date-divider-text text-warning">
        ${new Date(msg.created_at).toLocaleDateString(undefined, {
          month: "long",
          day: "numeric",
          year: "numeric",
        })}
      </span>`;

      // Create wrapper for that day’s messages
      dividerWrapper = document.createElement("div");
      dividerWrapper.className = "date-wrapper";
      dividerWrapper.dataset.date = msgDate;

      chatContainer.appendChild(divider);
      chatContainer.appendChild(dividerWrapper);
    }

    // === Determine user label ===
    const userLabel = msg.sender.id == window.currentUserId ? "" : `${msg.sender.title || ""} ${msg.sender.full_name || ""}`.trim();

    // === Reply info if this message is a reply ===
    let replyInfo = "";
    if (msg.parent && msg.parent_message) {
      const parentSender = msg.parent_message.sender || {};
      const strongText = parentSender.id == window.currentUserId ? "You" : `${parentSender.title || ""} ${parentSender.full_name || ""}`.trim();
      const messageText = msg.parent_message.message || "";

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
              <div>${g.date_of_visit ? new Date(g.date_of_visit).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }) : ""}</div>
            </div>
          </div>`;
      }

      replyInfo = `
        <div class="reply-preview-container mb-2 text-start">
          <div class="reply-preview small text-white px-2 py-1 rounded-2" 
                style="border-left: 8px solid #018f14ff; background-color: #93db9d34; font-style: normal; box-shadow: 0 4px 8px #000000b0;">
            <div class="text-muted text-green">${strongText}</div>
            <div class="fs-4 text-light">${messageText}</div>
            ${parentGuestCardHTML}
          </div>
        </div>`;
    }

    // === Long press to reply ===
    let pressTimer;
    msgEl.addEventListener("mousedown", startPress);
    msgEl.addEventListener("touchstart", startPress);
    msgEl.addEventListener("mouseup", cancelPress);
    msgEl.addEventListener("mouseleave", cancelPress);
    msgEl.addEventListener("touchend", cancelPress);
    msgEl.addEventListener("touchcancel", cancelPress);

    msgEl.addEventListener("click", e => {
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

    function startPress() {
      pressTimer = setTimeout(() => {
        const replyName = msg.sender.id === window.currentUserId ? "You" : `${msg.sender.title || ""} ${msg.sender.full_name || ""}`.trim();
        setReply(msg.id, replyName, msg.message, msg.guest_card || null);
      }, 500);
    }
    function cancelPress() {
      clearTimeout(pressTimer);
    }

    // === Seen tick for sender ===
    let seenTick = "";
    if (msg.sender.id == window.currentUserId) {
      seenTick = msg.is_seen_by_all
        ? `<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-checks text-green ms-1" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M7 12l5 5l10 -10"/><path d="M2 12l5 5m5 -5l5 -5"/></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-check text-muted ms-1" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 12l5 5l10 -10"/></svg>`;
    }

    const userColor = msg.sender.id == window.currentUserId ? "bg-green-lt text-white" : getUserColor(msg.sender.id);

    // === Message bubble content ===
    msgEl.innerHTML = `
      <div class="message-bubble d-inline-block px-3 py-2 rounded-3 text-start ${userColor}" style="box-shadow: 0 4px 8px #0000004d;">
        ${userLabel ? `<span class="text-secondary fs-5">${userLabel}</span><br>` : ""}
        ${replyInfo}
        ${msg.guest_card ? `
          <div class="reply-preview-container mb-2 rounded-2" style="box-shadow: 0 4px 8px #000000b0;">
            <div class="chat-guest-card reply-preview small text-white px-2 py-2 rounded-2 d-flex align-items-center gap-3"  
                  data-guest-id="${msg.guest_card.id}" style="cursor:pointer; border-left: 8px solid #018f14ff; background-color: #11182781;" transition: background-color 0.3s; font-style: normal;">
              ${msg.guest_card.picture
                ? `<img src="${msg.guest_card.picture}" alt="${msg.guest_card.name}" 
                        style="width:300px; height:300px; object-fit:cover; border-radius:6px; display:block; margin:0 auto; box-shadow:0 4px 8px rgba(0,0,0,0.3);">`
                : `<div class="avatar bg-gray d-flex align-items-center justify-content-center fs-2 fw-bold"
                      style="width:100px; height:100px; border-radius:6px; margin:0 auto;">
                    ${msg.guest_card.name ? msg.guest_card.name[0].toUpperCase() : "?"}
                  </div>`}
              <div class="mt-2 text-center" style="font-style: normal;">
                <div class="fw-bold fs-3 text-warning">${msg.guest_card.title} ${msg.guest_card.name}</div>
                <div class="text-muted">${msg.guest_card.custom_id}</div>
                <div>${msg.guest_card.date_of_visit ? new Date(msg.guest_card.date_of_visit).toLocaleDateString(undefined, { month:"short", day:"numeric", year:"numeric" }) : ""}</div>
              </div>
            </div>
          </div>` : ""}
        <strong class="message-content text-white fs-2">${msg.message || ""}</strong>
        <br>
        <small class="text-muted">${new Date(msg.created_at).toLocaleTimeString()} ${seenTick}</small>
      </div>
    `;

    // ✅ Append message to wrapper instead of divider
    dividerWrapper.appendChild(msgEl);

    // Scroll to bottom
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
  }

















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



    if(data.guest){
      const formattedGuestDate = formatGuestDate(data.guest.date_of_visit);
      guestHTML = `
        <div class="chat-guest mb-1 p-2 border text-white rounded bg-gray">
          <img src="${data.guest.image}" style="width:150px;height:150px;border-radius:6px;object-fit:cover;margin-right:5px;">
          <strong class="text-warning">${data.guest.title} ${data.guest.name}</strong> (${data.guest.custom_id})<br>
          ${formattedGuestDate}
        </div>
      `;
    }

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


















// =========================
// CHAT PAGE INIT
// =========================
document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chatMessagesContainer");
  const chatForm = document.getElementById("chatReplyForm");
  const chatInput = document.getElementById("chatInput");
  const replyToIdInput = document.getElementById("replyToId");
  const attachmentPreview = document.getElementById("attachmentPreview");
  const replyIndicator = document.getElementById("replyIndicator");
  const replyToNameSpan = document.getElementById("replyToName");
  const clearBtn = document.getElementById("clearReplyBtn");
  const chatSearchInput = document.getElementById("chatSearchInput");

  let replyToId = null;
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

    // fallback if userId is invalid
    if (typeof userId !== "number" || isNaN(userId)) return "bg-gray-500 text-white";

    return colors[userId % colors.length];
  }

  // Assign user card colors safely
  document.querySelectorAll(".user-card").forEach(card => {
    const userId = parseInt(card.dataset.userid, 10);
    const colorClass = getUserColor(userId); // always returns a string
    card.classList.add(...colorClass.split(" "));
  });

  function setReply(id, name, message, guestCard = null) {
    replyToId = id;
    if (replyToIdInput) replyToIdInput.value = id;
    if (replyIndicator && replyToNameSpan) {
      replyIndicator.style.display = "flex";

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
  // Render guest details modal
  // =========================
  function renderGuestDetails(guest) {
    let html = `
      <div class="text-center mb-4">
        <div class="position-relative d-inline-block" style="width:100px; height:100px;">
          ${guest.picture
            ? `<span class="avatar avatar-xl rounded" 
                    style="background-image: url('${guest.picture}'); display:inline-block; width:100px; height:100px; border-radius:0.5rem; background-size:cover; background-position:center; box-shadow:0 2px 5px #008ca567,0 4px 10px #008ca567; transition: box-shadow 0.3s ease;"`
            : `<span class="avatar avatar-xl bg-grey text-white d-inline-flex align-items-center justify-content-center" 
                    style="width:100px; height:100px; font-weight:bold; font-size:24px; line-height:1; border-radius:0.5rem;">
              ${guest.full_name ? guest.full_name[0].toUpperCase() : "?"}
              </span>`}
        </div>

        <h3 class="m-0 mb-2 text-warning mt-2 fs-2">${guest.title} ${guest.full_name || "Unknown"}</h3>
        <div class="text-muted text-warning fs-3 fw-bold" style="font-family: monospace;">
          ${guest.custom_id || "-"}
        </div>

        ${guest.phone_number ? `<div class="mb-2 mt-2">
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

        <div class="mb-4">
          ${guest.social_media_accounts?.map(account => {
            if (!account.platform || !account.handle) return '';
            const colors = { linkedin: "#037ae9ff", whatsapp: "#03f74cff", instagram: "#de08f1ff", twitter: "#1DA1F2", tiktok: "#25ECE6" };
            let svgPaths = '';
            switch(account.platform) {
              case 'linkedin':
                svgPaths = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M8 11v5"/><path d="M8 8v.01"/><path d="M12 16v-5"/><path d="M16 16v-3a2 2 0 1 0 -4 0"/><path d="M3 7a4 4 0 0 1 4 -4h10a4 4 0 0 1 4 4v10a4 4 0 0 1 -4 4h-10a4 4 0 0 1 -4 -4z"/>`; break;
              case 'whatsapp':
                svgPaths = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 21l1.65 -3.8a9 9 0 1 1 3.4 2.9l-5.05 .9"/><path d="M9 10a.5 .5 0 0 0 1 0v-1a.5 .5 0 0 0 -1 0v1a5 5 0 0 0 5 5h1a.5 .5 0 0 0 0 -1h-1a.5 .5 0 0 0 0 1"/>`; break;
              case 'instagram':
                svgPaths = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 8a4 4 0 0 1 4 -4h8a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h-8a4 4 0 0 1 -4 -4z"/><path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/><path d="M16.5 7.5v.01"/>`; break;
              case 'twitter':
                svgPaths = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 4l11.733 16h4.267l-11.733 -16z"/><path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772"/>`; break;
              case 'tiktok':
                svgPaths = `<path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M21 7.917v4.034a9.948 9.948 0 0 1 -5 -1.951v4.5a6.5 6.5 0 1 1 -8 -6.326v4.326a2.5 2.5 0 1 0 4 2v-11.5h4.083a6.005 6.005 0 0 0 4.917 4.917z"/>`; break;
            }
            return `<a href="${account.handle}" target="_blank" class="text-white me-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="${colors[account.platform] || '#fff'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${svgPaths}</svg>
                    </a>`;
          }).join('')}
        </div>
      </div>
    `;

    // Fields timeline
    html += `<div class="row g-4">`;
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
      if ((index + 1) % 2 === 0 && index + 1 !== guest.field_data.length) html += `</div><div class="row g-4">`;
    });
    html += `</div>`;
    return html;
  }

  // =========================
  // Append chat message
  // =========================
  function appendMessage(msg) {
    if (!chatContainer || !msg.id) return;

    // Skip duplicates
    if (document.getElementById("msg-" + msg.id)) return;

    // --- Determine date key ---
    const msgDate = isoDateToLocal(msg.created_at);
    const key = dateKey(msgDate);

    // --- Find or create date wrapper ---
    let wrapper = el(`.date-wrapper[data-date="${key}"]`, chatContainer);
    let divider;

    if (!wrapper) {
      // Create date divider
      divider = document.createElement("div");
      divider.className = "date-divider sticky top-0 z-10 text-center py-1 bg-dark text-warning fw-bold";
      divider.dataset.date = key;
      divider.textContent = prettyDateLabel(msgDate);

      // Create wrapper for messages
      wrapper = document.createElement("div");
      wrapper.className = "date-wrapper";
      wrapper.dataset.date = key;

      // Append to container (chronological logic can come later)
      chatContainer.appendChild(divider);
      chatContainer.appendChild(wrapper);
    }

    // --- Create message bubble ---
    const msgEl = document.createElement("div");
    msgEl.id = "msg-" + msg.id;
    msgEl.className = msg.sender.id == window.currentUserId ? "text-end mb-2" : "text-start mb-2";

    const userColor = msg.sender.id == window.currentUserId ? "bg-green-lt text-white" : "bg-blue-lt text-white";

    msgEl.innerHTML = `
      <div class="message-bubble d-inline-block px-3 py-2 rounded-3 ${userColor}">
        <strong>${msg.sender.full_name || "Unknown"}</strong><br>
        ${msg.message || ""}
        <br>
        <small class="text-muted">${new Date(msg.created_at).toLocaleTimeString()}</small>
      </div>
    `;

    // Append message to wrapper
    wrapper.appendChild(msgEl);

    // Scroll to bottom
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
  }

  // =========================
  // Guest card hover
  // =========================
  document.addEventListener("mouseover", e => {
    const card = e.target.closest(".chat-guest-card");
    if (card) card.style.backgroundColor = "#191a181e";
  });

  document.addEventListener("mouseout", e => {
    const card = e.target.closest(".chat-guest-card");
    if (card) card.style.backgroundColor = "#11182781";
  });

  // =========================
  // WebSocket Setup
  // =========================
  let chatSocket;

  function connectChatSocket() {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = `${protocol}://${window.location.host}/ws/chat/`;
    chatSocket = new WebSocket(wsUrl);

    chatSocket.onopen = () => console.log("Chat WebSocket connected");
    chatSocket.onclose = () => setTimeout(connectChatSocket, 3000);
    chatSocket.onerror = err => console.error("Chat WebSocket error:", err);

    chatSocket.onmessage = event => {
      try {
        const data = JSON.parse(event.data);
        console.log("WS incoming:", data); // debug log
        if (data.type === "chat_message") {
          appendMessage(data.message);

          // Optional: Ensure newest messages are always scrolled into view
          chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
        }
      } catch (err) {
        console.error("Error parsing WS message:", err);
      }
    };
  }

  connectChatSocket();

  // =========================
  // Send chat via WS
  // =========================
  if (chatForm) {
    chatForm.onsubmit = e => {
      e.preventDefault();
      if (!chatInput.value.trim() && !replyToId && !selectedGuest) return;

      
      sendMessageWS();

      function sendMessageWS() {
        chatSocket.send(JSON.stringify({
          type: "chat_message",
          message: chatInput.value,
          parent_id: replyToId || null,
          guest_id: selectedGuest?.id || null,
        }));

        chatInput.value = "";
        selectedGuest = null;
        attachmentPreview.innerHTML = "";
        clearReply();
      }
    };
  }

  // =========================
  // Live search (with date wrappers)
  // =========================
  if (chatSearchInput) {
    chatSearchInput.addEventListener("input", () => {
      const query = chatSearchInput.value.toLowerCase();
      const allWrappers = chatContainer.querySelectorAll(".date-wrapper");
      const allDividers = chatContainer.querySelectorAll(".date-divider");

      allDividers.forEach(div => div.style.display = "none");
      allWrappers.forEach(wrapper => wrapper.style.display = "none");

      allWrappers.forEach(wrapper => {
        const messages = wrapper.querySelectorAll(".text-start, .text-end");
        let hasMatch = false;

        messages.forEach(msg => {
          const bubble = msg.querySelector(".message-bubble");
          if (!bubble) return;
          const matches = bubble.textContent.toLowerCase().includes(query);
          msg.style.display = matches ? "" : "none";
          if (matches) hasMatch = true;
        });

        if (hasMatch) {
          wrapper.style.display = "";
          const divider = wrapper.previousElementSibling;
          if (divider && divider.classList.contains("date-divider")) {
            divider.style.display = "";
          }
        }
      });
    });
  }

  // =========================
  // Guest selection
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

      const guestInitial = selectedGuest.full_name ? selectedGuest.full_name[0].toUpperCase() : "?";
      const guestVisual = selectedGuest.picture
        ? `<img src="${selectedGuest.picture}" alt="${selectedGuest.full_name}" style="width:60px; height:60px; object-fit:cover; border-radius:6px;">`
        : `<div class="avatar bg-gray d-flex align-items-center justify-content-center fs-3 fw-bold" style="width:60px; height:60px; border-radius:6px;">${guestInitial}</div>`;

      attachmentPreview.innerHTML = `
        <div class="reply-preview-container mb-2 ms-4 me-1">
          <div class="reply-preview text-white px-2 py-2 rounded-2 d-flex align-items-center justify-content-between gap-3"
              style="border-left: 8px solid #018f14ff; background-color: #11182781; font-style: normal; box-shadow: 0 4px 8px #0000004d;">
            <div class="d-flex align-items-center gap-3">
              ${guestVisual}
              <div>
                <div class="fw-bold text-warning">${selectedGuest.title} ${selectedGuest.full_name}</div>
                <div class="text-muted">${selectedGuest.custom_id}</div>
                <div>${selectedGuest.date_of_visit ? new Date(selectedGuest.date_of_visit).toLocaleDateString(undefined,{month:"short",day:"numeric",year:"numeric"}) : ""}</div>
              </div>
            </div>
            <button type="button" class="btn p-0 border-0 d-flex align-items-center justify-content-center clear-guest" style="width:16px; height:16px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
              </svg>
            </button>
          </div>
        </div>`;
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

  // =========================
  // Guest card click → modal
  // =========================
  document.addEventListener("click", e => {
    const guestCard = e.target.closest(".chat-guest-card");
    if (!guestCard) return;

    const guestId = guestCard.getAttribute("data-guest-id");
    if (!guestId) return;

    fetch(`/guest/${guestId}/detail/`)
      .then(res => res.json())
      .then(guest => {
        document.getElementById("chatGuestModalBody").innerHTML = renderGuestDetails(guest);
        const modalEl = document.getElementById("chatGuestModal");
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
      })
      .catch(err => console.error("Failed to load guest details", err));
  });

  // =========================
  // User card click
  // =========================
  document.querySelectorAll(".user-card").forEach(card => {
    const canViewGuests = card.dataset.canViewGuests === "true";

    card.addEventListener("click", e => {
      if (!canViewGuests) {
        e.preventDefault(); // prevent dropdown if user cannot view guests
      }
      // No need to manually toggle; Bootstrap handles it automatically
    });
  });

  // =========================
  // Call card click
  // =========================
  document.querySelectorAll(".call-card").forEach(card => {
    card.addEventListener("click", e => {
      const phoneNumber = card.dataset.phone;
      if (phoneNumber) {
        window.location.href = `tel:${phoneNumber}`;
      }
    });
  });

});
