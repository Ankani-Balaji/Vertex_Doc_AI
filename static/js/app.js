// app.js
document.addEventListener("DOMContentLoaded", () => {

  /* ---------------------------------------------------------
     Toasts: auto-remove after animation
  --------------------------------------------------------- */
  document.querySelectorAll(".toast").forEach((toast) => {
    setTimeout(() => toast.remove(), 4600);
  });

  /* ---------------------------------------------------------
     Scan / loading overlay on upload submit
  --------------------------------------------------------- */
  const overlay = document.getElementById("loading-spinner");
  const uploadForm = document.getElementById("upload-form");

  if (uploadForm && overlay) {
    uploadForm.addEventListener("submit", () => {
      overlay.style.display = "flex";
    });
  }

  /* ---------------------------------------------------------
     Drag & drop upload zone
  --------------------------------------------------------- */
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("pdf_file");
  const dzTitle = document.getElementById("dropzone-title");
  const dzSub = document.getElementById("dropzone-sub");

  if (dropzone && fileInput) {
    ["dragenter", "dragover"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.add("drag-active");
      });
    });

    ["dragleave", "drop"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.remove("drag-active");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length) {
        fileInput.files = files;
        updateDropzoneLabel(files[0]);
      }
    });

    fileInput.addEventListener("change", () => {
      if (fileInput.files && fileInput.files.length) {
        updateDropzoneLabel(fileInput.files[0]);
      }
    });

    function updateDropzoneLabel(file) {
      if (dzTitle) dzTitle.textContent = file.name;
      if (dzSub) dzSub.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB · ready to analyze`;
    }
  }

  /* ---------------------------------------------------------
     Mobile sidebar toggle
  --------------------------------------------------------- */
  const sidebar = document.getElementById("sidebar");
  const scrim = document.getElementById("sidebar-scrim");
  const openBtn = document.getElementById("sidebar-open");
  const closeBtn = document.getElementById("sidebar-close");

  function openSidebar() {
    sidebar && sidebar.classList.add("is-open");
    scrim && scrim.classList.add("is-open");
  }
  function closeSidebar() {
    sidebar && sidebar.classList.remove("is-open");
    scrim && scrim.classList.remove("is-open");
  }

  openBtn && openBtn.addEventListener("click", openSidebar);
  closeBtn && closeBtn.addEventListener("click", closeSidebar);
  scrim && scrim.addEventListener("click", closeSidebar);

  /* ---------------------------------------------------------
     Chat: AJAX submit, typing indicator, typewriter reveal
  --------------------------------------------------------- */
  const chatThread = document.getElementById("chat-thread");
  const askForm = document.getElementById("ask-form");
  const questionInput = document.getElementById("question-input");
  const sendBtn = document.getElementById("composer-send");
  const mainScroll = document.getElementById("main-scroll");

  function scrollToBottom() {
    if (mainScroll) mainScroll.scrollTop = mainScroll.scrollHeight;
  }

  function clearEmptyState() {
    const empty = chatThread && chatThread.querySelector(".chat-empty");
    if (empty) empty.remove();
  }

  function appendUserBubble(text) {
    if (!chatThread) return;
    clearEmptyState();
    const row = document.createElement("div");
    row.className = "bubble-row bubble-user";
    row.innerHTML = `<div class="bubble"></div>`;
    row.querySelector(".bubble").textContent = text;
    chatThread.appendChild(row);
    scrollToBottom();
  }

  function appendTypingBubble() {
    if (!chatThread) return null;
    const row = document.createElement("div");
    row.className = "bubble-row bubble-ai";
    row.innerHTML = `
      <span class="ai-avatar">VD</span>
      <div class="bubble is-typing">
        <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
      </div>`;
    chatThread.appendChild(row);
    scrollToBottom();
    return row;
  }

  function revealAnswer(bubbleEl, text) {
    bubbleEl.classList.remove("is-typing");
    bubbleEl.textContent = "";
    const words = text.split(" ");
    let i = 0;
    const step = () => {
      bubbleEl.textContent += (i === 0 ? "" : " ") + words[i];
      i++;
      scrollToBottom();
      if (i < words.length) {
        setTimeout(step, 14 + Math.random() * 20);
      }
    };
    step();
  }

  function appendErrorBubble(message) {
    if (!chatThread) return;
    const row = document.createElement("div");
    row.className = "bubble-row bubble-ai";
    row.innerHTML = `<span class="ai-avatar">VD</span><div class="bubble is-error"></div>`;
    row.querySelector(".bubble").textContent = message;
    chatThread.appendChild(row);
    scrollToBottom();
  }

  async function submitQuestion(question) {
    appendUserBubble(question);
    const typingRow = appendTypingBubble();
    const typingBubble = typingRow.querySelector(".bubble");

    if (sendBtn) sendBtn.disabled = true;

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "question=" + encodeURIComponent(question),
      });

      const data = await res.json();

      if (!res.ok || data.error) {
        typingRow.remove();
        appendErrorBubble(data.error || "Something went wrong. Please try again.");
      } else {
        revealAnswer(typingBubble, data.answer);
      }
    } catch (err) {
      typingRow.remove();
      appendErrorBubble("Network error — please check your connection and try again.");
    } finally {
      if (sendBtn) sendBtn.disabled = false;
    }
  }

  if (askForm && questionInput) {
    askForm.addEventListener("submit", (e) => {
      const question = questionInput.value.trim();
      if (!question) return;
      e.preventDefault();
      questionInput.value = "";
      submitQuestion(question);
    });
  }

  document.querySelectorAll(".suggestion-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const question = chip.getAttribute("data-question");
      if (!question) return;
      closeSidebar();
      if (askForm) {
        submitQuestion(question);
      }
    });
  });

  // Land on the latest message on load
  scrollToBottom();
});
