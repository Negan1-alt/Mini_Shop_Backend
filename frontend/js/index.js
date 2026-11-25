renderTop(true);
let all = [], cat = "All", timer;
const grad = id => { const h = (id * 47) % 360; return `linear-gradient(160deg,hsl(${h} 70% 52%),hsl(${(h + 40) % 360} 70% 28%))`; };

async function load(q = "") {
  $("grid").innerHTML = '<p class="empty">Loading…</p>';
  try { all = await api(q ? "/products/search/by-name?name=" + encodeURIComponent(q) : "/products"); }
  catch (e) { $("grid").innerHTML = '<p class="empty">' + esc(e.message) + "</p>"; return; }
  cat = "All"; drawCats(); draw();
}
function drawCats() {
  const names = [...new Set(all.map(p => p.category).filter(Boolean))];
  $("cats").innerHTML = ["All", ...names].map(n =>
    `<button class="cat" aria-pressed="${n === cat}" data-c="${esc(n)}"><span>${esc(n)}</span><span>${n === "All" ? all.length : all.filter(p => p.category === n).length}</span></button>`).join("");
}
function card(p) {
  const cover = p.image_url ? `<img class="cover" src="${esc(p.image_url)}" alt="">`
    : `<div class="cover" style="background:${grad(p.id)}"><b>${esc(p.name)}</b></div>`;
  const btn = getUser() ? `<button class="add" data-id="${p.id}">Add to cart</button>` : '<a class="add" href="login.html">Log in to buy</a>';
  return `<article class="card">${cover}<h3>${esc(p.name)}</h3>` +
    (p.description ? `<p class="meta">${esc(p.description)}</p>` : "") +
    `<div class="row"><span class="price">${p.price != null ? money(p.price) : ""}</span>${btn}</div></article>`;
}
function draw() {
  const l = all.filter(p => cat === "All" || p.category === cat), s = $("sort").value;
  if (s === "name") l.sort((a, b) => a.name.localeCompare(b.name));
  if (s === "low") l.sort((a, b) => (a.price ?? 0) - (b.price ?? 0));
  if (s === "high") l.sort((a, b) => (b.price ?? 0) - (a.price ?? 0));
  $("n").textContent = "(" + l.length + ")";
  $("grid").innerHTML = l.length ? l.map(card).join("") : '<p class="empty">No products found. Try another search.</p>';
}
document.addEventListener("click", e => {
  const t = e.target.closest("[data-c],[data-id]"); if (!t) return;
  if (t.dataset.c) { cat = t.dataset.c; drawCats(); draw(); }
  else addToCart(all.find(p => p.id == t.dataset.id));
});
$("sort").onchange = draw;
$("q").oninput = e => { clearTimeout(timer); timer = setTimeout(() => load(e.target.value.trim()), 300); };
load();
