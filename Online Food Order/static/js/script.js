// =================================================
// MENU PAGE – Quantity + Order Now
// =================================================
function changeQty(btn, step) {
  const item = btn.closest(".item");
  const qtyInput = item.querySelector(".qty");

  let qty = parseInt(qtyInput.value);
  qty += step;

  if (qty < 1) qty = 1;
  qtyInput.value = qty;
}

function orderNow(btn) {
  const item = btn.closest(".item");

  const product = item.dataset.product;
  const unitPrice = parseInt(item.dataset.price);
  const qty = parseInt(item.querySelector(".qty").value);

  const total = unitPrice * qty;

  window.location.href =
    `/payment?product=${product}&price=${total}&qty=${qty}`;
}

// =================================================
// PAYMENT PAGE – Capture URL Params
// =================================================
if (window.location.pathname.includes("/payment")) {
  const params = new URLSearchParams(window.location.search);

  const product = params.get("product") || "Unknown Product";
  const price = params.get("price") || "0";
  const qty = params.get("qty") || "1";

  const productName = document.getElementById("productName");
  const productPrice = document.getElementById("productPrice");

  if (productName) {
    productName.textContent = `Order: ${product}`;
  }

  if (productPrice) {
    productPrice.textContent = `Price: ₹${price} (Qty: ${qty})`;
  }

  // store qty hidden for payment
  const qtyInput = document.getElementById("qtyInput");
  if (qtyInput) qtyInput.value = qty;
}

// =================================================
// PAYMENT FUNCTION – Cash on Delivery
// =================================================
function makePayment(event) {
  event.preventDefault();

  const params = new URLSearchParams(window.location.search);

  const product = params.get("product") || "Unknown Product";
  const price = params.get("price") || "0";
  const qty = params.get("qty") || "1";

  const fullName = document.getElementById("fullName")?.value.trim();
  const street = document.getElementById("street")?.value.trim();
  const city = document.getElementById("city")?.value.trim();
  const state = document.getElementById("state")?.value.trim();
  const pin = document.getElementById("pin")?.value.trim();
  const phone = document.getElementById("phone")?.value.trim();

  if (!fullName || !street || !city || !pin || !phone) {
    alert("⚠️ Please fill all the required details before placing the order.");
    return;
  }

  const order = {
    product: product,
    qty: parseInt(qty),
    price: parseInt(price),
    customer: fullName,
    address: `${street}, ${city}, ${state}, ${pin}`,
    phone: phone,
    status: "Cash on Delivery",
    date: new Date().toLocaleString()
  };

  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  orders.push(order);
  localStorage.setItem("orders", JSON.stringify(orders));

  localStorage.setItem("paymentDone", "true");
  alert("✅ Order Placed Successfully!");

  document.getElementById("paymentForm").reset();
  window.location.href = "/";
}

// expose function
if (window.location.pathname.includes("/payment")) {
  window.makePayment = makePayment;
}

// =================================================
// HOME PAGE – Success Message
// =================================================
if (window.location.pathname === "/" || window.location.pathname.includes("index")) {
  const msgBox = document.getElementById("paymentMsg");

  if (localStorage.getItem("paymentDone") === "true") {
    if (msgBox) msgBox.classList.remove("hidden");
    localStorage.removeItem("paymentDone");
  }
}

// =================================================
// ADMIN PANEL – LocalStorage Orders (Basic)
// =================================================
if (window.location.pathname.includes("admin")) {
  const pass = prompt("Enter Admin Password:");

  if (pass !== "admin123") {
    alert("Access Denied!");
    window.location.href = "/";
  } else {
    const orders = JSON.parse(localStorage.getItem("orders")) || [];
    const list = document.getElementById("adminOrders");

    if (list) {
      list.innerHTML = "";

      if (orders.length === 0) {
        list.innerHTML = "<li>No Orders Yet</li>";
      } else {
        orders.forEach((o, i) => {
          const li = document.createElement("li");
          li.textContent =
            `${i + 1}) ${o.product} | Qty: ${o.qty} | ₹${o.price} | ${o.customer} | 📞 ${o.phone}`;
          list.appendChild(li);
        });
      }
    }
  }
}
