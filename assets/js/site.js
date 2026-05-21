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

function getReferenceHref(kind, entry) {
  if (!entry || !entry.slug) {
    return "";
  }

  if (kind === "characters") {
    return `/wuthering-waves-characters/${encodeURIComponent(entry.slug)}/`;
  }

  if (kind === "weapons") {
    return `/wuthering-waves-weapons/${encodeURIComponent(entry.slug)}/`;
  }

  if (kind === "items") {
    return `/wuthering-waves-items/${encodeURIComponent(entry.slug)}/`;
  }

  return "";
}

function buildReferenceLink(kind, entry) {
  const href = getReferenceHref(kind, entry);
  const title = getReferenceTitle(entry);
  return href && title ? { href, title } : null;
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

      entries.forEach((entry) => {
        const card = document.createElement("article");
        const variant = kind === "weapons" ? "weapon" : kind === "items" ? "item" : "character";
        card.className = `reference-card ${variant}`;

        const artLink = document.createElement("a");
        artLink.className = "reference-link";
        artLink.href = getReferenceHref(kind, entry);

        const art = document.createElement("div");
        art.className = "reference-art";

        const img = document.createElement("img");
        img.src = entry.src;
        img.alt = getReferenceTitle(entry);
        img.loading = "lazy";
        img.decoding = "async";
        art.appendChild(img);
        artLink.appendChild(art);

        const meta = document.createElement("div");
        meta.className = "reference-meta";
        meta.innerHTML = `<h3><a class="reference-link" href="${getReferenceHref(kind, entry)}">${getReferenceTitle(entry)}</a></h3>`;

        card.appendChild(artLink);
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

async function loadReferenceDirectories() {
  const directories = Array.from(document.querySelectorAll("[data-reference-directory]"));
  if (!directories.length) {
    return;
  }

  try {
    const response = await fetch("/data/reference-images.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    directories.forEach((directory) => {
      const kind = directory.getAttribute("data-reference-directory");
      const entries = Array.isArray(payload[kind]) ? payload[kind] : [];
      directory.innerHTML = "";

      if (!entries.length) {
        directory.innerHTML = '<article class="notice reference-empty">Reference directory entries are not available yet. Run the local download script and publish the generated files.</article>';
        return;
      }

      const sortedEntries = [...entries].sort((a, b) =>
        getReferenceTitle(a).localeCompare(getReferenceTitle(b), undefined, { sensitivity: "base" })
      );

      sortedEntries.forEach((entry) => {
        const linkData = buildReferenceLink(kind, entry);
        if (!linkData) {
          return;
        }

        const anchor = document.createElement("a");
        anchor.className = "directory-link";
        anchor.href = linkData.href;
        anchor.textContent = linkData.title;
        directory.appendChild(anchor);
      });
    });
  } catch (error) {
    directories.forEach((directory) => {
      directory.innerHTML = '<article class="notice reference-empty">Reference directory entries are not available yet. Run the local download script and publish the generated files.</article>';
    });
  }
}

window.addEventListener("DOMContentLoaded", () => {
  loadReferenceImages();
  loadReferenceDirectories();
});
