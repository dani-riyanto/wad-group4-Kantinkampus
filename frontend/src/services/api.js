const BASE_URL = 'http://localhost:8000';

export async function fetchOrders(search = '', signal = null) {
  const params = new URLSearchParams({ skip: 0, limit: 10 });
  if (search) params.append('search', search);

  const res = await fetch(`${BASE_URL}/sessions?${params.toString()}`, { signal });
  if (!res.ok) throw new Error(`Gagal mengambil data (${res.status})`);
  return await res.json();
}

export async function createOrder(orderData) {
  const res = await fetch(`${BASE_URL}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(orderData)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.message || `Gagal menambah pesanan (${res.status})`);
  }
  return await res.json();
}

export async function deleteOrder(id) {
  const res = await fetch(`${BASE_URL}/sessions/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Gagal menghapus pesanan (${res.status})`);
  return true;
}
