<script setup>
import { computed } from 'vue'

const props = defineProps({
  orders: { type: Array, default: () => [] }
})

const totalOrders = computed(() => props.orders.length)
const pendingOrders = computed(() => props.orders.filter(o => o.status === 'Baru' || o.status === 'Diproses').length)
const totalRevenue = computed(() => {
  const sum = props.orders.reduce((acc, curr) => {
    let raw = curr.total_price
    if (typeof raw === 'string') {
      raw = raw.replace(/\./g, '').replace(/[^0-9]/g, '')
    }
    return acc + (Number(raw) || 0)
  }, 0)
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(sum)
})
</script>

<template>
  <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
    <div class="bg-[#22211b] p-5 rounded-xl border border-[#333129]">
      <p class="text-xs text-[#9e9b8f] font-medium">Total pesanan</p>
      <p class="text-3xl font-bold text-white mt-2">{{ totalOrders }}</p>
      <p class="text-xs text-[#706e63] mt-2">Data tersimpan otomatis</p>
    </div>

    <div class="bg-[#22211b] p-5 rounded-xl border border-[#333129]">
      <p class="text-xs text-[#9e9b8f] font-medium">Perlu diproses</p>
      <p class="text-3xl font-bold text-white mt-2">{{ pendingOrders }}</p>
      <p class="text-xs text-[#d94814] mt-2 font-medium">Segera konfirmasi</p>
    </div>

    <div class="bg-[#22211b] p-5 rounded-xl border border-[#333129]">
      <p class="text-xs text-[#9e9b8f] font-medium">Estimasi pendapatan</p>
      <p class="text-3xl font-bold text-white mt-2">{{ totalRevenue }}</p>
      <p class="text-xs text-[#706e63] mt-2">Dari semua pesanan</p>
    </div>
  </section>
</template>
