let orders = [];

const tbody = document.querySelector("#adminOrders tbody");

// ================================
// Load orders from backend
// ================================
async function loadOrders() {
  try {
    const res = await fetch("/api/orders");

    if (res.status === 401) {
      console.warn("Admin not logged in");
      return;
    }

    orders = await res.json();
    renderOrders();

  } catch (err) {
    console.error("Failed to load orders", err);
  }
}

// ================================
// Render Orders (COLUMN PERFECT)
// ================================
function renderOrders() {
  if (!orders || orders.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="10" style="text-align:center;font-weight:600;">
          No Orders Yet
        </td>
      </tr>`;
    return;
  }

  tbody.innerHTML = "";

  orders.forEach((order, index) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <!-- # -->
      <td>${index + 1}</td>

      <!-- Customer -->
      <td>${order.customer_name || "N/A"}</td>

      <!-- Address -->
      <td>${order.address || "N/A"}</td>

      <!-- Phone -->
      <td>📞 ${order.phone || "N/A"}</td>

      <!-- Product -->
      <td style="color:#ff5722;font-weight:600;">
        ${order.product}
      </td>

     <!-- Qty -->
      <td>${order.qty || 1}</td>
      <!-- Price -->
      
      <td style="color:#4caf50;font-weight:700;">
        ₹${order.total_price ?? order.price}
      </td>

     

      <!-- Payment Status -->
      <td>
        <strong style="color:${order.status === "Paid" ? "#2e7d32" : "#e65100"}">
          ${order.status}
        </strong>
      </td>

      <!-- Date -->
      <td>${order.created_at}</td>

      <!-- Actions -->
      <td>
        <button onclick="toggleStatus(${order.id})"
          style="background:#ff9800;color:white;padding:6px 10px;border:none;border-radius:6px;cursor:pointer;">
          Toggle
        </button>

        <button onclick="deleteOrder(${order.id})"
          style="background:#f44336;color:white;padding:6px 10px;border:none;border-radius:6px;cursor:pointer;">
          Delete
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}

// ================================
// Toggle Payment Status
// ================================
async function toggleStatus(id) {
  try {
    const res = await fetch(`/api/orders/${id}/toggle`, {
      method: "PATCH"
    });

    const data = await res.json();
    if (data.success) loadOrders();

  } catch (err) {
    console.error("Toggle failed", err);
  }
}

// ================================
// Delete Order
// ================================
async function deleteOrder(id) {
  if (!confirm("Delete this order?")) return;

  try {
    const res = await fetch(`/api/orders/${id}`, {
      method: "DELETE"
    });

    const data = await res.json();
    if (data.success) loadOrders();

  } catch (err) {
    console.error("Delete failed", err);
  }
}

// ================================
// Initial Load
// ================================
document.addEventListener("DOMContentLoaded", loadOrders);
