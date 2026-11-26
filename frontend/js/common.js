const $ = id => document.getElementById(id);
const money = n => "$" + Number(n || 0).toFixed(2);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

// ---- session (the backend returns only user_id for now, so we keep that) ----
const getUser = () => { try { return JSON.parse(localStorage.getItem("user")); } catch { return null; } };
const setUser = u => localStorage.setItem("user", JSON.stringify(u));
const logout = () => { localStorage.removeItem("user"); location.href = "index.html"; };

// ---- cart (stored in the browser until the backend has an /orders endpoint) ----
const cartKey = () => "cart_" + (getUser()?.email || "guest");
const getCart = () => { try { return JSON.parse(localStorage.getItem(cartKey())) || {}; } catch { return {}; } };
const saveCart = c => localStorage.setItem(cartKey(), JSON.stringify(c));

// ---- API helper: turns FastAPI errors ({"detail": ...}) into readable messages ----
async function api(path, opts = {}) {
  const token = getUser()?.token;
  let res;
  try {
    res = await fetch(API + path, {
      ...opts,
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: "Bearer " + token }),
        ...opts.headers,
      },
    });
  } catch { throw new Error("Can't reach the server. Is FastAPI running at " + API + " and is CORS enabled?"); }
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 && token) logout();   // token expired or invalid
  if (!res.ok) {
    const d = data.detail;
    throw new Error(typeof d === "string" ? d : Array.isArray(d) ? d.map(x => x.msg).join(", ") : "Request failed (" + res.status + ")");
  }
  return data;
}

function renderTop(withSearch) {
  const u = getUser();
  $("top").innerHTML =
    '<a class="logo" href="index.html">Pagebound</a>' +
    (withSearch ? '<input class="search" id="q" type="search" placeholder="Search products" aria-label="Search products">' : "") +
    (u ? '<span class="who">' + esc(u.email) + '</span><button class="pill" id="logoutBtn">Log out</button>'
       : '<a class="pill" href="login.html">Log in</a>') +
    '<button class="cartbtn" id="openCart">Cart (<span id="count">0</span>)</button>';
  document.body.insertAdjacentHTML("beforeend",
    '<aside class="drawer" id="drawer" aria-label="Cart"><h2>Your cart <button class="x" id="closeCart" aria-label="Close cart">✕</button></h2>' +
    '<div class="items" id="items"></div><div class="total"><span>Total</span><span id="total">$0.00</span></div>' +
    '<button class="checkout" id="checkout">Checkout</button></aside>');
  if (u) $("logoutBtn").onclick = logout;
  $("openCart").onclick = () => $("drawer").classList.add("open");
  $("closeCart").onclick = () => $("drawer").classList.remove("open");
  $("checkout").onclick = () => alert("Checkout needs an orders endpoint on the backend. That's the next step.");
  document.addEventListener("click", e => {
    const t = e.target, c = getCart();
    if (t.dataset.inc) c[t.dataset.inc].n++;
    else if (t.dataset.dec) { if (--c[t.dataset.dec].n <= 0) delete c[t.dataset.dec]; }
    else if (t.dataset.rm) delete c[t.dataset.rm];
    else return;
    saveCart(c); renderCart();
  });
  renderCart();
}

function renderCart() {
  const c = getCart(), ids = Object.keys(c);
  let sum = 0, n = 0;
  $("items").innerHTML = ids.length ? ids.map(id => {
    const { p, n: k } = c[id]; sum += p.price * k; n += k;
    return '<div class="item"><div>' + esc(p.name) + '<div class="meta">' + money(p.price) + '</div></div>' +
      '<div class="qty"><button data-dec="' + id + '" aria-label="Less">−</button> ' + k +
      ' <button data-inc="' + id + '" aria-label="More">+</button> <button class="x" data-rm="' + id + '" aria-label="Remove">✕</button></div></div>';
  }).join("") : '<p class="meta">Your cart is empty. Add a product to get started.</p>';
  $("count").textContent = n; $("total").textContent = money(sum);
}

function addToCart(p) {
  const c = getCart();
  c[p.id] = c[p.id] || { p: { id: p.id, name: p.name, price: Number(p.price) || 0 }, n: 0 };
  c[p.id].n++; saveCart(c); renderCart(); $("drawer").classList.add("open");
}
