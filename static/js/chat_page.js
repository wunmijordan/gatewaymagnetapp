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
    if (typeof userId !== "number" || isNaN(userId)) return "bg-gray-500 text-white";
    return colors[userId % colors.length];
  }

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
    let html = `<div class="text-center mb-4">`;
    html += guest.picture
      ? `<img src="${guest.picture}" alt="${guest.full_name}" class="avatar avatar-xl rounded" style="width:100px; height:100px; object-fit:cover;">`
      : `<div class="avatar avatar-xl bg-grey text-white d-inline-flex align-items-center justify-content-center fs-2 fw-bold" style="width:100px; height:100px;">${guest.full_name ? guest.full_name[0].toUpperCase() : "?"}</div>`;
    html += `<h3 class="m-0 mb-2 text-warning mt-2 fs-2">${guest.title} ${guest.full_name || "Unknown"}</h3>
      <div class="text-muted text-warning fs-3 fw-bold" style="font-family: monospace;">${guest.custom_id || "-"}</div>`;

    if (guest.phone_number) {
      html += `<div class="mb-2 mt-2"><a href="tel:${guest.phone_number}" class="btn btn-sm btn-green">Call</a></div>`;
    }

    html += `<div class="mb-4">`;
    html += guest.social_media_accounts?.map(account => {
      if (!account.platform || !account.handle) return '';
      return `<a href="${account.handle}" target="_blank" class="me-2 text-white">${account.platform}</a>`;
    }).join('');
    html += `</div></div>`;

    // Timeline fields
    html += `<div class="row g-4">`;
    guest.field_data.forEach((field, index) => {
      html += `<div class="col-12 col-md-6">
        <ul class="timeline">
          <li class="timeline-event">
            <div class="timeline-event-icon bg-x-lt d-flex align-items-center justify-content-center" style="width:32px; height:32px;">
              ${guest.svg_icons?.[field.icon] || ""}
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

    if (document.getElementById("msg-" + msg.id)) return;

    const msgDate = new Date(msg.created_at);
    const key = msgDate.toDateString();

    let wrapper = chatContainer.querySelector(`.date-wrapper[data-date="${key}"]`);
    let divider;
    if (!wrapper) {
      divider = document.createElement("div");
      divider.className = "date-divider sticky top-0 z-10 text-center py-1 bg-dark text-warning fw-bold";
      divider.dataset.date = key;
      divider.textContent = key;

      wrapper = document.createElement("div");
      wrapper.className = "date-wrapper";
      wrapper.dataset.date = key;

      chatContainer.appendChild(divider);
      chatContainer.appendChild(wrapper);
    }

    const msgEl = document.createElement("div");
    msgEl.id = "msg-" + msg.id;
    msgEl.className = msg.sender.id == window.currentUserId ? "text-end mb-2" : "text-start mb-2";

    const userColor = msg.sender.id == window.currentUserId ? "bg-green-lt text-white" : "bg-blue-lt text-white";

    msgEl.innerHTML = `
      <div class="message-bubble d-inline-block px-3 py-2 rounded-3 ${userColor}">
        <strong>${msg.sender.full_name || "Unknown"}</strong><br>
        ${msg.message || ""}
        <br>
        <small class="text-muted">${msgDate.toLocaleTimeString()}</small>
      </div>
    `;

    wrapper.appendChild(msgEl);
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
  }

  // =========================
  // WebSocket Setup
  // =========================
  let chatSocket;

  function connectChatSocket() {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/`);

    chatSocket.onopen = () => console.log("Chat WS connected");
    chatSocket.onclose = () => setTimeout(connectChatSocket, 3000);
    chatSocket.onerror = err => console.error("Chat WS error:", err);

    chatSocket.onmessage = event => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "chat_message") appendMessage(data.message);
      } catch (err) { console.error(err); }
    };
  }

  connectChatSocket();

  // =========================
  // Send chat via WS + append locally
  // =========================
  if (chatForm) {
    chatForm.onsubmit = e => {
      e.preventDefault();
      if (!chatInput.value.trim() && !replyToId && !selectedGuest) return;

      const tempMsg = {
        id: "temp-" + Date.now(),
        sender: { id: window.currentUserId, full_name: window.currentUserName || "You" },
        message: chatInput.value,
        created_at: new Date().toISOString()
      };
      appendMessage(tempMsg);

      chatSocket.send(JSON.stringify({
        type: "chat_message",
        message: chatInput.value,
        parent_id: replyToId || null,
        guest_id: selectedGuest?.id || null
      }));

      chatInput.value = "";
      selectedGuest = null;
      attachmentPreview.innerHTML = "";
      clearReply();
    };
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
              style="border-left: 8px solid #018f14ff; background-color: #11182781;">
            <div class="d-flex align-items-center gap-3">
              ${guestVisual}
              <div>
                <div class="fw-bold text-warning">${selectedGuest.title} ${selectedGuest.full_name}</div>
                <div class="text-muted">${selectedGuest.custom_id}</div>
                <div>${selectedGuest.date_of_visit ? new Date(selectedGuest.date_of_visit).toLocaleDateString(undefined,{month:"short",day:"numeric",year:"numeric"}) : ""}</div>
              </div>
            </div>
            <button type="button" class="btn p-0 border-0 d-flex align-items-center justify-content-center clear-guest" style="width:16px; height:16px;">
              ✕
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
  // Live search
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
          if (divider && divider.classList.contains("date-divider")) divider.style.display = "";
        }
      });
    });
  }

});
