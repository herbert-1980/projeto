document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("mainModal");
  var loginBtn = document.getElementById("loginBtn");
  var registerBtn = document.getElementById("registerBtn");
  var closeBtn = document.getElementsByClassName("btn-close")[0];

  // Verificar se os elementos existem
  if (!modal || !loginBtn || !registerBtn || !closeBtn) {
      console.error("Algum elemento modal não foi encontrado no DOM.");
      return;
  }

  loginBtn.onclick = function () {
      modal.style.display = "block";
      document.getElementById("loginSection").style.display = "block";
      document.getElementById("registerSection").style.display = "none";
      document.getElementById("logoutSection").style.display = "none";
  };

  registerBtn.onclick = function () {
      modal.style.display = "block";
      document.getElementById("loginSection").style.display = "none";
      document.getElementById("registerSection").style.display = "block";
      document.getElementById("logoutSection").style.display = "none";
  };

  closeBtn.onclick = function () {
      modal.style.display = "none";
  };

  window.onclick = function (event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  };


  let currentIndex = 0;

  function showBanner(index) {
      const bannerContainer = document.getElementById("banner-container");
      if (banners.length > 0 && banners[index]) {
          bannerContainer.innerHTML = `
              <a href="${banners[index].link}" class="banner-item">
                  <img class="img-fluid" src="${banners[index].url}" style="width: 728px; height: 90px;" alt="Banner VIP">
              </a>
          `;
      } else {
          bannerContainer.innerHTML = "<p>Não há banners disponíveis no momento.</p>";
      }
  }

  function nextBanner() {
      currentIndex = (currentIndex + 1) % banners.length;
      showBanner(currentIndex);
  }

  // Exibir o primeiro banner se existir
  if (banners.length > 0) {
      showBanner(currentIndex);
      setInterval(nextBanner, 10000);
  } else {
      console.warn("Nenhum banner foi encontrado.");
  }
});
