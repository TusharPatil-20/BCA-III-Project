// 📁 static/js/orders.js

// 🗑️ एखादी ऑर्डर डिलीट करा
async function deleteOrder(id) {
  if (!confirm(`⚠️ Are you sure you want to delete order #${id}?`)) return;

  const res = await fetch(`/api/orders/${id}`, { method: "DELETE" });
  const data = await res.json();

  if (data.success) {
    alert(`✅ Order #${id} deleted successfully`);
    location.reload();
  } else {
    alert(`❌ Failed to delete order #${id}`);
  }
}

// 🔁 पेमेंट स्टेटस बदलणे (Paid ↔ Cash on Delivery)
async function toggleStatus(id) {
  const res = await fetch(`/api/orders/${id}/toggle`, { method: "PATCH" });
  const data = await res.json();

  if (data.success) {
    alert(`✅ Status updated: ${data.new_status}`);
    location.reload();
  } else {
    alert(`❌ Failed to update status`);
  }
}

// 🧹 सगळ्या ऑर्डर्स डिलीट करा आणि ID रीसेट करा
async function clearOrders() {
  if (!confirm("⚠️ Are you sure you want to delete ALL orders and reset ID?")) return;

  const res = await fetch("/api/orders/clear", { method: "DELETE" });
  const data = await res.json();

  if (data.success) {
    alert("✅ All orders cleared! ID reset to 1.");
    location.reload();
  } else {
    alert("❌ Failed to clear orders.");
  }
}
