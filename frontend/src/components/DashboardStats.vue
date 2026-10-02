<script setup>
import { computed } from 'vue'
import SectionHeading from './SectionHeading.vue'

const props = defineProps({
  orders: { type: Array, default: () => [] }
})

const totalOrders = computed(() => props.orders.length)
const pendingOrders = computed(() => props.orders.filter(o => o.status === 'Baru' || o.status === 'Diproses').length)
const totalRevenue = computed(() => {
  const sum = props.orders.reduce((acc, curr) => {
    let raw = curr.total_price
    if (typeof raw === 'string') raw = raw.replace(/\./g, '').replace(/[^0-9]/g, '')
    return acc + (Number(raw) || 0)
  }, 0)
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(sum)
})

const stats = [
  { label: 'Total pesanan', value: totalOrders, note: 'Data tersimpan otomatis', tone: 'muted' },
  { label: 'Perlu diproses', value: pendingOrders, note: 'Segera konfirmasi', tone: 'warning' },
  { label: 'Estimasi pendapatan', value: totalRevenue, note: 'Dari semua pesanan', tone: 'muted' }
]
</script>

<template>
  <section class="border-y border-border bg-surface-1">
    <div class="container py-8 sm:py-10">
      <SectionHeading eyebrow="Ringkasan" title="Angka hari ini" level="h2" class="mb-6" />
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article v-for="stat in stats" :key="stat.label" class="border border-border bg-white p-5">
          <p class="text-[15px] leading-[23px] text-muted">{{ stat.label }}</p>
          <p class="mt-2 font-serif text-[28px] leading-[40px] tabular-nums text-primary lg:text-[34px] lg:leading-[44px]">
            {{ stat.value }}
          </p>
          <p class="mt-3 text-[15px] leading-[23px]" :class="stat.tone === 'warning' ? 'text-warning' : 'text-muted'">
            {{ stat.note }}
          </p>
        </article>
      </div>
    </div>
  </section>
</template>
