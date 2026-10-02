<script setup>
import OrderItem from './OrderItem.vue'
import StateLoading from './StateLoading.vue'
import StateEmpty from './StateEmpty.vue'
import StateError from './StateError.vue'

const props = defineProps({
  orders: { type: Array, default: () => [] },
  loading: Boolean,
  error: String,
  searchQuery: String,
  activeTab: String
})

defineEmits(['update:searchQuery', 'update:activeTab', 'retry-fetch', 'delete-order'])
const tabs = ['Semua', 'Baru', 'Diproses', 'Selesai']
</script>

<template>
  <div class="bg-[#22211b] p-6 rounded-2xl border border-[#333129]">
    <div class="flex items-center justify-between mb-4">
      <div>
        <span class="text-xs font-semibold tracking-wider text-[#9e9b8f] uppercase">Daftar Pesanan</span>
        <h3 class="font-serif text-2xl text-white">Pesanan terkini</h3>
      </div>
      <span class="text-xs text-[#9e9b8f] bg-[#181712] px-3 py-1 rounded-full border border-[#3c3a30]">
        {{ orders.length }} pesanan
      </span>
    </div>

    <div class="mb-4">
      <label for="search_input" class="sr-only">Cari pesanan</label>
      <div class="relative">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-[#706e63]">🔍</span>
        <input id="search_input" :value="searchQuery" @input="$emit('update:searchQuery', $event.target.value)"
          type="text" placeholder="Cari nama, menu, atau nomor..."
          class="w-full bg-[#181712] border border-[#3c3a30] rounded-xl pl-9 pr-4 py-2.5 text-sm text-white placeholder-[#706e63] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#d94814]" />
      </div>
    </div>

    <div class="flex space-x-2 mb-6 overflow-x-auto pb-1">
      <button v-for="tab in tabs" :key="tab" @click="$emit('update:activeTab', tab)"
        :class="['px-3 py-1.5 text-xs rounded-lg transition font-medium focus-visible:ring-2 focus-visible:ring-[#d94814]',
          activeTab === tab ? 'bg-[#d94814] text-white' : 'bg-[#181712] text-[#9e9b8f] hover:text-white border border-[#3c3a30]']">
        {{ tab }}
      </button>
    </div>

    <StateLoading v-if="loading" />
    <StateError v-else-if="error" :error-message="error" @retry="$emit('retry-fetch')" />
    <StateEmpty v-else-if="orders.length === 0" />
    <div v-else>
      <OrderItem v-for="order in orders" :key="order.id" :order="order" @delete-order="$emit('delete-order', $event)" />
    </div>
  </div>
</template>
