const BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000`

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    credentials: 'include'
  })
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const detail = Array.isArray(errorData.detail)
      ? errorData.detail.map(item => item.msg).join(', ')
      : errorData.detail;
    const error = new Error(
      detail || errorData.message || `Permintaan gagal (${res.status})`
    )
    error.status = res.status
    if (res.status === 401 && !['/auth/login', '/auth/session'].includes(path)) {
      window.dispatchEvent(new Event('auth-expired'))
    }
    throw error
  }
  if (res.status === 204) return null
  return res.json()
}

function csrfHeaders(csrfToken) {
  return { 'X-CSRF-Token': csrfToken }
}

export function login(username, password) {
  return request('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
}

export function getAuthSession() {
  return request('/auth/session')
}

export function hasSessionHint() {
  return document.cookie
    .split(';')
    .some(cookie => cookie.trim().startsWith('csrf_token='))
}

export function logout(csrfToken) {
  return request('/auth/logout', {
    method: 'DELETE',
    headers: csrfHeaders(csrfToken)
  })
}

export function updateProfile(csrfToken, userId, displayName) {
  return request(`/users/${userId}`, {
    method: 'PATCH',
    headers: {
      ...csrfHeaders(csrfToken),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ display_name: displayName })
  })
}

export function createUser(csrfToken, username, password) {
  return request('/users', {
    method: 'POST',
    headers: {
      ...csrfHeaders(csrfToken),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
}

export function fetchUsers() {
  return request('/users')
}

export function deleteUser(csrfToken, userId) {
  return request(`/users/${userId}`, {
    method: 'DELETE',
    headers: csrfHeaders(csrfToken)
  })
}

export async function fetchOrders(search = '', signal = null) {
  const params = new URLSearchParams({ skip: 0, limit: 10 });
  if (search) params.append('search', search);

  return request(`/sessions?${params.toString()}`, { signal })
}

export async function createOrder(orderData, csrfToken) {
  return request('/sessions', {
    method: 'POST',
    headers: {
      ...csrfHeaders(csrfToken),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(orderData)
  });
}

export async function deleteOrder(id, csrfToken) {
  return request(`/sessions/${id}`, {
    method: 'DELETE',
    headers: csrfHeaders(csrfToken)
  })
}

export async function fetchMenus() {
  return request('/menus')
}

export async function updateOrder(id, data, csrfToken) {
  return request(`/sessions/${id}`, {
    method: 'PATCH',
    headers: {
      ...csrfHeaders(csrfToken),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
}

export async function createMenu(menuData, csrfToken) {
  return request('/menus', {
    method: 'POST',
    headers: {
      ...csrfHeaders(csrfToken),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(menuData)
  })
}