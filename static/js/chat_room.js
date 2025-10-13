document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chatMessagesContainer");
  const stickyDateHeader = document.getElementById("stickyDateHeader");
  const chatInput = document.getElementById("chatInput");
  const sendButton = document.getElementById("sendButton");
  const replyPreview = document.getElementById("replyPreview");
  const replyPreviewText = document.getElementById("replyPreviewText");
  const cancelReply = document.getElementById("cancelReply");
  const openBtn = document.getElementById("openUserGuestPopup");
  const popup = document.getElementById("userGuestPopup");
  const popupBody = document.getElementById("popupBody");
  const popupSearch = document.getElementById("popupSearch");
  const closeBtn = document.getElementById("popupClose");
  const optionsPanel = document.getElementById("chatOptionsPanel");
  const scrollToBottomBtn = document.getElementById("scrollToBottomBtn");
  const mentionDropdown = document.getElementById("mentionDropdown");

  const fileInput = document.getElementById("fileInput");
  const openFileAttach = document.getElementById("openFileAttach");
  const filePreviewContainer = document.getElementById("filePreviewContainer");
  const filePreviewContent = document.getElementById("filePreviewContent");
  const cancelFilePreview = document.getElementById("cancelFilePreview");
  //const roomId = chatContainer.dataset.roomId;

  // Handle all back buttons (desktop + mobile)
  document.querySelectorAll(".chat-back-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      window.history.back();
    });
  });

  let chatSocket = null;

  function connectSocket() {
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    chatSocket = new WebSocket(`${wsScheme}://${window.location.host}/ws/chat/`);

    chatSocket.onopen = () => {
      console.log("✅ Connected to WebSocket");
    };

    chatSocket.onclose = (e) => {
      console.log("❌ Socket closed. Reconnecting in 3s...", e.reason);
      setTimeout(connectSocket, 3000); // 🔄 auto-reconnect
    };

    chatSocket.onerror = (err) => {
      console.error("Socket error:", err);
      chatSocket.close();
    };

    chatSocket.onmessage = (e) => {
      const data = JSON.parse(e.data);

      // 🔍 Debug log
      console.log("📩 Incoming WebSocket data:", data);

      // Update your local USER_GUESTS
      if (data.guest && data.guest.assigned_user) {
        const idx = USER_GUESTS.findIndex(g => g.id === data.guest.id);
        if (idx !== -1) USER_GUESTS[idx].assigned_user = data.guest.assigned_user;
      }

      if (data.type === "chat_message" || data.message) {
        appendMessage(data);
        return;
      }

      if (data.type === "pinned_preview") {
        // Initial load or refresh (server sends last 3 pinned)
        pinnedMessages.length = 0;
        (data.messages || []).forEach(m => addPinnedMessage(m));
        renderPinnedPreview();
        return;
      }

      // Individual message pinned toggles (no full message payload)
      if (data.type === "message_pinned") {
        const ids = data.message_ids || [];
        const pinnedMap = data.pinned || {};
        const pinner = data.pinned_by || null;
        ids.forEach(id => {
          const node = document.getElementById(`chat-bubble-${id}`);
          if (!node) return;
          const flags = node.querySelector('.chat-bubble-flags');
          const shouldPin = pinnedMap[String(id)] || pinnedMap[id];
          if (shouldPin) {
            if (!node.querySelector('.pin-flag')) {
              const pin = document.createElement('span');
              pin.classList.add('pin-flag');
              pin.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#f703d7ff" class="bi bi-pin-angle-fill" viewBox="0 0 16 16">
                <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a6 6 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182c-.195.195-1.219.902-1.414.707s.512-1.22.707-1.414l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a6 6 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146"/>
              </svg>`;
              flags?.appendChild(pin);
            }
            // 🔹 Add pinned preview immediately with pinner info
            addPinnedMessage({
              id,
              message: node.querySelector('.chat-bubble-body')?.innerText || "",
              original_sender_id: node.dataset.senderId,
              original_sender_name: node.dataset.senderName,
              original_sender_title: node.dataset.senderTitle,
              pinned_by: pinner,   // ✅ include this
              pinned: true,
              pinned_at: new Date().toISOString()
            });
          } else {
            const el = node?.querySelector('.pin-flag');
            if (el) el.remove();
            removePinnedMessage(id);
          }
        });
        removePinnedMessage();
        return;
      }

      if (data.action === "pin_update" || data.action === "pin") {
        (data.pins || []).forEach(p => {
          const id = p.id || p.message_id || p;
          if (p.pinned) {
            // if full message present, add to preview stack
            if (p.message) {
              addPinnedMessage(p);
            } else {
              // just toggle flag on bubble if present
              const node = document.getElementById(`chat-bubble-${id}`);
              if (node && !node.querySelector('.pin-flag')) {
                const flags = node.querySelector('.chat-bubble-flags');
                const pin = document.createElement('span');
                pin.classList.add('pin-flag');
                pin.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#f703d7ff" class="bi bi-pin-angle-fill" viewBox="0 0 16 16">
                    <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a6 6 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182c-.195.195-1.219.902-1.414.707s.512-1.22.707-1.414l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a6 6 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146"/>
                  </svg>`;
                flags?.appendChild(pin);
              }
            }
          } else {
            removePinnedMessage(id);
            const node = document.getElementById(`chat-bubble-${id}`);
            const el = node?.querySelector('.pin-flag');
            if (el) el.remove();
          }
        });
        return;
      }

      // Fallback: if server sent other non-message payloads, ignore
      console.warn("Skipping non-message payload:", data);
    };

  }
  // Call this once when the page loads
  connectSocket();

  function getUserColor(userId) {
    const colors = ["bg-blue-lt text-white","bg-green-lt text-white","bg-orange-lt text-white","bg-purple-lt text-white","bg-pink-lt text-white","bg-cyan-lt text-white","bg-yellow-lt text-white","bg-red-lt text-white","bg-indigo-lt text-white","bg-teal-lt text-white","bg-lime-lt text-white","bg-amber-lt text-white","bg-fuchsia-lt text-white","bg-emerald-lt text-white","bg-violet-lt text-white","bg-rose-lt text-white","bg-sky-lt text-white","bg-orange-200 text-white","bg-purple-200 text-white","bg-pink-200 text-white"];
    return colors[userId % colors.length];
  }

  let selectedGuest = null;
  let replyToId = null;
  let selectedBubbles = new Set(); // selected message IDs
  let lastSelectionClick = null;    // for detecting single-selection for edit/reply
  const isTouch = ("ontouchstart" in window);
  let loading = false;
  let oldestLoaded = null; // track oldest message timestamp
  const limit = 50;
  let lastMessageDate = null;
  let pinnedMessages = []; // local cache (max 3, FIFO)
  // --- Utility: escape user-provided strings for RegExp ---
  function escapeRegex(str) {
    if (str == null) return "";
    return String(str).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  // --- Input listener for "@" ---
  // Use users JSON from Django
  const usersList = USERS.map(u => ({
      id: u.id,
      full_name: u.full_name || u.username,
      title: u.title || "",
      username: u.username,
      image: u.image || null,
      color: (u.color && u.color.trim() !== "") ? u.color : "#00aeff71"
  }));

  function getInputText() {
    if (!chatInput) return "";
    return (chatInput.innerText || "").trim();
  }
  function clearInput() { chatInput.innerHTML = ""; }

  let mentions = [];
  let filteredUsers = [];
  let currentSelection = 0;

  // --- Show dropdown above the input ---
  function showMentionDropdown() {
    if (!filteredUsers.length) return hideMentionDropdown();

    mentionDropdown.innerHTML = filteredUsers.map((u, idx) => `
      <div class="mention-item ${idx === currentSelection ? 'active' : ''}" data-id="${u.id}">
        <span class="avatar" style="${u.image ? 'background-image:url(' + u.image + ')' : ''}">
          ${!u.image ? (u.full_name || u.username).slice(0,2).toUpperCase() : ''}
        </span>
        <div class="user-info d-flex">
          <span class="title">${u.title || ''}</span>
          <span class="name">${u.full_name}</span>
        </div>
      </div>
    `).join('');

    mentionDropdown.classList.remove("d-none");
    mentionDropdown.style.display = "block";

    // Position above input
    const parentRect = chatInput.offsetParent.getBoundingClientRect();
    const inputRect = chatInput.getBoundingClientRect();
    const dropdownHeight = mentionDropdown.offsetHeight;
    mentionDropdown.style.left = (inputRect.left - parentRect.left) + "px";
    mentionDropdown.style.top = (inputRect.top - parentRect.top - dropdownHeight - 4) + "px";
    mentionDropdown.style.minWidth = chatInput.offsetWidth + "px";
  }

  function hideMentionDropdown() {
    mentionDropdown.classList.add("d-none");
    mentionDropdown.style.display = "none";
    currentSelection = 0;
  }

  // --- Insert mention into contenteditable ---
  function selectMention(item) {
    const userId = item.dataset.id;
    const user = filteredUsers.find(u => u.id == userId);
    if (!user) return;

    const titlePrefix = user.title ? (user.title + " ") : "";
    const mentionText = `@${titlePrefix}${user.full_name} `;

    // Always get fresh selection
    chatInput.focus();
    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);

    // Find text before cursor in current node
    let nodeText = range.startContainer.textContent || "";
    const before = nodeText.slice(0, range.startOffset);

    // Delete `@query` before cursor if it exists
    const match = before.match(/@([^\s@]*)$/);
    if (match) {
      range.setStart(range.startContainer, before.length - match[0].length);
      range.deleteContents();
    }

    // Insert mention
    const node = document.createTextNode(mentionText);
    range.insertNode(node);

    // Move caret after mention
    range.setStartAfter(node);
    range.setEndAfter(node);
    sel.removeAllRanges();
    sel.addRange(range);

    hideMentionDropdown();
  }

  function updateActive() {
    const items = mentionDropdown.querySelectorAll("div[data-id]");
    items.forEach((el, idx) =>
      el.classList.toggle("active", idx === currentSelection)
    );
  }

  // --- Detect mentions on input ---
  chatInput.addEventListener("input", () => {
    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);

    const textBeforeCursor =
      range.startContainer.textContent?.slice(0, range.startOffset) || "";

    const match = textBeforeCursor.match(/@([^\s@]*)$/);
    if (match) {
      const query = match[1].toLowerCase();
      filteredUsers = USERS.filter((u) => {
        const fullName = (u.full_name || u.username).toLowerCase();
        const title = (u.title || "").toLowerCase();
        return `${title} ${fullName}`.includes(query);
      });
      currentSelection = 0;
      showMentionDropdown();
    } else {
      hideMentionDropdown();
    }
  });

  // --- Keyboard navigation ---
  chatInput.addEventListener("keydown", (e) => {
    const items = mentionDropdown.querySelectorAll("div[data-id]");
    const isDropdownOpen = !mentionDropdown.classList.contains("d-none");

    if (!isDropdownOpen || !items.length) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      currentSelection = (currentSelection + 1) % items.length;
      updateActive();
      return;
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      currentSelection = (currentSelection - 1 + items.length) % items.length;
      updateActive();
      return;
    }

    if (e.key === "Enter" || e.key === "Tab") {
      e.preventDefault();
      selectMention(items[currentSelection]);
      return; // ✅ stop here, no newline logic
    }

    if (e.key === "Escape") {
      e.preventDefault();
      hideMentionDropdown();
      return;
    }
  });

  // --- Click/tap on mention item ---
  mentionDropdown.addEventListener("mousedown", (e) => {
    // use mousedown so selection isn’t lost before click
    e.preventDefault();
    const item = e.target.closest("div[data-id]");
    if (item) selectMention(item);
  });

  // --- Expose mentions array for sendMessage ---
  //window.getCurrentMentions = () => mentions;
  //window.clearMentions = () => { mentions = []; };


  // Format timestamp to "Sept. 15, 2025 - 11:10"
  function formatForCopy(iso) {
    const d = new Date(iso);
    const months = ["Jan.","Feb.","Mar.","Apr.","May","Jun.","Jul.","Aug.","Sept.","Oct.","Nov.","Dec."];
    const datePart = `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    const timePart = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
    return `${datePart} - ${timePart}`;
  }

  // Example: when right-clicking a message
  document.querySelectorAll(".chat-message").forEach(msg => {
    msg.addEventListener("contextmenu", e => {
      e.preventDefault();
      const isPinned = msg.dataset.pinned === "true"; // <-- set this when pinning
      updatePinButton(isPinned);
      // show options panel...
    });
  });


  function updateOptionsPanelVisibility() {
    if (selectedBubbles.size > 0) {
      optionsPanel.classList.remove("hidden");
      optionsPanel.setAttribute("aria-hidden", "false");
    } else {
      optionsPanel.classList.add("hidden");
      optionsPanel.setAttribute("aria-hidden", "true");
    }
  }

  // Utility: gather selected bubble DOM nodes
  function getSelectedNodes() {
    return Array.from(selectedBubbles).map(id => document.getElementById(`chat-bubble-${id}`)).filter(Boolean);
  }

  // Toggle selection (highlight) for a single bubble
  function toggleBubbleSelection(bubbleEl, messageId) {
    if (selectedBubbles.has(messageId)) {
      selectedBubbles.delete(messageId);
      bubbleEl.classList.remove("selected");
    } else {
      selectedBubbles.add(messageId);
      bubbleEl.classList.add("selected");
    }
    updateOptionsPanelVisibility();
    // focus input on reply candidate (UX)
    chatInput.focus();
  }

  // Clear all selections
  function clearSelections() {
    getSelectedNodes().forEach(node => node.querySelector(".chat-bubble")?.classList.remove("selected"));
    selectedBubbles.clear();
    updateOptionsPanelVisibility();
  }



  // Use existing DOM container with id="pinnedPreview" if present
  const pinnedPreviewContainer = document.getElementById('pinnedPreview') || document.querySelector('.pinned-preview');

  // Render the pinned preview stack
  function renderPinnedPreview() {
    const container = pinnedPreviewContainer;
    if (!container) return;
    container.innerHTML = "";

    pinnedMessages.forEach(msg => {
      // Outer wrapper
      const outer = document.createElement("div");
      outer.classList.add("pinned-outer");
      outer.dataset.id = msg.id;

      // Pin icon
      const icon = document.createElement("div");
      icon.classList.add("pinned-icon");
      icon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#f703d7ff" class="bi bi-pin" viewBox="0 0 16 16">
          <path d="M4.146.146A.5.5 0 0 1 4.5 0h7a.5.5 0 0 1 .5.5c0 .68-.342 1.174-.646 1.479-.126.125-.25.224-.354.298v4.431l.078.048c.203.127.476.314.751.555C12.36 7.775 13 8.527 13 9.5a.5.5 0 0 1-.5.5h-4v4.5c0 .276-.224 1.5-.5 1.5s-.5-1.224-.5-1.5V10h-4a.5.5 0 0 1-.5-.5c0-.973.64-1.725 1.17-2.189A6 6 0 0 1 5 6.708V2.277a3 3 0 0 1-.354-.298C4.342 1.674 4 1.179 4 .5a.5.5 0 0 1 .146-.354m1.58 1.408-.002-.001zm-.002-.001.002.001A.5.5 0 0 1 6 2v5a.5.5 0 0 1-.276.447h-.002l-.012.007-.054.03a5 5 0 0 0-.827.58c-.318.278-.585.596-.725.936h7.792c-.14-.34-.407-.658-.725-.936a5 5 0 0 0-.881-.61l-.012-.006h-.002A.5.5 0 0 1 10 7V2a.5.5 0 0 1 .295-.458 1.8 1.8 0 0 0 .351-.271c.08-.08.155-.17.214-.271H5.14q.091.15.214.271a1.8 1.8 0 0 0 .37.282"/>
        </svg>
      `;

      // Pinner info
      const pinner = document.createElement("div");
      pinner.classList.add("pinner");
      if (msg.pinned_by && msg.pinned_by.id === CURRENT_USER_ID) {
        pinner.textContent = "You pinned";
      } else if (msg.pinned_by) {
        pinner.textContent = `${msg.pinned_by.title || ""} ${msg.pinned_by.name} pinned`;
      } else {
        pinner.textContent = "Pinned";
      }

      // Preview bubble
      const preview = document.createElement("div");
      preview.classList.add("pinned-info");
      const senderTitle = msg.original_sender_title || "";
      const senderName = msg.original_sender_name || msg.sender_name || "Unknown";
      const sender = `${senderTitle} ${senderName}`.trim();
      const text = msg.message || msg.message_text || "(Guest Card)";
      const previewText = `${sender}: ${text}`;
      preview.textContent = previewText.length > 140 ? previewText.slice(0, 137) + "..." : previewText;

      // Click-to-scroll
      preview.addEventListener("click", () => {
        const wrapper = document.getElementById(`chat-bubble-${msg.id}`);
        if (wrapper) {
          const bubble = wrapper.querySelector(".chat-bubble");
          if (bubble) {
            bubble.scrollIntoView({ behavior: "smooth", block: "center" });
            bubble.classList.add("highlight-pinned");
            setTimeout(() => bubble.classList.remove("highlight-pinned"), 5000);
          }
        }
      });

      outer.appendChild(icon);
      outer.appendChild(pinner);
      outer.appendChild(preview);
      container.appendChild(outer);
    });
  }

  // Add or update a pinned message in FIFO (max 3)
  function addPinnedMessage(msg) {
    // Check for duplicates
    const exists = pinnedMessages.find(m => String(m.id) === String(msg.id));
    if (exists) return;

    // Enforce 14-day expiry if pinned_at exists
    if (msg.pinned_at) {
      const pinnedAt = new Date(msg.pinned_at);
      if (isNaN(pinnedAt.getTime()) || (Date.now() - pinnedAt.getTime()) > 14 * 24 * 60 * 60 * 1000) return;
    }

    // Keep max 3, FIFO
    if (pinnedMessages.length >= 3) {
      pinnedMessages.shift();
    }

    pinnedMessages.push(msg);
    renderPinnedPreview();
  }

  // Remove a message from preview
  function removePinnedMessage(id) {
    const idx = pinnedMessages.findIndex(m => String(m.id) === String(id));
    if (idx !== -1) {
      pinnedMessages.splice(idx, 1);
      renderPinnedPreview();
    }
  }


  document.getElementById("pinBtn").addEventListener("click", () => {
    if (!selectedBubbles.size) return;

    const ids = Array.from(selectedBubbles);

    // ✅ Just tell the server
    chatSocket.send(JSON.stringify({
      action: "pin",
      message_ids: ids,
      sender_id: CURRENT_USER_ID
    }));

    clearSelections();
  });

  







  // Guest Date of Visit Formatting
  function formatGuestDate(dateStr) {
    if (!dateStr) return "";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateStr).toLocaleDateString(undefined, options);
  }

  // --- Safe Date Parser ---
  function safeParseDate(isoString) {
    if (!isoString) return null;
    // Strip microseconds like .123456
    const cleaned = isoString.replace(/\.\d+/, "");
    const d = new Date(cleaned);
    return isNaN(d.getTime()) ? null : d;
  }

  // --- Update getDateText to use safe date ---
  function getDateText(date) {
    if (!date) return "";
    const now = new Date();
    const msgDay = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    if (msgDay.getTime() === today.getTime()) return "Today";
    if (msgDay.getTime() === yesterday.getTime()) return "Yesterday";

    const diffTime = today.getTime() - msgDay.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays < 7) return msgDay.toLocaleDateString(undefined, { weekday: "long" });

    return msgDay.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  }

  // Attach from Guest list to Chat handler
  document.querySelectorAll(".attach-to-chat").forEach(item => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      
      let guest = JSON.parse(e.currentTarget.getAttribute("data-guest"));

      // 🔹 ALWAYS populate assigned_user from your arrays
      const matchedGuest =
        USER_GUESTS.find(g => g.id === guest.id) ||
        UNASSIGNED_GUESTS.find(g => g.id === guest.id);

      guest.assigned_user = matchedGuest?.assigned_user || null;

      createGuestPreview(guest);
      chatInput.focus();
      chatInput.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });


  // 🔹 File type icons
  function getFileIcon(ext, type) {
    const size = 96; // bigger icons for visibility
    const commonAttrs = `xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" 
                        viewBox="0 0 24 24" fill="none" stroke="currentColor" 
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="icon icon-tabler" style="color:#f8fafc;">`;

    if (ext === "pdf" || type.includes("pdf")) return `
      <svg ${commonAttrs}>
        <path stroke="#961822ff" d="M0 0h24v24H0z" fill="none"/>
        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
        <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" />
        <path d="M5 18h1.5a1.5 1.5 0 0 0 0 -3h-1.5v6" />
        <path d="M17 18h2" /><path d="M20 15h-3v6" />
        <path d="M11 15v6h1a2 2 0 0 0 2 -2v-2a2 2 0 0 0 -2 -2h-1z" />
      </svg>`;

    if (["doc", "docx"].includes(ext)) return `
      <svg ${commonAttrs}>
        <path stroke="#182496ff" d="M0 0h24v24H0z" fill="#182496ff"/>
        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
        <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" />
        <path d="M5 15v6h1a2 2 0 0 0 2 -2v-2a2 2 0 0 0 -2 -2h-1z" />
        <path d="M20 16.5a1.5 1.5 0 0 0 -3 0v3a1.5 1.5 0 0 0 3 0" />
        <path d="M12.5 15a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1 -3 0v-3a1.5 1.5 0 0 1 1.5 -1.5z" />
      </svg>`;

    if (["xls", "xlsx", "csv"].includes(ext)) return `
      <svg ${commonAttrs}>
        <path stroke="#189618ff" d="M0 0h24v24H0z" fill="#189618ff"/>
        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
        <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" />
        <path d="M4 15l4 6" /><path d="M4 21l4 -6" />
        <path d="M17 20.25c0 .414 .336 .75 .75 .75h1.25a1 1 0 0 0 1 -1v-1a1 1 0 0 0 -1 -1h-1
                a1 1 0 0 1 -1 -1v-1a1 1 0 0 1 1 -1h1.25a.75 .75 0 0 1 .75 .75" />
        <path d="M11 15v6h3" />
      </svg>`;

    if (["ppt", "pptx"].includes(ext)) return `
      <svg ${commonAttrs}>
        <path stroke="#963c18ff" d="M0 0h24v24H0z" fill="none"/>
        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
        <path d="M5 18h1.5a1.5 1.5 0 0 0 0 -3h-1.5v6" />
        <path d="M11 18h1.5a1.5 1.5 0 0 0 0 -3h-1.5v6" />
        <path d="M16.5 15h3" /><path d="M18 15v6" />
        <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" />
      </svg>`;

    if (["zip", "rar", "7z", "tar", "gz"].includes(ext)) return `
      <svg ${commonAttrs}>
        <path stroke="#961885ff" d="M0 0h24v24H0z" fill="none"/>
        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
        <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" />
        <path d="M16 18h1.5a1.5 1.5 0 0 0 0 -3h-1.5v6" />
        <path d="M12 15v6" /><path d="M5 15h3l-3 6h3" />
      </svg>`;

    // Fallback generic file
    return `
      <svg ${commonAttrs} fill="currentColor" class="icon-tabler icon-tabler-file">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
        <path d="M12 2l.117 .007a1 1 0 0 1 .876 .876l.007 .117v4l.005 .15a2 2 0 0 0 
                1.838 1.844l.157 .006h4l.117 .007a1 1 0 0 1 .876 .876l.007 .117v9
                a3 3 0 0 1 -2.824 2.995l-.176 .005h-10a3 3 0 0 1 -2.995 -2.824
                l-.005 -.176v-14a3 3 0 0 1 2.824 -2.995l.176 -.005h5z" />
        <path d="M19 7h-4l-.001 -4.001z" />
      </svg>`;
  }


  //File Attachment Preview
  let selectedFile = null;

  document.getElementById("attachFileBtn").addEventListener("click", () => {
    document.getElementById("fileInput").click();
  });

  document.getElementById("fileInput").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    createFilePreview(file);
    chatInput.focus();
    chatInput.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  function createFilePreview(file) {
    removeFilePreview();
    selectedFile = file;

    const preview = document.createElement("div");
    preview.id = "filePreview";
    preview.classList.add(
      "d-flex","align-items-center","text-white",
      "border-0","p-2","mb-2","rounded-2","bg-gray-900"
    );
    preview.style.boxShadow = "0 4px 8px #0000004d";

    const type = (file.type || "").toLowerCase();
    const ext = file.name.split(".").pop().toLowerCase();
    let thumb = "";

    if (type.startsWith("image/")) {
      thumb = `<img src="${URL.createObjectURL(file)}"
                    style="max-width:60px; max-height:60px; object-fit:cover; border-radius:4px; margin-right:10px;">`;
    } else if (type.startsWith("video/")) {
      thumb = `<video src="${URL.createObjectURL(file)}"
                      style="max-width:60px; max-height:60px; border-radius:4px; margin-right:10px;" muted></video>`;
    } else if (type.startsWith("audio/")) {
      thumb = `<audio src="${URL.createObjectURL(file)}"
                      style="width:120px; margin-right:10px;" controls></audio>`;
    } else if (ext === "pdf") {
      thumb = `<embed src="${URL.createObjectURL(file)}" type="application/pdf"
                      style="width:60px; height:60px; border-radius:4px; margin-right:10px;">`;
    } else {
      // ✅ use your new icon function for docs/zip/etc
      thumb = `<div style="width:60px;height:60px;display:flex;align-items:center;justify-content:center;
                          background:#1f2937;border-radius:6px;margin-right:10px;">
                ${getFileIcon(ext, type)}
              </div>`;
    }

    preview.innerHTML = `
      ${thumb}
      <div class="flex-grow-1 overflow-hidden">
        <strong class="text-white text-truncate d-block" style="max-width:160px;">${file.name}</strong>
        <small class="text-muted">${(file.size / 1024).toFixed(1)} KB</small>
      </div>
      <span id="cancelFilePreview" class="text-red ms-2"
              style="background:none;border:none;">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
            viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="icon icon-tabler icon-tabler-x">
          <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
          <path d="M18 6l-12 12" /><path d="M6 6l12 12" />
        </svg>
      </span>
    `;

    document.getElementById("guestPreviewContainer").appendChild(preview);

    document.getElementById("cancelFilePreview").addEventListener("click", removeFilePreview);
    adjustPreviewPositions();
  }

  function removeFilePreview() {
    const preview = document.getElementById("filePreview");
    if (preview) preview.remove();
    selectedFile = null;
  }

  //Link Preview
  let selectedLinkPreview = null;
  let linkPreviewTimeout = null;

  // Listen to chat input
  chatInput.addEventListener("input", () => {
    clearTimeout(linkPreviewTimeout);
    linkPreviewTimeout = setTimeout(() => {
      // use innerText instead of value for contenteditable
      const text = (chatInput.innerText || "").trim();
      const firstWord = text.split(/\s+/)[0] || "";
      const url = extractURLIfFirstWord(firstWord);

      if (url) {
        // Only fetch if the first link changed
        if (!selectedLinkPreview || selectedLinkPreview.url !== url) {
          fetchLinkPreview(url);
        }
      } else {
        removeLinkPreview();
      }
    }, 300); // debounce 300ms
  });

  // Extract URL only if it is the first word
  function extractURLIfFirstWord(text) {
    if (!text) return null;

    // Regex matches http(s), www, or bare domains with optional port/path
    const urlRegex = /^(https?:\/\/[^\s]+|www\.[^\s]+|[\w.-]+\.[a-z]{2,}(?::\d+)?(?:\/[^\s]*)?)$/i;
    const match = text.match(urlRegex);
    if (!match || !match[0]) return null;

    let url = match[0];
    if (!/^https?:\/\//i.test(url)) url = "https://" + url; // prepend https if missing
    return url;
  }

  // Fetch link preview
  async function fetchLinkPreview(url) {
    try {
      const res = await fetch(`/accounts/fetch_link_preview/?url=${encodeURIComponent(url)}`);
      const data = await res.json();
      if (res.ok && data.title) {
        selectedLinkPreview = data;
        createLinkPreview(data);
      }
    } catch (err) {
      console.error("Link preview fetch failed:", err);
    }
  }

  // Render the preview (same as before)
  function createLinkPreview(previewData) {
    removeLinkPreview();
    selectedLinkPreview = previewData;

    const preview = document.createElement("div");
    preview.id = "linkPreview";
    preview.classList.add("d-flex","align-items-center","text-white","border-0","p-2","mb-2","rounded-2","bg-gray-900");
    preview.style.boxShadow = "0 4px 8px #0000004d";

    preview.innerHTML = `
      ${previewData.image
        ? `<img src="${previewData.image}" style="width:60px;height:60px;border-radius:4px;object-fit:cover;margin-right:10px;">`
        : `<span class="avatar bg-blue-lt d-flex align-items-center justify-content-center"
                  style="width:60px;height:60px;border-radius:4px;margin-right:10px;">🌐</span>`}
      <div class="flex-grow-1">
        <div class="fw-bold text-white text-truncate" style="max-width: calc(100% - 10px);" title="${previewData.title}">
          ${previewData.title}
        </div>
        <div class="text-muted small" style="display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
          ${previewData.description || ''}
        </div>
        <div class="text-secondary small">${new URL(previewData.url).hostname}</div>
      </div>
      <span id="cancelLinkPreview" class="avatar text-red p-0 border-0 d-flex align-items-center justify-content-center"
            style="width:24px; height:24px; cursor:pointer;">
        ✖
      </span>
    `;

    document.getElementById("guestPreviewContainer").appendChild(preview);
    document.getElementById("cancelLinkPreview").addEventListener("click", removeLinkPreview);
    adjustPreviewPositions();
  }

  function removeLinkPreview() {
    const preview = document.getElementById("linkPreview");
    if (preview) preview.remove();
    selectedLinkPreview = null;
  }

  // Preview Position
  function adjustPreviewPositions() {
    const reply = document.getElementById("replyPreview");
    const guest = document.getElementById("guestPreview");

    if (reply && !reply.classList.contains("d-none")) {
      const guestHeight = guest ? guest.offsetHeight + 6 : 0;
      reply.style.bottom = `calc(100% + ${guestHeight}px)`;
    }
    if (guest) {
      guest.style.bottom = "100%";
    }
  }

  // Reply preview HTML (used for both reply bar + inside bubbles)
  function createReplyPreviewHTML(data, inBubble = false) {
    let replyOwner = "";

    if (data.parent) {
      if (data.parent.sender_id === CURRENT_USER_ID) {
        replyOwner = "You";
      } else {
        replyOwner = `${data.parent.sender_title} ${data.parent.sender_name}`;
      }
    }

    const innerHTML = data.parent
      ? `
        <small style="color: inherit;">${replyOwner}</small><br>
        <span class="reply-preview-text text-secondary">
          ${data.parent.message || ""}
        </span>
        ${
          data.parent.guest
            ? `<div class="d-flex align-items-center mt-1">
                ${
                  data.parent.guest.image
                    ? `<img src="${data.parent.guest.image}"
                            style="width:35px;height:35px;border-radius:4px;object-fit:cover;" />`
                    : `<span class="avatar bg-gray d-flex align-items-center justify-content-center"
                            style="width:35px;height:35px;border-radius:4px;">
                        ${data.parent.guest.name[0]}
                      </span>`
                }
                <span class="ms-2 text-warning">
                  ${data.parent.guest.title} ${data.parent.guest.name}
                </span>
              </div>`
            : ""
        }
      `
      : "";

    // Wrap in container only if it's for a bubble
    return inBubble
      ? `<div class="chat-reply-preview fs-7 mb-1 p-1 rounded"
                data-parent-id="${data.parent.id}"
                style="cursor:pointer; background: #111827;
                      border-left:4px solid #018f14ff; width:auto;
                      box-shadow: 0 4px 8px #0000004d;">
            ${innerHTML}
        </div>`
      : innerHTML;
  }

  // Chat Bubble Text Formatting
  function formatMessage(text) {
    let formatted = text
      // bold
      .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
      // italic
      .replace(/\*(.*?)\*/g, '<i>$1</i>')
      // underline
      .replace(/_(.*?)_/g, '<u>$1</u>')
      // highlight
      .replace(/==(.+?)==/g, '<span class="highlight">$1</span>');

    // Numbered list: 1. 2. etc
    //formatted = formatted.replace(/^(\s*)(\d+\.\s)/gm, '<span class="fw-bold">$1$2</span>');

    // Nested list: a. b. c. → italic
    //formatted = formatted.replace(/^(\s+)([a-z]\.\s)/gm, '<i>$1$2</i>');

    return formatted;
  }

  // Enhanced linkify for chat text
  function linkify(text) {
    if (!text) return "";

    const urlRegex = /\b(https?:\/\/[^\s]+|www\.[^\s]+|[\w.-]+\.[a-z]{2,}(?::\d+)?(?:\/[^\s]*)?)\b/gi;

    return text.replace(urlRegex, (match) => {
      let url = match;
      if (!/^https?:\/\//i.test(url)) url = "https://" + url;

      try {
        const parsed = new URL(url);
        const display = parsed.hostname.replace(/^www\./, "");
        return `<a href="${url}" target="_blank" rel="noopener noreferrer" 
                  class="text-cyan text-decoration-none">${display}</a>`;
      } catch {
        return match;
      }
    });
  }


  // Render Message
  function renderMessage(data, isPrepend = false) {
    //console.log("Incoming message:", data);
    const isMe = data.sender_id === CURRENT_USER_ID;

    const replyHTML = data.parent ? createReplyPreviewHTML({ parent: data.parent }, true) : "";

    const bubbleColorClass = isMe ? "bg-green-lt text-white" : data.color;

    const bubble = document.createElement("div");
    bubble.dataset.createdAt = data.created_at;
    bubble.classList.add("chat-item");
    bubble.id = `chat-bubble-${data.id}`;
    bubble.dataset.senderId = data.sender_id;   // 🔥 needed for edit check
    bubble.dataset.color = data.color || "";   // helpful for reply handler
    //bubble.dataset.edited = data.edited ? "true" : "false"; // if already edited

    let guestHTML = "";
    if (data.guest) {
      bubble.dataset.guest = JSON.stringify(data.guest);
      const formattedGuestDate = formatGuestDate(data.guest.date_of_visit);

      // Check if guest has an assigned user
      const assignedUser = data.guest.assigned_user; // make sure your guest object includes assigned user
      //if (assignedUser) {
      //  console.log("Assigned:", assignedUser.full_name);
      //} else {
      //  console.log("No assigned user");
      //}
      let assignedHTML = "";
      if (assignedUser) {
        assignedHTML = `
          <div class="assigned-user d-flex align-items-center gap-2">
            <div class="avatar rounded"
                style="width:32px; height:32px; background-color: #11182781; overflow:hidden; 
                        display:flex; align-items:center; justify-content:center; box-shadow: 0 4px 8px #000000a1;"">
              ${assignedUser.image
                  ? `<img src="${assignedUser.image}" alt="${assignedUser.full_name}" style="width:100%; height:100%; object-fit:cover;">`
                  : `${assignedUser.full_name ? assignedUser.full_name[0].toUpperCase() : "?"}`}
            </div>
            <span class="text-white small">${assignedUser.title || ''} ${assignedUser.full_name}</span>
          </div>
        `;
      }

      guestHTML = `
        <div class="chat-guest-card text-white text-center px-2 py-2 mb-2 rounded-2 d-flex flex-column align-items-center gap-2"
            style="max-width: 250px; box-shadow: 0 4px 8px #000000a1; background-color: #11182781;">
          ${data.guest.image
              ? `<img src="${data.guest.image}" alt="${data.guest.name}" 
                      style="width:200px; height:200px; object-fit:cover; border-radius:6px;
                      box-shadow: 0 4px 8px #000000a1;">`
              : `<div class="avatar bg-gray d-flex align-items-center justify-content-center fs-2 fw-bold"
                    style="width:200px; height:200px; border-radius:6px;
                    box-shadow: 0 4px 8px #000000a1;">
                  ${data.guest.name ? data.guest.name[0].toUpperCase() : "?"}
                </div>`}
          <div class="text-center mt-2">
            <div class="fw-bold fs-3 text-warning"
                  style="max-width: 200px; white-space: pre-wrap; word-break: break-word;">${data.guest.title} ${data.guest.name}</div>
            <div class="text-muted">${data.guest.custom_id}</div>
            <div>${formattedGuestDate}</div>
          </div>
          ${assignedHTML}
        </div>
      `;
    }

    // Render FIle Attachment
    function renderFilePreview(file) {
      if (!file) return "";

      const name = file.name || "file";
      const type = (file.type || "").toLowerCase();
      const ext = name.includes(".") ? name.split(".").pop().toLowerCase() : "";
      const sizeText = file.size ? `${(file.size/1024).toFixed(1)} KB` : "";
      const fileUrl = file.display_url || file.url;

      if (type.startsWith("image/")) {
        return `
          <div class="chat-file-card text-white px-2 py-2 mb-2 rounded-2 d-flex flex-column align-items-center gap-2"
              style="box-shadow: 0 4px 8px #000000a1; background-color: #11182781;">
            <a href="${file.url}" target="_blank">
              <img src="${file.url}" alt="${name}"
                  style="max-width:200px; max-height:200px; object-fit:cover; border-radius:6px;">
            </a>
            <div class="mt-1 small text-muted text-center" 
                  style="max-width: 200px; white-space: pre-wrap; word-break: break-word;">${name} · ${sizeText}</div>
          </div>`;
      }

      if (type.startsWith("video/")) {
        return `
          <div class="chat-file-card text-white px-2 py-2 mb-2 rounded-2 d-flex flex-column align-items-center gap-2"
              style="box-shadow: 0 4px 8px #000000a1; background-color: #11182781;">
            <div class="chat-file-card mb-2">
              <video src="${file.url}" controls
                    style="max-width:200px; max-height:150px; border-radius:6px;"></video>
            </div>
            <div class="mt-1 small text-muted text-center" 
                  style="max-width: 200px; white-space: pre-wrap; word-break: break-word;">${name} · ${sizeText}</div>
          </div>`;
      }

      if (type.startsWith("audio/")) {
        return `
          <div class="chat-file-card text-white px-2 py-2 mb-2 rounded-2 d-flex flex-column align-items-center gap-2"
              style="box-shadow: 0 4px 8px #000000a1; background-color: #11182781;">
            <div class="chat-file-card mb-2">
              <audio src="${file.url}" controls style="width:200px;"></audio>
            </div>
            <div class="mt-1 small text-muted text-center" 
                style="max-width: 200px; white-space: pre-wrap; word-break: break-word;">${name} · ${sizeText}</div>
          </div>`;
      }

      if (ext === "pdf") {
        return `
          <div class="chat-file-card text-white px-2 py-2 mb-2 rounded-2 d-flex flex-column align-items-center gap-2"
              style="box-shadow: 0 4px 8px #000000a1; background-color: #11182781;">
            <a href="${fileUrl}" target="_blank">
              <iframe src="${file.url}" type="application/pdf"
                    style="width:200px; height:200px; border-radius:6px;"></iframe>
              <div class="mt-1 small text-muted text-center" 
                  style="max-width: 200px; white-space: pre-wrap; word-break: break-word;">${name} · ${sizeText}</div>
            </a>
          </div>`;
      }

      // Generic doc / zip / etc with icon
      const icon = getFileIcon(ext, type);
      return `
        <div class="chat-file-card text-white px-2 py-2 mb-2 rounded-2 d-flex flex-column align-items-center gap-2"
              style="box-shadow: 0 4px 8px #000000a1; background-color: #11182781;">
          <a href="${file.url}" target="_blank" class="text-center" 
              style="text-decoration:none; max-width:200px; max-height:200px; object-fit:cover; border-radius:6px;">
            ${icon}  
            <div class="small text-white">${ext.toUpperCase()}</div>
          </a> 
          <div class="mt-1 small text-muted text-center mt-2" 
                style="max-width: 200px; white-space: pre-wrap; word-break: break-word;">${name} · ${sizeText}</div>          
        </div>`;
    }
    let fileHTML = data.file ? renderFilePreview(data.file) : "";

    // Render Link
    let linkHTML = "";
    if (data.link_preview) {
      const lp = data.link_preview;
      linkHTML = `
        <a href="${lp.url}" target="_blank" rel="noopener noreferrer"
          class="chat-link-card text-white text-decoration-none px-2 py-2 mb-2 rounded-2 d-flex align-items-center gap-2"
          style="box-shadow:0 4px 8px #000000a1; background-color: #11182781; max-width:100%; overflow:hidden;">
          
          ${lp.image
            ? `<img src="${lp.image}" style="flex-shrink:0; width:60px; height:60px; border-radius:4px; object-fit:cover;">`
            : `<span class="avatar bg-blue-lt d-flex align-items-center justify-content-center"
                      style="flex-shrink:0; width:60px; height:60px; border-radius:4px;">🌐</span>`}
          
          <div class="flex-grow-1 overflow-hidden" style="max-width:100%;">
            <div class="fw-bold text-white text-truncate" 
                style="display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" 
                title="${lp.title}">
              ${lp.title}
            </div>
            <div class="text-muted small" 
                style="display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; text-overflow:ellipsis; word-break:break-word;">
              ${lp.description || ''}
            </div>
            <div class="text-secondary small text-truncate" style="overflow:hidden; text-overflow:ellipsis;">
              ${new URL(lp.url).hostname}
            </div>
          </div>
        </a>
      `;
    }

    const avatarHTML = data.sender_image
      ? `<span class="avatar rounded" style="background-image:url('${data.sender_image}'); width:20px; height:20px; background-size:cover; background-position:center;"></span>`
      : `<span class="avatar ${data.color || ''} d-flex align-items-center justify-content-center border-0 rounded"
            style="width:20px; height:20px; font-weight:normal; border-radius:8px">
          ${
            data.sender_name
              ? (data.sender_name.split(" ").map(n => n[0])[0] || data.sender_name[0])
              : "?" // fallback placeholder
          }
        </span>`;

    const messageHTML = linkify(renderMessageWithMentions(data.message, data.mentions));
    bubble.innerHTML = `
      <div class="d-flex align-items-end ${isMe ? "justify-content-end" : ""}">
        ${!isMe ? `<div class="me-1">${avatarHTML}</div>` : ""}
        <div class="chat-bubble ${isMe ? 'chat-bubble-me' : ""} ${bubbleColorClass}"
            style="box-shadow: 0 4px 8px #000000d2; display: flex; flex-direction: column;
                    align-items: stretch; cursor: pointer; max-width: 75%; left: 20px border-radius: 12px; width: fit-content;">
          ${!isMe ? `
            <div class="chat-bubble-title" style="font-size: 0.75rem;">
              <small><i class="chat-bubble-author" style="color: inherit;">
                ${data.sender_title || ""} ${data.sender_name}
              </i></small>
            </div>` : ""}
          <div class="chat-bubble-body" style="display: block; gap: 0.5rem; padding: 0;">
            ${replyHTML}
            ${guestHTML}
            ${fileHTML}
            ${linkHTML}

            ${data.message?.trim() ? `<div class="message-row" style="display: block; margin: 0;">
              <div class="fs-4 text-white"
                  style="white-space: pre-wrap; word-break: break-word; margin:0; padding:0;">${formatMessage(messageHTML)}</div></div>` : ""}
            <div style="display:flex; justify-content:flex-end; width:100%;">
              <small class="chat-bubble-date text-muted"
                    style="white-space: nowrap; font-size: 0.6rem;" 
                    data-full-date="${data.created_at}">
                ${new Date(data.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
              </small>
            </div>
            <div class="chat-bubble-flags"></div>
          </div>
        </div>
      </div>
    `;

    //📌 Add flags if pinned/mentioned
    const flags = bubble.querySelector(".chat-bubble-flags");
      if (data.pinned) {
        const pin = document.createElement("span");
        pin.classList.add("pin-flag");
        pin.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#f703d7ff" class="bi bi-pin-angle-fill" viewBox="0 0 16 16">
            <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a6 6 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182c-.195.195-1.219.902-1.414.707s.512-1.22.707-1.414l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a6 6 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146"/>
          </svg>`;
        flags.appendChild(pin);
      }
      if (data.mentions && data.mentions.some(m => parseInt(m.id) === CURRENT_USER_ID)) {
        const flag = document.createElement("span");
        flag.classList.add("mention-flag");
        flag.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" 
              fill="none" stroke="currentColor" stroke-width="2" 
              stroke-linecap="round" stroke-linejoin="round" 
              class="icon icon-tabler icons-tabler-outline icon-tabler-at bounce-flag" style="width:14px; height:14px;">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" />
            <path d="M16 12v1.5a2.5 2.5 0 0 0 5 0v-1.5a9 9 0 1 0 -5.5 8.28" />
          </svg>`;
        flags.appendChild(flag);
      }

    // Set message text and preserve newlines
    //const msgDiv = bubble.querySelector(".fs-3");
    //msgDiv.style.whiteSpace = "pre-wrap"; // preserves \n
    //msgDiv.textContent = data.message;

    // 🔥 Update last message preview in user list (left column)
    const lastMsgEl = document.getElementById(`last-message-${data.sender_id}`);
    if (lastMsgEl) {
      let preview = data.message && data.message.trim() ? data.message : "(Attachment)";
      if (preview.length > 28) preview = preview.slice(0, 28) + "…";
      lastMsgEl.textContent = preview;
    }


    // ---------- selection handlers ----------
    const chatBubbleEl = bubble.querySelector(".chat-bubble");

    // Desktop: right-click opens selection/option panel
    if (!isTouch) {
      chatBubbleEl.addEventListener("contextmenu", (ev) => {
        ev.preventDefault();
        toggleBubbleSelection(chatBubbleEl, data.id);
      });
      // left-click toggles selection if options are open (so user can multi-select easily)
      chatBubbleEl.addEventListener("click", (ev) => {
        if (selectedBubbles.size > 0) {
          ev.preventDefault();
          toggleBubbleSelection(chatBubbleEl, data.id);
        }
      });
    }

    // Mobile: long-press opens selection/option panel (500ms)
    if (isTouch) {
      let pressTimer;
      chatBubbleEl.addEventListener("touchstart", (ev) => {
        ev.preventDefault();     // prevent default touch highlighting
        ev.stopPropagation();
        pressTimer = setTimeout(() => toggleBubbleSelection(chatBubbleEl, data.id), 500);
      }, { passive: false });

      ["touchend","touchmove","touchcancel"].forEach(e => {
        chatBubbleEl.addEventListener(e, (ev) => {
          clearTimeout(pressTimer);
          ev.preventDefault();   // stop native text-selection/copy popup
          ev.stopPropagation();
        }, { passive: false });
      });
      // swipe to reply (left/right) - preserved
      let touchStartX = 0, touchEndX = 0;
      chatBubbleEl.addEventListener("touchstart", (e)=> touchStartX = e.changedTouches[0].screenX);
      chatBubbleEl.addEventListener("touchend", (e)=> {
        touchEndX = e.changedTouches[0].screenX;
        const deltaX = touchEndX - touchStartX;

        // Only trigger on right swipe (deltaX > 50)
        if (deltaX > 50) {
          // trigger reply preview for single bubble
          replyToId = data.id;
          replyPreview.classList.remove("d-none");
          replyPreviewText.innerHTML = `<small>
            ${data.sender_id === CURRENT_USER_ID ? "You" : `${data.sender_title || ""} ${data.sender_name}`}
          </small><br> 
          <span class="reply-preview-text text-secondary">${data.message || ""}</span>`;

          if (data.guest) {
            replyPreviewText.innerHTML += `
              <div class="d-flex align-items-center mt-1">
                ${
                  data.guest.image
                    ? `<img src="${data.guest.image}" style="width:35px;height:35px;border-radius:4px;object-fit:cover;" />`
                    : `<span class="avatar bg-gray d-flex align-items-center justify-content-center" 
                          style="width:35px;height:35px;border-radius:4px;">${data.guest.name[0]}</span>`
                }
                <span class="ms-2 text-warning">${data.guest.title} ${data.guest.name}</span>
              </div>`;
          }
          chatInput.focus();
          adjustPreviewPositions();
        }
      });
    }

    // ========== Click reply preview inside bubble -> scroll & highlight ==========
    bubble.querySelectorAll(".chat-reply-preview").forEach(el => {
      el.addEventListener("click", () => {
        const parentEl = document.getElementById(`chat-bubble-${el.dataset.parentId}`);
        if (parentEl) {
          parentEl.scrollIntoView({ behavior: "smooth", block: "center" });
          
          // ✅ apply highlight directly to bubble div
          const bubbleEl = parentEl.querySelector(".chat-bubble");
          if (bubbleEl) {
            bubbleEl.classList.add("highlight-chat-bubble");
            setTimeout(() => bubbleEl.classList.remove("highlight-chat-bubble"), 5000);
          }
        }
      });
    });

    if (cancelReply) {
      cancelReply.addEventListener("click", () => {
        replyToId = null;
        replyPreview.classList.add("d-none");
        adjustPreviewPositions();
        replyPreviewText.innerHTML = ""; // clear text
      });
    }
    return bubble;
  }

  // ---------- Prepend older messages ----------
  function prependMessages(messages) {
    const prevScrollHeight = chatContainer.scrollHeight;
    const prevScrollTop = chatContainer.scrollTop;

    // ✅ Keep backend order (oldest → newest)
    messages.forEach(msg => {
      // Skip duplicates silently
      if (!document.getElementById(`chat-bubble-${msg.id}`)) {
        chatContainer.prepend(renderMessage(msg, true));
      }
    });

    // ✅ Restore scroll position after prepend
    chatContainer.scrollTop = chatContainer.scrollHeight - prevScrollHeight + prevScrollTop;

    // ✅ Rebuild separators cleanly
    normalizeDateSeparators();
    updateStickyHeader();
  }

  // ---------- Normalize date separators ----------
  // --- normalizeDateSeparators (fixed to use safeParseDate) ---
  function normalizeDateSeparators() {
    chatContainer.querySelectorAll(".chat-date-separator").forEach(el => el.remove());

    let lastDay = null;
    const messages = [...chatContainer.querySelectorAll(".chat-item")]
      .sort((a, b) => {
        const da = safeParseDate(a.dataset.createdAt);
        const db = safeParseDate(b.dataset.createdAt);
        return da - db;
      });

    // ✅ Clear container and rebuild in order
    messages.forEach(msg => chatContainer.appendChild(msg));

    messages.forEach(msg => {
      const createdAt = msg.dataset.createdAt;
      if (!createdAt) return;
      const msgDateObj = safeParseDate(createdAt);
      if (!msgDateObj) return;

      const msgDay = new Date(msgDateObj.getFullYear(), msgDateObj.getMonth(), msgDateObj.getDate());

      if (!lastDay || msgDay.getTime() !== lastDay.getTime()) {
        lastDay = msgDay;

        const separator = document.createElement("div");
        separator.classList.add("chat-date-separator", "mb-2");
        Object.assign(separator.style, {
          display: "inline-block",
          padding: "2px 12px",
          borderRadius: "20px",
          fontWeight: "500",
          fontSize: "0.8rem",
          color: "#f59f00",
          backgroundColor: "#1f2937",
          boxShadow: "0 4px 8px #000000d2",
          textAlign: "center",
          margin: "auto"
        });
        separator.textContent = getDateText(msgDay);

        chatContainer.insertBefore(separator, msg);
      }
    });
  }

  function updateStickyHeader() {
    const separators = Array.from(chatContainer.querySelectorAll(".chat-date-separator"));
    let headerText = "";
    const containerRect = chatContainer.getBoundingClientRect();

    for (let i = 0; i < separators.length; i++) {
      const sep = separators[i];
      const rect = sep.getBoundingClientRect();

      if (rect.top <= containerRect.top + 10) {
        headerText = sep.textContent;
      }
    }

    if (headerText) {
      stickyDateHeader.textContent = headerText;
      stickyDateHeader.style.opacity = "1";
      stickyDateHeader.style.transform = "translate(-50%, 0)";
    } else {
      stickyDateHeader.style.opacity = "0";
    }
  }
  chatContainer.addEventListener("scroll", updateStickyHeader);


  // ---------- Load more ----------
  async function loadMoreMessages() {
    if (loading) return;
    loading = true;
    let url = `load/?limit=${limit}`;
    if (oldestLoaded) url += `&before=${encodeURIComponent(oldestLoaded)}`;

    try {
      const res = await fetch(url);
      const data = await res.json();

      if (data.messages.length) {
        prependMessages(data.messages);

        // ✅ first element is now the oldest
        oldestLoaded = data.messages[0].created_at;
      }
    } catch (err) {
      console.error(err);
    }

    loading = false;
  }

  // ---------- Append new live message ----------
  function appendMessage(data, isPrepend = false) {
    // 🔹 Ensure assigned_user is included for rendering immediately
    if (data.guest) {
      const latestGuest = USER_GUESTS.find(g => g.id === data.guest.id) || UNASSIGNED_GUESTS.find(g => g.id === data.guest.id);
      data.guest.assigned_user = latestGuest?.assigned_user || data.guest.assigned_user || null;
    }

    //if (data.type === "pin") {
    //  updatePinnedPreview(data); // your preview logic
    //  return;
    //}

    //if (data.type === "unpin") {
    //  removePinnedPreview(data.message_id);
    //  return;
    //}

    if (!data.message && data.type !== 'chat_message') {
      console.warn("Skipping non-message payload:", data);
      return;
    }

    if (document.getElementById(`chat-bubble-${data.id}`)) return console.warn("Duplicate skipped (append):", data.id);

    const bubble = renderMessage(data);
    if (isPrepend) chatContainer.insertBefore(bubble, chatContainer.firstChild); else chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    normalizeDateSeparators();
    updateStickyHeader();
  }

  // ---------- Infinite scroll ----------
  chatContainer.addEventListener("scroll", () => {
    if (chatContainer.scrollTop === 0 && !loading) loadMoreMessages();
  });

  // ---------- Initial load ----------
  loadMoreMessages();


  LAST_MESSAGES.forEach(appendMessage);

  /***********************
  * Mentions Utilities *
  ***********************/

  // Utility to safely escape regex special chars
  function escapeRegex(string) {
    if (!string) return "";
    return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  // Detect manually typed mentions in message text
  function detectMentionsFromText(text) {
    if (!text) return [];
    const detected = [];

    usersList.forEach(u => {
      const fullName = escapeRegex(u.full_name || u.username);
      const title = u.title ? escapeRegex(u.title) : "";

      // If title exists, allow optional "Title " before the name
      const pattern = title
        ? `@(?:${title}\\s+)?${fullName}`
        : `@${fullName}`;

      const regex = new RegExp(pattern, "i"); // case-insensitive
      if (regex.test(text) && !mentions.some(m => m.id == u.id)) {
        detected.push({ id: u.id, title: u.title, name: u.full_name });
      }
    });

    return detected;
  }

  // Render mentions in message with styled spans
  function renderMessageWithMentions(message, mentionsList) {
    if (!mentionsList || !mentionsList.length) return message;

    let renderedMsg = message;

    mentionsList.forEach(m => {
      const titlePrefix = m.title ? m.title + " " : "";
      const name = m.name || m.fullname; // fallback

      const regex = new RegExp(
        `@${escapeRegex(titlePrefix + name)}`,
        "gi"
      );

      const mentionColor = m.color || "#00aeffff";

      renderedMsg = renderedMsg.replace(
        regex,
        `<span class="mention" style="color:${mentionColor}">@${titlePrefix}${name}</span>`
      );
    });

    return renderedMsg;
  }

  async function sendMessage(message = "", guest = selectedGuest) {
    // Always pull latest text if not explicitly passed
    if (!message) {
      message = getInputText();
    }

    // ✅ Safeguard: block empty or whitespace-only messages
    if (!message || !message.trim()) {
      if (!guest && !replyToId && !selectedFile && !selectedLinkPreview) {
        console.warn("sendMessage exited: nothing to send");
        return;
      }
    }

    if (!chatSocket || chatSocket.readyState !== WebSocket.OPEN) {
      console.warn("sendMessage exited: WebSocket not open", chatSocket?.readyState);
      return;
    }

    // 🔹 Ensure assigned_user is included
    if (guest) {
      // Use already assigned user if present
      if (!guest.assigned_user) {
        const latestGuest = USER_GUESTS.find(g => g.id === guest.id) || UNASSIGNED_GUESTS.find(g => g.id === guest.id);
        guest.assigned_user = latestGuest?.assigned_user || null;
      }
    }

    // Detect manually typed mentions
    const manualMentions = detectMentionsFromText(message).map(m => {
      const user = USERS.find(u => u.id === m.id); // get the full user object
      return {
        ...m,
        color: user?.color || "#00aeffff" // assign their chat bubble color
      };
    });

    // Push to mentions array
    manualMentions.forEach(m => mentions.push(m));

    // Edit mode
    //if (chatInput.dataset.editingId) {
    //  const editId = parseInt(chatInput.dataset.editingId, 10);
    //  const node = document.getElementById(`chat-bubble-${editId}`);
    //  if (node) {
    //    node.dataset.edited = "true";
    //    const body = node.querySelector(".chat-bubble-body .fs-4");
    //    if (body) body.textContent = message.trim();

    //    let editedTag = node.querySelector(".edited-flag");
    //    if (!editedTag) {
    //      const dateEl = node.querySelector(".chat-bubble-date");
    //      if (dateEl) {
    //        editedTag = document.createElement("span");
    //        editedTag.className = "edited-flag text-muted ms-1";
    //        editedTag.style.fontSize = "0.7rem";
    //        editedTag.textContent = "(Edited)";
    //        dateEl.appendChild(editedTag);
    //      }
    //    }
    //  }

    //  chatSocket.send(JSON.stringify({
    //    action: "edit",
    //    message_id: editId,
    //    new_text: message.trim(),
    //    sender_id: CURRENT_USER_ID
    //  }));

    //  chatInput.value = "";
    //  delete chatInput.dataset.editingId;
    //  return;
    //}

    const payload = {
      sender_id: CURRENT_USER_ID,
      guest_id: guest ? parseInt(guest.id, 10) : null,
      reply_to_id: replyToId || null,
      mentions: mentions.map(m => m.id),
      guest: guest
      ? {
          id: parseInt(guest.id, 10),
          name: guest.name,
          custom_id: guest.custom_id,
          image: guest.image,
          title: guest.title,
          date_of_visit: guest.date_of_visit,
          assigned_user: guest.assigned_user || null
        }
      : null
    };

    // Only include message if it’s non-empty
    if (message && message.trim()) {
      payload.message = message.trim();
    }

    //if (guest) {
    //  payload.guest = {
    //    id: parseInt(guest.id, 10),
    //    name: guest.name,
    //    custom_id: guest.custom_id,
    //    image: guest.image,
    //    title: guest.title,
    //    date_of_visit: guest.date_of_visit,
        //assigned_user: guest.assigned_user || null
    //  };
    //}

    // File Send Payload
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
        const res = await fetch("/accounts/upload_file/", {
          method: "POST",
          body: formData
        });

        if (!res.ok) throw new Error("File upload failed");
        const uploaded = await res.json();

        // ✅ Pass whole metadata to WS
        payload.file = uploaded;
        selectedFile = null;
      } catch (err) {
        console.error("❌ File upload error:", err);
        return; // abort sending
      }
    }

    if (selectedLinkPreview) {
      payload.link_preview = selectedLinkPreview;
    }

    // 🔥 Log guest info reliably
    console.group("📝 Sending message");
    console.log("Guest object:", guest);
    console.log("Assigned user:", guest?.assigned_user);
    console.log("Message content:", message.trim());
    console.log("Final payload:", JSON.stringify(payload, null, 2)); // ✅ full JSON preview
    console.groupEnd();

    chatSocket.send(JSON.stringify(payload));

    // Cleanup
    clearInput();
    autoResizeContenteditable(chatInput);
    removeGuestPreview();
    replyToId = null;
    replyPreview.classList.add("d-none");
    removeFilePreview();
    removeLinkPreview();
    //window.clearMentions();
    mentions = [];
  }



/***********************
 * Input + Send Control
 ***********************/

// Handle typing in textarea
chatInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && e.shiftKey) {
    // Shift+Enter → Send
    e.preventDefault(); // stop newline
    sendMessage(chatInput.value);
  } else if (e.key === "Enter") {
    // Enter → newline (default), so do nothing special
    // but we auto-resize the textarea
    setTimeout(() => {
      chatInput.style.height = "auto";
      chatInput.style.height = chatInput.scrollHeight + "px";
    }, 0);
  }
});

// Handle Send button click
sendButton.addEventListener("click", e => {
  e.preventDefault();
  sendMessage(chatInput.value);
});


function applyMarkdownInline(el) {
    const caretOffset = saveCaretPosition(el);
    let html = el.innerHTML;

    // --- Highlight === like before
    html = html.replace(/==([^=]+)==/g, (match, p1) => {
      if (/<mark>.*<\/mark>/.test(p1)) return match;
      return `==<mark>${p1}</mark>==`;
    });

    // --- Bold: **text**
    html = html.replace(/\*\*([^*]+)\*\*/g, (match, p1) => {
      if (/^\*\*<strong>.*<\/strong>\*\*$/.test(match)) return match;
      return `**<strong>${p1}</strong>**`;
    });

    // --- Italic: *text*
    html = html.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, (match, p1) => {
      if (/^\*<em>.*<\/em>\*$/.test(match)) return match;
      return `${p1}*<em>${p2}</em>*`;
    });

    // --- Underline: _text_
    html = html.replace(/_([^_]+)_/g, (match, p1) => {
      if (/^_<u>.*<\/u>_$/.test(match)) return match;
      return `_<u>${p1}</u>_`;
    });

    if (el.innerHTML !== html) {
      el.innerHTML = html;
      restoreCaretPosition(el, caretOffset);
    }
  }



// Nested combos
    html = html.replace(/\*\*_(.+?)_\*\*/g, "**_<strong><u>$1</u></strong>_**");
    html = html.replace(/_==(.+?)==_/g, "_==<u><mark>$1</mark></u>==_");





function autoResizeTextarea(el) {
    el.style.height = "auto"; // reset so scrollHeight is accurate

    const lineHeight = 20; // adjust to match your textarea CSS line-height
    const minHeight = lineHeight * 2;  // ~2 lines minimum
    const maxHeight = lineHeight * 5;  // ~5 lines maximum

    const newHeight = Math.min(el.scrollHeight, maxHeight);

    el.style.height = newHeight + "px";

    // Enable vertical scrollbar only if content exceeds maxHeight
    el.style.overflowY = el.scrollHeight > maxHeight ? "auto" : "hidden";
  }

  // Resize on input
  chatInput.addEventListener("input", () => autoResizeTextarea(chatInput));

  // Make Enter = newline only
  const TAB_SPACES = "    "; // 4-space "tab" (change if you want a different width)

  chatInput.addEventListener("keydown", (e) => {
    const selStart = chatInput.selectionStart;
    const selEnd = chatInput.selectionEnd;

    // 1) SPACE after typing "1." (space not yet inserted on keydown)
    if (e.key === " " && !e.shiftKey && selStart === selEnd) {
      const before = chatInput.value.substring(0, selStart);
      const lastNewline = before.lastIndexOf("\n");
      const currentLine = before.substring(lastNewline + 1);

      // if line ends with digits + dot (no trailing space yet), e.g. "1."
      if (/^\s*\d+\.$/.test(currentLine)) {
        e.preventDefault();

        const after = chatInput.value.substring(selStart);

        // Build the new line: tab spaces + "<number>. "
        const newLine = TAB_SPACES + currentLine + " ";

        // Reconstruct value and position caret after the inserted space
        chatInput.value =
          chatInput.value.substring(0, lastNewline + 1) + newLine + after;

        const newPos = (lastNewline + 1) + newLine.length;
        chatInput.selectionStart = chatInput.selectionEnd = newPos;

        autoResizeTextarea(chatInput);
        return;
      }
    }

    // 2) ENTER: continue auto-numbering (unchanged behavior)
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

      const before = chatInput.value.substring(0, selStart);
      const after = chatInput.value.substring(selEnd);

      const lastNewline = before.lastIndexOf("\n");
      const currentLine = before.substring(lastNewline + 1);

      let newText = "\n";

      // Capture existing indent and number (indent may include TAB_SPACES now)
      const match = currentLine.match(/^(\s*)(\d+)\.\s/);
      if (match) {
        const indent = match[1];
        const number = parseInt(match[2], 10);
        newText += indent + (number + 1) + ". ";
      }

      chatInput.value = before + newText + after;
      const pos = before.length + newText.length;
      chatInput.selectionStart = chatInput.selectionEnd = pos;

      autoResizeTextarea(chatInput);
      return;
    }
  });

  // Send only with Send button
  sendButton.addEventListener("click", (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (text) {
      sendMessage(text);
      chatInput.value = ""; // clear input
      autoResizeTextarea(chatInput); // reset height
    }
  });

  // Initial height set
  autoResizeTextarea(chatInput);



<!-- Textarea -->
                    <textarea class="form-control border-0 flex-grow-1" id="chatInput" 
                              placeholder="Type Message" rows="1"
                              style="resize: none; overflow: hidden; background: transparent;"></textarea>



function autoResizeTextarea(el) {
    el.style.height = "auto"; // reset so scrollHeight is accurate

    const lineHeight = 20; // adjust to match your textarea CSS line-height
    const minHeight = lineHeight * 2;  // ~2 lines minimum
    const maxHeight = lineHeight * 5;  // ~5 lines maximum

    const newHeight = Math.min(el.scrollHeight, maxHeight);

    el.style.height = newHeight + "px";

    // Enable vertical scrollbar only if content exceeds maxHeight
    el.style.overflowY = el.scrollHeight > maxHeight ? "auto" : "hidden";
  }

  // Resize on input
  chatInput.addEventListener("input", () => autoResizeTextarea(chatInput));






if (data.action === "pin_update" || data.action === "pin") {
        (data.pins || []).forEach(p => {
          const id = p.id || p.message_id || p;
          if (p.pinned) {
            // if full message present, add to preview stack
            if (p.message) {
              addPinnedMessage(p);
            } else {
              // just toggle flag on bubble if present
              const node = document.getElementById(`chat-bubble-${id}`);
              if (node && !node.querySelector('.pin-flag')) {
                const flags = node.querySelector('.chat-bubble-flags');
                const pin = document.createElement('span');
                pin.classList.add('pin-flag');
                pin.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin-angle-fill" viewBox="0 0 16 16">
                  <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a6 6 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182c-.195.195-1.219.902-1.414.707s.512-1.22.707-1.414l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a6 6 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0 .43-.108 1.022-.589 1.503a.5.5 0 0 1-.354.146"/>
                </svg>`;
                flags.appendChild(pin);
              }
            }
          } else {
            removePinnedMessage(id);
            const node = document.getElementById(`chat-bubble-${id}`);
            const el = node?.querySelector('.pin-flag');
            if (el) el.remove();
          }
        });
        return;
      }





