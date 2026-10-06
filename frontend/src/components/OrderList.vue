<script setup>
import SectionHeading from './SectionHeading.vue'
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
const tabClass = tab => props.activeTab === tab
  ? 'border border-primary bg-primary px-4 py-2 text-sm font-semibold text-white'
  : 'border border-border bg-white px-4 py-2 text-sm font-semibold text-muted transition-colors hover:border-primary hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary'
</script>

<template>
  <div>
    <SectionHeading eyebrow="Daftar Pesanan" title="Pesanan terkini" level="h3" class="mb-5" />

    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="relative w-full sm:max-w-xs">
        <label for="search_input" class="sr-only">Cari pesanan</label>
        <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
          class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted">
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-3.5-3.5" />
        </svg>
        <input id="search_input" :value="searchQuery" @input="$emit('update:searchQuery', $event.target.value)"
          type="search" placeholder="Cari nama, menu, atau nomor..."
          class="w-full appearance-none border border-border bg-white py-2.5 pl-10 pr-4 text-base text-primary placeholder:text-muted focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary" />
      </div>
      <span class="self-start rounded-full border border-border bg-surface-1 px-3 py-1 text-[13px] font-semibold text-muted">
        {{ orders.length }} pesanan
      </span>
    </div>

    <div class="mt-5 flex flex-wrap gap-2">
      <button v-for="tab in tabs" :key="tab" type="button" @click="$emit('update:activeTab', tab)"
        :aria-pressed="activeTab === tab" :class="tabClass(tab)">{{ tab }}</button>
    </div>

    <div class="mt-6" aria-live="polite">
      <StateLoading v-if="loading" />
      <StateError v-else-if="error" :error-message="error" @retry="$emit('retry-fetch')" />
      <StateEmpty v-else-if="orders.length === 0" />
      <div v-else class="space-y-4">
        <OrderItem v-for="order in orders" :key="order.id" :order="order" @delete-order="$emit('delete-order', $event)" />
      </div>
    </div>
  </div>
</template>
