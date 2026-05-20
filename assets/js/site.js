function prettifySlug(value) {
  return String(value || "")
    .split("-")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function looksMojibake(value) {
  return /[ÃÅÆÇÐÑØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]/.test(value || "");
}

function getReferenceTitle(entry) {
  if (entry && entry.name && !looksMojibake(entry.name)) {
    return entry.name;
  }

  if (entry && entry.slug) {
    return prettifySlug(entry.slug);
  }

  return "Reference";
}

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

async function loadReferenceImages() {
  const galleries = Array.from(document.querySelectorAll("[data-reference-gallery]"));
  if (!galleries.length) {
    return;
  }

  try {
    const response = await fetch("/data/reference-images.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    galleries.forEach((gallery) => {
      const kind = gallery.getAttribute("data-reference-gallery");
      const entries = Array.isArray(payload[kind]) ? payload[kind] : [];
      gallery.innerHTML = "";

      if (!entries.length) {
        gallery.innerHTML = '<article class="notice reference-empty">Run <code>python3 scripts/download_wuwatracker_reference_images.py</code> to populate this gallery.</article>';
        return;
      }

      entries.slice(0, 12).forEach((entry) => {
        const card = document.createElement("article");
        card.className = `reference-card ${kind === "weapons" ? "weapon" : "character"}`;

        const art = document.createElement("div");
        art.className = "reference-art";

        const img = document.createElement("img");
        img.src = entry.src;
        img.alt = getReferenceTitle(entry);
        img.loading = "lazy";
        img.decoding = "async";
        art.appendChild(img);

        const meta = document.createElement("div");
        meta.className = "reference-meta";
        meta.innerHTML = `<h3>${getReferenceTitle(entry)}</h3>`;

        card.appendChild(art);
        card.appendChild(meta);
        gallery.appendChild(card);
      });
    });
  } catch (error) {
    galleries.forEach((gallery) => {
      gallery.innerHTML = '<article class="notice reference-empty">Reference images are not available yet. Run the local download script and publish the generated files.</article>';
    });
  }
}

window.addEventListener("DOMContentLoaded", () => {
  loadReferenceImages();
});