<div class="page-wrapper">
  <!-- BEGIN PAGE HEADER -->
  <div class="page-header d-print-none" aria-label="Page header">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <!-- Dynamic Page Title -->
          <kbd class="bg-indigo-lt"><h2 class="page-title">{{ page_title }}</h2></kbd>
        </div>
      </div>
    </div>
  </div>
  <!-- END PAGE HEADER -->

  <div class="page-body">
    <div class="container-xl flex-fill d-flex flex-column">
      <div class="card flex-fill">
        <div class="row g-0 flex-fill chat-layout">
          <!-- LEFT COLUMN -->
          <div class="col-12 col-lg-5 col-xl-3 border-end d-flex flex-column chat-users">
            <div class="card-header mb-2 chat-top-header justify-content-center align-items-center border-0">
              <!-- Back button (mobile only) -->
              <button id="chatBackBtn" class="btn btn-link p-0 me-2 d-lg-none" style="color:white;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
                    viewBox="0 0 24 24" fill="none" stroke="currentColor" 
                    stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="icon icon-tabler icon-tabler-arrow-left">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M5 12h14" />
                  <path d="M5 12l6 6" />
                  <path d="M5 12l6 -6" />
                </svg>
              </button>
              <!-- Avatar -->
              <span class="avatar avatar-lg bg-purple-lt d-flex align-items-center justify-content-center" style="width:40px; height:40px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-armchair">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M5 11a2 2 0 0 1 2 2v2h10v-2a2 2 0 1 1 4 0v4a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-4a2 2 0 0 1 2 -2z" />
                  <path d="M5 11v-5a3 3 0 0 1 3 -3h8a3 3 0 0 1 3 3v5" />
                  <path d="M6 19v2" /><path d="M18 19v2" />
                </svg>
              </span>

              <!-- Text -->
              <kbd class="ms-2 bg-warning-lt"><h5>A People <em>Helped</em> By God!</h5></kbd>
            </div>
            <div class="card-body p-0 mt-0 mb-3 scrollable flex-fill" style="height: 500px; overflow-y: auto;">
              <div class="row g-2 flex-nowrap">
                {% for user in users %}
                  <div class="col-12 user-card">
                    <div class="card shadow-sm ms-2 me-2 border-0 {{ user.color }}">
                      <div class="card-body py-2 px-3 d-flex align-items-center">
                        <!-- Avatar -->
                        <div class="me-3">
                          <a href="tel:{{ user.phone_number }}">
                            {% if user.image %}
                              <span class="avatar rounded"
                                    style="background-image:url('{{ user.image }}');
                                          width:40px; height:40px;
                                          background-size:cover;
                                          background-position:center;">
                              </span>
                            {% else %}
                              <span class="avatar d-flex align-items-center justify-content-center rounded text-white fw-bold"
                                    style="width:40px; height:40px; font-size:0.9rem;">
                                {{ user.initials }}
                              </span>
                            {% endif %}
                          </a>
                        </div>
                        <!-- Name + Last Message -->
                        <div class="flex-grow-1">
                          <div class="fw-bold text-truncate" style="color: var(--tblr-{{ user.color }});">
                            {{ user.title|default:"" }} {{ user.full_name }}
                          </div>
                          <div id="last-message-{{ user.id }}"
                                class="text-secondary fst-italic text-truncate" 
                                style="font-size:0.65rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {{ user.last_message|default:"No messages yet"|truncatechars:30 }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                {% endfor %}
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN -->
          <div class="col-12 col-lg-7 col-xl-9 d-flex flex-column">
            <div class="card-header justify-content-center border-0">
              <div class="input-icon">
                <span class="input-icon-addon">
                  <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-user-search">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                    <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" /><path d="M6 21v-2a4 4 0 0 1 4 -4h1.5" />
                    <path d="M18 18m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" /><path d="M20.2 20.2l1.8 1.8" />
                  </svg>
                </span>
                <input type="text" id="chatSearch" class="form-control" 
                      placeholder="Search Chat" aria-label="Search">
              </div>
            </div>
            <div class="card-body mt-0 p-0 d-flex flex-column flex-fill">
              <!-- Chat Container -->
              <div class="chat-bubbles text-start ps-3 pe-2" id="chatMessagesContainer" style="overflow-y:auto; height:500px; position:relative; overflow-x:hidden;">
                <!-- Messages will be dynamically loaded here -->
              </div>
              <!-- Options Panel -->
              <div id="chatOptionsPanel" class="options-panel hidden" aria-hidden="true">
                <button id="replyBtn" title="Reply">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ff5e01ff" class="bi bi-reply-all-fill" viewBox="0 0 16 16">
                    <path d="M8.021 11.9 3.453 8.62a.72.72 0 0 1 0-1.238L8.021 4.1a.716.716 0 0 1 1.079.619V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z"/>
                    <path d="M5.232 4.293a.5.5 0 0 1-.106.7L1.114 7.945l-.042.028a.147.147 0 0 0 0 .252l.042.028 4.012 2.954a.5.5 0 1 1-.593.805L.539 9.073a1.147 1.147 0 0 1 0-1.946l3.994-2.94a.5.5 0 0 1 .699.106"/>
                  </svg>
                </button>
                <!--<button id="editBtn" title="Edit">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                    <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
                  </svg>
                </button>-->
                <button id="copyBtn" title="Copy">
                  <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="#02bd12ff"  class="icon icon-tabler icons-tabler-filled icon-tabler-copy-check">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                    <path d="M18.333 6a3.667 3.667 0 0 1 3.667 3.667v8.666a3.667 3.667 0 0 1 -3.667 3.667h-8.666a3.667 3.667 0 0 1 -3.667 -3.667v-8.666a3.667 3.667 0 0 1 3.667 -3.667zm-3.333 -4c1.094 0 1.828 .533 2.374 1.514a1 1 0 1 1 -1.748 .972c-.221 -.398 -.342 -.486 -.626 -.486h-10c-.548 0 -1 .452 -1 1v9.998c0 .32 .154 .618 .407 .805l.1 .065a1 1 0 1 1 -.99 1.738a3 3 0 0 1 -1.517 -2.606v-10c0 -1.652 1.348 -3 3 -3zm1.293 9.293l-3.293 3.292l-1.293 -1.292a1 1 0 0 0 -1.414 1.414l2 2a1 1 0 0 0 1.414 0l4 -4a1 1 0 0 0 -1.414 -1.414" />
                  </svg>
                </button>
                <button id="pinBtn" title="Pin">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#f703d7ff" class="bi bi-pin-angle-fill" viewBox="0 0 16 16">
                    <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a6 6 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182c-.195.195-1.219.902-1.414.707s.512-1.22.707-1.414l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a6 6 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146"/>
                  </svg>
                </button>
                <!--
                <button id="deleteBtn" title="Delete">
                  <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-trash">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 7l16 0" />
                    <path d="M10 11l0 6" /><path d="M14 11l0 6" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
                    <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
                  </svg>
                </button>
                -->
              </div>
              <!-- Sticky Date Header -->
              <div id="stickyDateHeader"></div>

              <!--<div id="scrollToBottomBtn" class="scroll-to-bottom" title="Scroll to bottom">⬇️</div>-->
              <!-- Floating scroll-to-bottom -->
              <div id="scrollToBottomBtn" class="scroll-to-bottom hidden" title="Scroll to bottom">
                <svg  xmlns="http://www.w3.org/2000/svg"  width="48"  height="48"  viewBox="0 0 24 24"  fill="currentColor"  class="icon icon-tabler icons-tabler-filled icon-tabler-square-rounded-arrow-down">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M12 2c-.218 0 -.432 .002 -.642 .005l-.616 .017l-.299 .013l-.579 .034l-.553 .046c-4.785 .464 -6.732 2.411 -7.196 7.196l-.046 .553l-.034 .579c-.005 .098 -.01 .198 -.013 .299l-.017 .616l-.004 .318l-.001 .324c0 .218 .002 .432 .005 .642l.017 .616l.013 .299l.034 .579l.046 .553c.464 4.785 2.411 6.732 7.196 7.196l.553 .046l.579 .034c.098 .005 .198 .01 .299 .013l.616 .017l.642 .005l.642 -.005l.616 -.017l.299 -.013l.579 -.034l.553 -.046c4.785 -.464 6.732 -2.411 7.196 -7.196l.046 -.553l.034 -.579c.005 -.098 .01 -.198 .013 -.299l.017 -.616l.005 -.642l-.005 -.642l-.017 -.616l-.013 -.299l-.034 -.579l-.046 -.553c-.464 -4.785 -2.411 -6.732 -7.196 -7.196l-.553 -.046l-.579 -.034a28.058 28.058 0 0 0 -.299 -.013l-.616 -.017l-.318 -.004l-.324 -.001zm0 5a1 1 0 0 1 .993 .883l.007 .117v5.585l2.293 -2.292a1 1 0 0 1 1.32 -.083l.094 .083a1 1 0 0 1 .083 1.32l-.083 .094l-4 4a1.008 1.008 0 0 1 -.112 .097l-.11 .071l-.114 .054l-.105 .035l-.149 .03l-.117 .006l-.075 -.003l-.126 -.017l-.111 -.03l-.111 -.044l-.098 -.052l-.092 -.064l-.094 -.083l-4 -4a1 1 0 0 1 1.32 -1.497l.094 .083l2.293 2.292v-5.585a1 1 0 0 1 1 -1z" fill="currentColor" stroke-width="0" />
                </svg>
              </div>
            </div>

            {% if not request.user|has_group:"Demo" or request.user.is_superuser %} 
              <!-- Message Input --> 
              <div class="card-footer border-0 position-relative"> 
                
                <div class="input-group input-group-flat rounded-2 border-0 d-flex flex-column p-2"
                    style="box-shadow: 0 4px 8px #000000d2; border-radius: 24px; background: #111827;">

                  <!-- Reply Preview (inline above textarea) -->
                  <div id="replyPreview" 
                      class="d-none d-flex reply-preview text-white p-2 mb-1 rounded-2 justify-content-between align-items-center"
                      style="border-left: 4px solid #018f14ff; background-color: #25292634; font-style: normal; box-shadow: 0 4px 8px #0000004d;">
                    <span id="replyPreviewText"></span>
                    <span id="cancelReply" class="avatar text-red p-0 border-0 d-flex align-items-center justify-content-center"
                          style="flex:0 0 auto; cursor:pointer;">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                      </svg>
                    </span>
                  </div>

                  <!-- Guest Preview (injected dynamically) -->
                  <div id="guestPreviewContainer"></div>

                  <!-- Input Row (always at bottom of stack) -->
                  <div class="d-flex align-items-end justify-content-center w-100">
                    <!-- Attachment Button -->
                    <a href="#" class="link-secondary dropdown p-2 text-purple d-flex align-items-center justify-content-center" 
                      id="openUserGuestPopup" style="flex: 0 0 auto;">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                          class="icon icon-tabler icons-tabler-outline icon-tabler-user-up"> 
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" /> 
                        <path d="M6 21v-2a4 4 0 0 1 4 -4h4" />
                        <path d="M19 22v-6" />
                        <path d="M22 19l-3 -3l-3 3" /> 
                      </svg> 
                    </a>

                    <!-- Textarea -->
                    <textarea class="form-control border-0 flex-grow-1" id="chatInput" 
                              placeholder="Type Message" rows="1"
                              style="resize: none; overflow: hidden; background: transparent;"></textarea>

                    <!-- Send Button -->
                    <a href="#" id="sendButton" class="link-secondary p-2 text-green d-flex align-items-center justify-content-center"
                      style="flex: 0 0 auto;"> 
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                          class="icon icon-tabler icons-tabler-outline icon-tabler-send"> 
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M10 14l11 -11" />
                        <path d="M21 3l-6.5 18a.55 .55 0 0 1 -1 0l-3.5 -7l-7 -3.5a.55 .55 0 0 1 0 -1l18 -6.5" /> 
                      </svg> 
                    </a>
                  </div>
                </div>
                <!-- Mention dropdown -->
                <div id="mentionDropdown" class="mention-dropdown d-none"></div> 
              </div> 
            {% endif %}
          </div>

        </div>
      </div>
    </div>
  </div>
