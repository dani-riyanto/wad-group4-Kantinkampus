<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import HeaderNav from './components/HeaderNav.vue'
import AuthPanel from './components/AuthPanel.vue'
import DashboardBanner from './components/DashboardBanner.vue'
import DashboardStats from './components/DashboardStats.vue'
import OrderForm from './components/OrderForm.vue'
import OrderList from './components/OrderList.vue'
import SiteFooter from './components/SiteFooter.vue'
import {
  createOrder,
  createUser,
  deleteUser,
  deleteOrder,
  fetchUsers,
  fetchOrders,
  hasSessionHint,
  getAuthSession,
  login,
  logout,
  updateOrder,
  updateProfile
} from './services/api.js'
import MenuForm from './components/MenuForm.vue'

const orders = ref([])
const loading = ref(false)
const error = ref(null)
const serverError = ref('')
const isSubmitting = ref(false)
const searchQuery = ref('')
const activeTab = ref('Semua')
const currentUser = ref(null)
const users = ref([])
const authBusy = ref(false)
const authError = ref('')
const authMessage = ref('')

let abortController = null

const loadOrders = async () => {
  if (!currentUser.value) {
    orders.value = []
    return
  }
  if (abortController) abortController.abort()
  abortController = new AbortController()
  loading.value = true
  error.value = null

  try {
    const data = await fetchOrders(searchQuery.value, abortController.signal)
    orders.value = Array.isArray(data) ? data : (data.data || [])
  } catch (err) {
    if (err.name !== 'AbortError') {
      error.value = err.message || 'Gagal terhubung ke server FastAPI (http://localhost:8000).'
      if (err.status === 401) expireAuth()
    }
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  if (currentUser.value?.role !== 'admin') {
    users.value = []
    return
  }
  users.value = await fetchUsers()
}

let searchDebounce = null
watch(searchQuery, () => {
  clearTimeout(searchDebounce)
  searchDebounce = setTimeout(() => {
    if (currentUser.value) loadOrders()
  }, 300)
})

const expireAuth = () => {
  currentUser.value = null
  orders.value = []
  users.value = []
  authError.value = 'Sesi berakhir. Silakan login kembali.'
}

const handleAuthExpired = () => expireAuth()

onMounted(async () => {
  window.addEventListener('auth-expired', handleAuthExpired)
  if (!hasSessionHint()) return
  authBusy.value = true
  try {
    const session = await getAuthSession()
    currentUser.value = session.user
    await loadOrders()
    await loadUsers()
  } catch (err) {
    if (err.status !== 401) {
      authError.value = `Tidak dapat memeriksa sesi: ${err.message}`
    }
  } finally {
    authBusy.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('auth-expired', handleAuthExpired)
  if (abortController) abortController.abort()
  if (searchDebounce) clearTimeout(searchDebounce)
})

const filteredOrders = computed(() => {
  if (activeTab.value === 'Semua') return orders.value
  return orders.value.filter(o => o.status === activeTab.value)
})

const handleCreateOrder = async (orderData, resetFn) => {
  isSubmitting.value = true
  serverError.value = ''
  try {
    await createOrder(orderData)
    resetFn()
    await loadOrders()
  } catch (err) {
    serverError.value = err.message
  } finally {
    isSubmitting.value = false
  }
}

const handleDeleteOrder = async (id) => {
  try {
    await deleteOrder(id)
    await loadOrders()
  } catch (err) {
    alert(`Gagal menghapus: ${err.message}`)
  }
}

const handleMenuAdded = () => {
  // Karena order form mengambil data menu dari database,
  // kita bisa memaksa reload halaman agar form pesanan mengambil menu terbaru
  window.location.reload() 
}

const handleLogin = async ({ username, password }) => {
  authBusy.value = true
  authError.value = ''
  authMessage.value = ''
  try {
    const result = await login(username, password)
    currentUser.value = result.user
    authMessage.value = `Berhasil login sebagai ${currentUser.value.username}.`
    await loadOrders()
    await loadUsers()
  } catch (err) {
    currentUser.value = null
    authError.value = err.message
  } finally {
    authBusy.value = false
  }
}

const handleLogout = async () => {
  authBusy.value = true
  authError.value = ''
  authMessage.value = ''
  try {
    await logout()
    currentUser.value = null
    orders.value = []
    users.value = []
    authMessage.value = 'Anda berhasil logout.'
  } catch (err) {
    authError.value = `Logout gagal; sesi masih aktif. Coba lagi. (${err.message})`
  } finally {
    authBusy.value = false
  }
}

const handleProfileUpdate = async (displayName) => {
  if (!currentUser.value) return
  authBusy.value = true
  authError.value = ''
  authMessage.value = ''
  try {
    currentUser.value = await updateProfile(
      currentUser.value.id,
      displayName
    )
    authMessage.value = 'Profil berhasil diperbarui.'
  } catch (err) {
    authError.value = err.message
  } finally {
    authBusy.value = false
  }
}

const handleCreateUser = async ({ username, password }) => {
  authBusy.value = true
  authError.value = ''
  authMessage.value = ''
  try {
    const user = await createUser(username, password)
    authMessage.value = `Akun ${user.username} berhasil dibuat dengan role user.`
    await loadUsers()
  } catch (err) {
    authError.value = err.message
  } finally {
    authBusy.value = false
  }
}

const handleDeleteUser = async (user) => {
  if (!window.confirm(`Hapus akun ${user.username}? Pesanan lama akan dialihkan ke admin.`)) {
    return
  }
  authBusy.value = true
  authError.value = ''
  authMessage.value = ''
  try {
    await deleteUser(user.id)
    authMessage.value = `Akun ${user.username} berhasil dihapus.`
    await loadUsers()
  } catch (err) {
    authError.value = err.message
  } finally {
    authBusy.value = false
  }
}

const handleUpdateOrder = async (order) => {
  try {
    if (currentUser.value?.role === 'admin') {
      const newStatus = prompt(`Ubah status untuk ${order.customer_name}:`, order.status)
      if (newStatus && newStatus !== order.status) {
        await updateOrder(order.id, { status: newStatus })
        await loadOrders()
      }
      return
    }

    const customerName = prompt('Nama pelanggan:', order.customer_name)
    if (customerName === null) return
    const quantityInput = prompt('Jumlah:', String(order.quantity))
    if (quantityInput === null) return
    const quantity = Number(quantityInput)
    if (!Number.isInteger(quantity) || quantity < 1) {
      throw new Error('Jumlah pesanan harus bilangan bulat minimal 1.')
    }
    const notes = prompt('Catatan:', order.notes || '')
    if (notes === null) return
    await updateOrder(
      order.id,
      { customer_name: customerName, quantity, notes }
    )
    await loadOrders()
  } catch (err) {
    alert(`Gagal memperbarui pesanan: ${err.message}`)
  }
}
</script>

<template>
  <div class="min-h-screen bg-white font-sans text-body">
    <HeaderNav />
    <AuthPanel
      :user="currentUser"
      :busy="authBusy"
      :error="authError"
      :message="authMessage"
      :users="users"
      @login="handleLogin"
      @logout="handleLogout"
      @update-profile="handleProfileUpdate"
      @create-user="handleCreateUser"
      @delete-user="handleDeleteUser"
    />
    <template v-if="currentUser">
      <DashboardBanner />
      <DashboardStats :orders="orders" />
      <main class="bg-white">
        <div class="container grid grid-cols-1 gap-8 py-8 sm:py-10 lg:grid-cols-12">
          <div class="lg:col-span-5 lg:sticky lg:top-6 lg:self-start">
            <OrderForm :is-submitting="isSubmitting" :server-error="serverError" @create-order="handleCreateOrder" />
            <MenuForm
              v-if="currentUser.role === 'admin'"
              @menu-added="handleMenuAdded"
            />
          </div>

          <div class="lg:col-span-7">
            <OrderList
              :orders="filteredOrders"
              :loading="loading"
              :error="error"
              :is-admin="currentUser.role === 'admin'"
              v-model:searchQuery="searchQuery"
              v-model:activeTab="activeTab"
              @retry-fetch="loadOrders"
              @delete-order="handleDeleteOrder"
              @update-order="handleUpdateOrder"
            />
          </div>
        </div>
      </main>
    </template>
    <section v-else class="container py-12 text-center">
      <h2 class="font-serif text-2xl text-primary">Login diperlukan</h2>
      <p class="mt-2 text-muted">Masuk untuk mengakses menu dan pesanan.</p>
    </section>
    <SiteFooter />
  </div>
</template>
