let toggleBtn = document.getElementById("toggle-btn");
let body = document.body;
let darkMode = localStorage.getItem("dark-mode");

const enableDarkMode = () => {
  toggleBtn.classList.replace("fa-sun", "fa-moon");
  body.classList.add("dark");
  localStorage.setItem("dark-mode", "enabled");
};

const disableDarkMode = () => {
  toggleBtn.classList.replace("fa-moon", "fa-sun");
  body.classList.remove("dark");
  localStorage.setItem("dark-mode", "disabled");
};

if (darkMode === "enabled") {
  enableDarkMode();
}

toggleBtn.onclick = (e) => {
  darkMode = localStorage.getItem("dark-mode");
  if (darkMode === "disabled") {
    enableDarkMode();
  } else {
    disableDarkMode();
  }
};

let isAlertActive = false;
let alertInterval;
let originalBackgroundColor;
let audio = new Audio("alertsound.mp3");
audio.loop = true;

document.addEventListener("keydown", function (event) {
  if (event.key === "P" || event.key === "p") {
    if (!isAlertActive) {
      originalBackgroundColor = document.body.style.backgroundColor;
      alertInterval = setInterval(function () {
        document.body.style.backgroundColor =
          document.body.style.backgroundColor === "red"
            ? originalBackgroundColor
            : "red";
      }, 500);

      audio.play();

      isAlertActive = true;
    } else {
      clearInterval(alertInterval);
      document.body.style.backgroundColor = originalBackgroundColor;
      audio.pause();
      audio.currentTime = 0;
      isAlertActive = false;
    }
  }
});

let profile = document.querySelector(".header .flex .profile");

document.querySelector("#user-btn").onclick = () => {
  profile.classList.toggle("active");
  search.classList.remove("active");
};

let search = document.querySelector(".header .flex .search-form");

document.querySelector("#search-btn").onclick = () => {
  search.classList.toggle("active");
  profile.classList.remove("active");
};

let sideBar = document.querySelector(".side-bar");

document.querySelector("#menu-btn").onclick = () => {
  sideBar.classList.toggle("active");
  body.classList.toggle("active");
};

document.querySelector("#close-btn").onclick = () => {
  sideBar.classList.remove("active");
  body.classList.remove("active");
};

document.addEventListener("keydown", function (event) {
  if (event.key === "f" || event.key === "F") {
    sideBar.classList.toggle("active");
    body.classList.toggle("active");
  }
});

window.onscroll = () => {
  profile.classList.remove("active");
  search.classList.remove("active");

  if (window.innerWidth < 1200) {
    sideBar.classList.remove("active");
    body.classList.remove("active");
  }
};