</div>




document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chatMessagesContainer");
  const chatForm = document.getElementById("chatReplyForm");
  const chatInput = document.getElementById("chatInput");
  const fileAttachment = document.getElementById("fileAttachment");
  const guestSelect = document.getElementById("guestSelect");
  const searchInput = document.getElementById("chatSearchInput");
  const typingIndicator = document.getElementById("typingIndicator");

  let replyToId = null;
  let selectedGuest = null;
  let userColors = {};
  let usersMap = {};
  let typingTimeout = null;
  const currentUserId = window.chatUserId;

  // ======== WebSocket Setup ========
  const chatSocket = new WebSocket(window.wsUrl);
  chatSocket.onopen = () => console.log("Connected to chat WebSocket");
  chatSocket.onclose = () => console.log("Disconnected from chat WebSocket");
  chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    switch(data.type) {
      case "chat_init":
        initUsers(data.users);
        initMessages(data.messages);
        break;
      case "chat_message":
        appendMessage(data.message, true);
        break;
      case "chat_seen":
        updateSeen(data.message_id, data.user_id);
        break;
      case "typing":
        showTyping(data.user_id);
        break;
      default: console.log("Unknown type:", data.type);
    }
  };

  // ======== INIT ========
  function initUsers(users) {
    users.forEach(u => {
      userColors[u.id] = u.color || "bg-gray-lt text-dark";
      usersMap[u.id] = u;
    });
  }

  function initMessages(messages) {
    messages.forEach(msg => appendMessage(msg));
    scrollToBottom();
  }

  // ======== APPEND MESSAGE ========
  function appendMessage(msg, scroll=false) {
    if (!chatContainer) return;
    const msgDate = new Date(msg.created_at).toDateString();

    // --- Date separator ---
    const lastDateSeparator = chatContainer.querySelector(".date-separator:last-of-type");
    const lastDate = lastDateSeparator?.dataset?.date;
    if (msgDate !== lastDate) {
      const dateSeparator = document.createElement("div");
      dateSeparator.className = "date-separator sticky-top text-center py-1";
      dateSeparator.dataset.date = msgDate;

      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(today.getDate() - 1);

      let label;
      if (msgDate === today.toDateString()) label = "Today";
      else if (msgDate === yesterday.toDateString()) label = "Yesterday";
      else label = new Date(msgDate).toLocaleDateString(undefined, { weekday:'short', month:'short', day:'numeric' });

      dateSeparator.innerHTML = `<span class="badge bg-light shadow-sm">${label}</span>`;
      chatContainer.appendChild(dateSeparator);
    }

    const isCurrentUser = msg.sender.id === currentUserId;
    const wrapper = document.createElement("div");
    wrapper.className = "message-wrapper d-flex mb-2";
    wrapper.style.justifyContent = isCurrentUser ? "flex-end" : "flex-start";
    wrapper.dataset.id = msg.id;
    wrapper.dataset.senderId = msg.sender.id;
    wrapper.dataset.msgDate = msgDate;

    const bubble = document.createElement("div");
    bubble.className = `chat-bubble p-2 rounded`;
    bubble.style.backgroundColor = isCurrentUser ? "#DCF8C6" : "#FFF"; // WhatsApp style colors
    bubble.style.maxWidth = "75%";

    const senderName = (!isCurrentUser || msg.parent_message) ? (isCurrentUser ? "You" : msg.sender.full_name) : "";
    bubble.innerHTML = `
      ${senderName ? `<strong>${senderName}:</strong>` : ""}
      <div class="message-text">${msg.message.replace(/\n/g,"<br>")}</div>
      ${msg.parent_message ? `<div class="reply-preview small text-muted mt-1 p-1 border-start border-2">
        Reply to ${msg.parent_message.sender.id===currentUserId ? "You":msg.parent_message.sender.full_name}: ${msg.parent_message.message.slice(0,30)}
      </div>`:""}
      ${msg.guest_card ? `<div class="guest-card mt-1 p-1 border rounded bg-light">
        Guest: ${msg.guest_card.name} (${msg.guest_card.custom_id})
      </div>`:""}
    `;

    // Seen indicator
    const seenDiv = document.createElement("div");
    seenDiv.className = "seen-indicator mt-1";
    seenDiv.dataset.seenBy = JSON.stringify(msg.seen_by||[]);
    updateSeenIndicator(seenDiv, msg.seen_by||[], msg.sender.id);

    bubble.appendChild(seenDiv);
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);

    if(scroll) scrollToBottom();
  }

  // ======== SEEN ========
  function updateSeenIndicator(seenDiv, seenBy, senderId) {
    if(!seenDiv) return;
    const otherUsers = seenBy.filter(uid=>uid!==senderId);
    if(!otherUsers.length){seenDiv.innerHTML=""; return;}
    const avatars = otherUsers.map(uid=>{
      const u=usersMap[uid];
      if(!u) return "";
      const initials=u.full_name?u.full_name.split(" ").map(n=>n[0].toUpperCase()).slice(0,2).join(""):"?";
      return `<span class="avatar avatar-xs rounded ${userColors[uid]||'bg-gray-lt text-dark'} me-1" title="${u.full_name}" style="width:24px;height:24px;font-size:12px;line-height:24px;text-align:center">${initials}</span>`;
    }).join("");
    seenDiv.innerHTML=`<small class="text-muted">Seen by:</small> ${avatars}`;
  }

  function markSeen(messageId){ chatSocket.send(JSON.stringify({type:"mark_seen", message_id:messageId})); }
  function updateSeen(messageId,userId){
    const wrapper=chatContainer.querySelector(`[data-id="${messageId}"]`);
    if(!wrapper) return;
    const seenDiv=wrapper.querySelector(".seen-indicator");
    let seenBy=JSON.parse(seenDiv.dataset.seenBy||"[]");
    if(!seenBy.includes(userId)){
      seenBy.push(userId);
      seenDiv.dataset.seenBy=JSON.stringify(seenBy);
      updateSeenIndicator(seenDiv,seenBy,parseInt(wrapper.dataset.senderId)||userId);
    }
  }

  // ======== SEND MESSAGE ========
  if(chatForm){
    chatForm.onsubmit=e=>{
      e.preventDefault();
      if(!chatInput.value.trim()&&!replyToId&&!fileAttachment.files[0]&&!selectedGuest) return;
      chatSocket.send(JSON.stringify({
        type:"chat_message",
        message:chatInput.value.trim(),
        parent_id:replyToId,
        guest_id:selectedGuest
      }));
      chatInput.value=""; replyToId=null; selectedGuest=null;
      if(guestSelect) guestSelect.value="";
    };
  }

  // ======== REPLY CLICK ========
  chatContainer.addEventListener("click", e=>{
    const replyBtn=e.target.closest(".reply-btn");
    if(!replyBtn) return;
    replyToId=replyBtn.dataset.messageId;
    chatInput.focus();
  });

  // ======== SEARCH ========
  if(searchInput){
    searchInput.addEventListener("input", ()=>{
      const q=searchInput.value.toLowerCase();
      chatContainer.querySelectorAll(".message-wrapper").forEach(msg=>{
        msg.style.display=msg.textContent.toLowerCase().includes(q)?"":"none";
      });
    });
  }

  // ======== SCROLL & SEEN ========
  function scrollToBottom(){ chatContainer.scrollTop=chatContainer.scrollHeight; }
  chatContainer.addEventListener("scroll",()=>{
    chatContainer.querySelectorAll(".message-wrapper").forEach(msg=>{
      const r=msg.getBoundingClientRect();
      if(r.top<window.innerHeight&&r.bottom>0) markSeen(msg.dataset.id);
    });
  });

  // ======== TYPING ========
  chatInput.addEventListener("input",()=>{
    chatSocket.send(JSON.stringify({type:"typing"}));
    clearTimeout(typingTimeout);
    typingTimeout=setTimeout(()=>{ if(typingIndicator) typingIndicator.innerText=""; },2000);
  });

  function showTyping(userId){
    const u=usersMap[userId];
    if(!u||!typingIndicator) return;
    typingIndicator.innerText=`${u.full_name} is typing...`;
    clearTimeout(typingTimeout);
    typingTimeout=setTimeout(()=>{ typingIndicator.innerText=""; },2000);
  }

  // ======== INITIAL LOAD ========
  if(window.initialUsers) initUsers(window.initialUsers);
  if(window.initialMessages) initMessages(window.initialMessages);
});












