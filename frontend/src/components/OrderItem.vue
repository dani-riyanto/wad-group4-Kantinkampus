<script setup>
const props = defineProps({
  order: { type: Object, required: true }
})
const emit = defineEmits(['delete-order'])

const statusClass = (status) => {
  if (status === 'Baru') return 'bg-[#521d10] text-[#f97316] border-[#7c2d12]'
  if (status === 'Diproses') return 'bg-[#3b2d10] text-[#eab308] border-[#713f12]'
  return 'bg-[#14351e] text-[#22c55e] border-[#14532d]'
}

const handleDelete = () => {
  if (window.confirm(`Apakah Anda yakin ingin menghapus pesanan ${props.order.order_number} (${props.order.customer_name})?`)) {
    emit('delete-order', props.order.id)
  }
const formatPrice = (price) => {
  let val = price
  if (typeof val === 'string') val = val.replace(/\./g, '').replace(/[^0-9]/g, '')
  return Number(val || 0).toLocaleString('id-ID')
}
</script>

<template>
  <div class="bg-[#1a1914] p-4 rounded-xl border border-[#2e2d24] mb-3">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-full bg-[#2e2c24] text-white font-bold flex items-center justify-center text-sm border border-[#403e33]">
          {{ order.customer_name ? order.customer_name.charAt(0).toUpperCase() : '?' }}
        </div>
        <div>
          <h4 class="font-bold text-white text-sm leading-tight">{{ order.customer_name }}</h4>
          <span class="text-xs text-[#858276]">{{ order.order_number }} · {{ order.time }}</span>
        </div>
      </div>
      <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full border', statusClass(order.status)]">
        {{ order.status }}
      </span>
    </div>

    <div class="bg-[#24231b] p-3 rounded-lg flex items-center justify-between mb-3">
      <div class="flex items-start space-x-3">
        <span class="text-xs font-bold text-[#d94814] bg-[#3a2016] px-1.5 py-0.5 rounded">{{ order.quantity }}x</span>
        <div>
          <p class="text-xs font-bold text-white">{{ order.menu }}</p>
          <p class="text-[11px] text-[#858276] italic">{{ order.notes || 'Tanpa catatan' }}</p>
        </div>
      </div>
      <span class="text-xs font-bold text-white">Rp {{ formatPrice(order.total_price) }}</span>
    </div>

    <div class="flex items-center justify-end space-x-4 text-xs text-[#858276] pt-1">
      <button type="button" class="hover:text-white flex items-center space-x-1 cursor-not-allowed opacity-60 focus-visible:ring-2 focus-visible:ring-white rounded">
        <span>✏️ Ubah (PUT)</span>
      </button>
      <button type="button" @click="handleDelete" class="hover:text-red-400 text-red-500/80 flex items-center space-x-1 focus-visible:ring-2 focus-visible:ring-red-400 rounded px-1">
        <span>🗑️ Hapus</span>
      </button>
    </div>
  </div>
</template>
