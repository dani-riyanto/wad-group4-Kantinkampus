<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import HeaderNav from './components/HeaderNav.vue'
import DashboardBanner from './components/DashboardBanner.vue'
import DashboardStats from './components/DashboardStats.vue'
import OrderForm from './components/OrderForm.vue'
import OrderList from './components/OrderList.vue'
import { fetchOrders, createOrder, deleteOrder } from './services/api.js'

const orders = ref([])
const loading = ref(false)
const error = ref(null)
const serverError = ref('')
const isSubmitting = ref(false)
const searchQuery = ref('')
const activeTab = ref('Semua')

let abortController = null

const loadOrders = async () => {
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
    }
  } finally {
    loading.value = false
  }
}

let searchDebounce = null
watch(searchQuery, () => {
  clearTimeout(searchDebounce)
  searchDebounce = setTimeout(() => { loadOrders() }, 300)
})

onMounted(() => { loadOrders() })

onUnmounted(() => {
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
</script>

<template>
  <div class="min-h-screen bg-[#181712] text-[#f3f3f0] font-sans px-4 md:px-8 lg:px-16 pb-16">
    <div class="max-w-6xl mx-auto">
      <HeaderNav />
      <DashboardBanner />
      <DashboardStats :orders="orders" />

      <main class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div class="lg:col-span-5">
          <OrderForm :is-submitting="isSubmitting" :server-error="serverError" @create-order="handleCreateOrder" />
        </div>
        <div class="lg:col-span-7">
          <OrderList :orders="filteredOrders" :loading="loading" :error="error" v-model:searchQuery="searchQuery"
            v-model:activeTab="activeTab" @retry-fetch="loadOrders" @delete-order="handleDeleteOrder" />
        </div>
      </main>
    </div>
  </div>
</template>