const msgDateObj = new Date(data.created_at);
    const msgDay = new Date(msgDateObj.getFullYear(), msgDateObj.getMonth(), msgDateObj.getDate());

    if (!lastMessageDate || msgDay.getTime() !== lastMessageDate.getTime()) {
      lastMessageDate = msgDay;
      const separator = document.createElement("div");
      separator.classList.add("chat-date-separator", "mb-2");
      Object.assign(separator.style, {
        display: "inline-block",
        padding: "2px 12px",
        borderRadius: "20px",
        fontWeight: "500",
        fontSize: "0.8rem",
        color: "#f59f00",
        backgroundColor: "#343531",
        boxShadow: "0 4px 8px rgba(0,0,0,0.4)",
        textAlign: "center",
        margin: "0 auto"
      });
      separator.textContent = getDateText(msgDay);
      chatContainer.appendChild(separator);
    }


// Sticky header setup
  //const stickyDateHeader = document.getElementById("stickyDateHeader");
  Object.assign(stickyDateHeader.style, {
    position: "absolute",
    top: "0px",
    left: "50%",
    transform: "translateX(-50%)",
    display: "inline-flex",
    padding: "4px 12px",
    borderRadius: "20px",
    fontWeight: "600",
    fontSize: "0.9rem",
    color: "#f59f00", // text-yellow-800
    backgroundColor: "#343531", // bg-yellow-lt
    boxShadow: "0 4px 8px rgba(0,0,0,0.4)",
    textAlign: "center",
    justifyContent: "center",
    margin: "0 auto",
    transition: "opacity 0.3s ease, transform 0.3s ease",
    zIndex: 50,
    pointerEvents: "none",
    opacity: "0"
  });

  // Date text formatter
  function getDateText(date) {
    const now = new Date();
    const msgDay = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    if (msgDay.getTime() === today.getTime()) return "Today";
    if (msgDay.getTime() === yesterday.getTime()) return "Yesterday";

    const diffTime = today.getTime() - msgDay.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 7) {
      return msgDay.toLocaleDateString(undefined, { weekday: "long" }); // "Monday"
    }

    return msgDay.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  }

  // Update sticky header
  function updateStickyHeader() {
    const children = Array.from(chatContainer.querySelectorAll(".chat-item"));
    let headerText = "";
    const containerRect = chatContainer.getBoundingClientRect();

    for (let i = 0; i < children.length; i++) {
      const item = children[i];
      const dateEl = item.querySelector(".chat-bubble-date");
      if (!dateEl) continue;

      const date = new Date(dateEl.getAttribute("data-full-date"));
      const rect = item.getBoundingClientRect();

      if (rect.top <= containerRect.top + 10) {
        headerText = getDateText(date);
      }
    }

    if (headerText) {
      stickyDateHeader.textContent = headerText;
      stickyDateHeader.style.opacity = "1";
      stickyDateHeader.style.transform = "translate(-50%, 0)";
    } else {
      stickyDateHeader.style.opacity = "0";
    }
  }
  chatContainer.addEventListener("scroll", updateStickyHeader);