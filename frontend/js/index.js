renderTop(true);
let all = [], timer;
const grad = id => { const h = (id * 47) % 360; return `linear-gradient(160deg,hsl(${h} 70% 52%),hsl(${(h + 40) % 360} 70% 28%))`; };

async function load(q = "") {
  $("grid").innerHTML = '<p class="empty">Loading…</p>';
  try { all = await api(q ? "/products?search=" + encodeURIComponent(q) : "/products"); }
  catch (e) { $("grid").innerHTML = '<p class="empty">' + esc(e.message) + "</p>"; return; }
  draw();
}

function card(p) {
  const out = p.stock != null && p.stock <= 0;
  const cover = p.image_url ? `<img class="cover" src="${esc(p.image_url)}" alt="">`
    : `<div class="cover" style="background:${grad(p.id)}"><b>${esc(p.name)}</b></div>`;
  const btn = !getUser() ? '<a class="add" href="login.html">Log in to buy</a>'
    : out ? '<button class="add" disabled>Out of stock</button>'
    : `<button class="add" data-id="${p.id}">Add to cart</button>`;
  const low = p.stock > 0 && p.stock <= 5 ? `<p class="meta">Only ${p.stock} left</p>` : "";
  return `<article class="card">${cover}<h3>${esc(p.name)}</h3>` +
    (p.description ? `<p class="meta">${esc(p.description)}</p>` : "") + low +
    `<div class="row"><span class="price">${p.price != null ? money(p.price) : ""}</span>${btn}</div></article>`;
}

function draw() {
  const l = all.filter(p => !$("instock").checked || p.stock > 0), s = $("sort").value;
  if (s === "name") l.sort((a, b) => a.name.localeCompare(b.name));
  if (s === "low") l.sort((a, b) => (a.price ?? 0) - (b.price ?? 0));
  if (s === "high") l.sort((a, b) => (b.price ?? 0) - (a.price ?? 0));
  $("n").textContent = "(" + l.length + ")";
  $("grid").innerHTML = l.length ? l.map(card).join("") : '<p class="empty">No products found. Try another search.</p>';
}

document.addEventListener("click", e => {
  const t = e.target.closest("[data-id]"); if (!t) return;
  addToCart(all.find(p => p.id == t.dataset.id));
});
$("sort").onchange = draw;
$("instock").onchange = draw;
$("q").oninput = e => { clearTimeout(timer); timer = setTimeout(() => load(e.target.value.trim()), 300); };
load();