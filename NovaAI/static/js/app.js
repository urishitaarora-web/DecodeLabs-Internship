/* ==========================================================
   NovaAI
   Main Controller & Sidebar Engine
========================================================== */

const sendBtn = document.getElementById("send");
const downloadBtn = document.getElementById("download");
const clearBtn = document.getElementById("clear");
const voiceBtn = document.getElementById("voice");
const speakerBtn = document.getElementById("speakerBtn");

const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const toggleIcon = document.getElementById("toggleIcon");
const menuToggle = document.getElementById("menuToggle");
const sidebarClose = document.getElementById("sidebarClose");
const sidebarOverlay = document.getElementById("sidebarOverlay");

const SIDEBAR_STORAGE_KEY = "nova_sidebar_collapsed";

/* ==========================================================
   SIDEBAR COLLAPSE / EXPAND (DESKTOP)
========================================================== */

function initSidebarState() {
    if (!sidebar) return;

    if (window.innerWidth > 992) {
        const isCollapsed = localStorage.getItem(SIDEBAR_STORAGE_KEY) === "true";
        if (isCollapsed) {
            sidebar.classList.add("collapsed");
            sidebar.setAttribute("aria-expanded", "false");
            if (sidebarToggle) {
                sidebarToggle.setAttribute("title", "Expand Sidebar");
                sidebarToggle.setAttribute("aria-label", "Expand Sidebar");
            }
            if (toggleIcon) {
                toggleIcon.className = "fa-solid fa-chevron-right";
            }
        } else {
            sidebar.classList.remove("collapsed");
            sidebar.setAttribute("aria-expanded", "true");
            if (sidebarToggle) {
                sidebarToggle.setAttribute("title", "Collapse Sidebar");
                sidebarToggle.setAttribute("aria-label", "Collapse Sidebar");
            }
            if (toggleIcon) {
                toggleIcon.className = "fa-solid fa-chevron-left";
            }
        }
    }
}

function toggleSidebarCollapse() {
    if (!sidebar) return;

    const willCollapse = !sidebar.classList.contains("collapsed");
    sidebar.classList.toggle("collapsed", willCollapse);
    sidebar.setAttribute("aria-expanded", willCollapse ? "false" : "true");

    if (sidebarToggle) {
        sidebarToggle.setAttribute("title", willCollapse ? "Expand Sidebar" : "Collapse Sidebar");
        sidebarToggle.setAttribute("aria-label", willCollapse ? "Expand Sidebar" : "Collapse Sidebar");
    }

    if (toggleIcon) {
        toggleIcon.className = willCollapse ? "fa-solid fa-chevron-right" : "fa-solid fa-chevron-left";
    }

    localStorage.setItem(SIDEBAR_STORAGE_KEY, willCollapse ? "true" : "false");
}

/* ==========================================================
   MOBILE SIDEBAR DRAWER
========================================================== */

function openMobileSidebar() {
    if (!sidebar || !sidebarOverlay) return;
    sidebar.classList.add("mobile-open");
    sidebarOverlay.classList.add("active");
    document.body.style.overflow = "hidden";
}

function closeMobileSidebar() {
    if (!sidebar || !sidebarOverlay) return;
    sidebar.classList.remove("mobile-open");
    sidebarOverlay.classList.remove("active");
    document.body.style.overflow = "";
}

/* ==========================================================
   EVENT LISTENERS
========================================================== */

if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
}

if (downloadBtn) {
    downloadBtn.addEventListener("click", () => {
        downloadChat();
        if (window.innerWidth <= 992) {
            closeMobileSidebar();
        }
    });
}

if (clearBtn) {
    clearBtn.addEventListener("click", () => {
        clearChat();
        if (window.innerWidth <= 992) {
            closeMobileSidebar();
        }
    });
}

if (voiceBtn) {
    voiceBtn.addEventListener("click", startVoiceRecognition);
}

if (speakerBtn) {
    speakerBtn.addEventListener("click", toggleSpeaker);
}

if (sidebarToggle) {
    sidebarToggle.addEventListener("click", toggleSidebarCollapse);
}

if (menuToggle) {
    menuToggle.addEventListener("click", openMobileSidebar);
}

if (sidebarClose) {
    sidebarClose.addEventListener("click", closeMobileSidebar);
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", closeMobileSidebar);
}

// Close on Escape key
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && sidebar && sidebar.classList.contains("mobile-open")) {
        closeMobileSidebar();
    }
});

// Initialize on DOM load
window.addEventListener("DOMContentLoaded", () => {
    initSidebarState();
});

// Update on resize
window.addEventListener("resize", () => {
    if (window.innerWidth > 992) {
        closeMobileSidebar();
    }
});