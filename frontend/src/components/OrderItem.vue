<script setup>
const props = defineProps({
  order: { type: Object, required: true }
})
const emit = defineEmits(['delete-order'])

const statusClass = (status) => {
  if (status === 'Baru') return 'border-info/30 bg-info/10 text-info'
  if (status === 'Diproses') return 'border-warning/30 bg-warning/10 text-warning'
  return 'border-success/30 bg-success/10 text-success'
}

const handleDelete = () => {
  if (window.confirm(`Apakah Anda yakin ingin menghapus pesanan ${props.order.order_number} (${props.order.customer_name})?`)) {
    emit('delete-order', props.order.id)
  }
}

const formatPrice = (price) => {
  let val = price
  if (typeof val === 'string') val = val.replace(/\./g, '').replace(/[^0-9]/g, '')
  return Number(val || 0).toLocaleString('id-ID')
}
</script>

<template>
  <article class="border border-border bg-white p-4 lg:p-5">
    <div class="flex flex-wrap items-start justify-between gap-4">
      <div class="flex items-center gap-3">
        <span aria-hidden="true"
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-border bg-surface-2 font-serif text-base font-bold text-primary">
          {{ order.customer_name ? order.customer_name.charAt(0).toUpperCase() : '?' }}
        </span>
        <div>
          <h4 class="font-serif text-base font-bold leading-tight text-primary">{{ order.customer_name }}</h4>
          <p class="mt-1 text-[15px] leading-[23px] text-muted">{{ order.order_number }} · {{ order.time }}</p>
        </div>
      </div>
      <span :class="['shrink-0 rounded-full border px-2.5 py-0.5 text-[13px] font-semibold leading-5', statusClass(order.status)]">
        {{ order.status }}
      </span>
    </div>

    <div class="mt-4 flex flex-wrap items-start justify-between gap-4 border-t border-border pt-4">
      <div class="flex items-start gap-3">
        <span class="border border-border bg-surface-1 px-2 py-0.5 text-[15px] font-semibold text-primary tabular-nums">{{ order.quantity }}x</span>
        <div>
          <p class="font-serif text-base font-bold text-primary">{{ order.menu }}</p>
          <p class="mt-1 text-[15px] leading-[23px] italic text-muted">{{ order.notes || 'Tanpa catatan' }}</p>
        </div>
      </div>
      <p class="font-serif text-lg text-primary tabular-nums">Rp {{ formatPrice(order.total_price) }}</p>
    </div>

    <div class="mt-4 flex flex-wrap items-center justify-end gap-6 border-t border-border pt-3 text-[15px]">
      <button type="button" disabled
        class="cursor-not-allowed border-b border-muted pb-1 text-muted opacity-60">Ubah (PUT)</button>
      <button type="button" @click="handleDelete" :aria-label="`Hapus pesanan ${props.order.order_number}`"
        class="border-b border-danger pb-1 text-danger transition-colors hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-danger">
        Hapus
      </button>
    </div>
  </article>
</template>
