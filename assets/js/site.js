document.addEventListener("click", (event) => {
  const trigger = event.target.closest(".video-lite");
  if (!trigger) {
    return;
  }

  const videoId = trigger.getAttribute("data-video-id");
  if (!videoId) {
    return;
  }

  const title = trigger.getAttribute("data-video-title") || "YouTube video";
  const wrapper = trigger.closest(".video-embed");
  if (!wrapper) {
    return;
  }

  const iframe = document.createElement("iframe");
  iframe.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(videoId)}?autoplay=1&rel=0`;
  iframe.title = title;
  iframe.loading = "lazy";
  iframe.allowFullscreen = true;
  iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";

  wrapper.replaceChildren(iframe);
});
