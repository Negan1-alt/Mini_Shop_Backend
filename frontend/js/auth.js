renderTop(false);
const f = $("form"), msg = $("msg"), reg = f.dataset.mode === "register";
if (new URLSearchParams(location.search).has("registered")) { msg.className = "ok"; msg.textContent = "Account created. Log in to continue."; }
f.onsubmit = async e => {
  e.preventDefault(); msg.className = ""; msg.textContent = "";
  const email = f.email.value.trim(), body = JSON.stringify({ email, password: f.password.value });
  try {
    if (reg) { await api("/register", { method: "POST", body }); location.href = "login.html?registered=1"; }
    else { const r = await api("/login", { method: "POST", body }); setUser({ token: r.access_token, role: r.role, email: email.toLowerCase() }); location.href = "index.html"; }
  } catch (err) { msg.textContent = err.message; }
};
