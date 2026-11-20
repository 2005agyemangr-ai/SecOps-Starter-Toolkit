const STORAGE_KEY = "lab_notes_v1";
let activeFilter = "All";

const loadNotes = () => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
};

const saveNotes = (notes) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
};

const render = () => {
  const listEl = document.getElementById("notes-list");
  const notes = loadNotes().filter((n) => activeFilter === "All" || n.tag === activeFilter);
  if (!notes.length) {
    listEl.innerHTML = `<p class="card">No notes for "${activeFilter}" yet.</p>`;
    return;
  }
  listEl.innerHTML = notes
    .map(
      (n) => `<article class="note-item">
        <span class="tag">${n.tag}</span>
        <h3>${n.title.replace(/</g, "&lt;")}</h3>
      </article>`
    )
    .join("");
};

document.getElementById("note-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const titleEl = document.getElementById("note-title");
  const tagEl = document.getElementById("note-tag");
  const title = titleEl.value.trim();
  if (!title) return;
  const notes = loadNotes();
  notes.unshift({ title, tag: tagEl.value });
  saveNotes(notes);
  titleEl.value = "";
  render();
});

document.getElementById("filter-bar").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-filter]");
  if (!btn) return;
  activeFilter = btn.dataset.filter;
  document.querySelectorAll("#filter-bar button").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  render();
});

render();
