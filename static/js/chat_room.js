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
