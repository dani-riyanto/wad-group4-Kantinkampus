<script setup>
import { reactive, computed } from 'vue'
import { MENU_OPTIONS, STATUS_OPTIONS } from '../constants.js'
import SectionHeading from './SectionHeading.vue'
import QuantityStepper from './QuantityStepper.vue'
import UiSelect from './UiSelect.vue'
import UiButton from './UiButton.vue'

const emit = defineEmits(['create-order'])
const props = defineProps({ isSubmitting: Boolean, serverError: String })

const form = reactive({ customer_name: '', menu: MENU_OPTIONS[0].name, quantity: 1, status: 'Baru', notes: '' })
const errors = reactive({ customer_name: '', quantity: '' })
const labelClass = 'mb-2 block text-[15px] leading-[23px] text-muted'
const fieldClass = 'w-full appearance-none border border-border bg-white px-4 py-2.5 text-base text-primary placeholder:text-muted focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary'

const menuOptions = computed(() => MENU_OPTIONS.map(m => ({ value: m.name, label: `${m.name} — Rp ${m.price.toLocaleString('id-ID')}` })))

const selectedMenuPrice = computed(() => MENU_OPTIONS.find(m => m.name === form.menu)?.price ?? 0)
const totalPriceFormatted = computed(() => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(selectedMenuPrice.value * form.quantity))

const validate = () => {
  let valid = true
  errors.customer_name = ''
  errors.quantity = ''
  if (!form.customer_name.trim()) { errors.customer_name = 'Nama pelanggan wajib diisi'; valid = false }
  if (form.quantity < 1) { errors.quantity = 'Jumlah minimal 1'; valid = false }
  return valid
}

const handleSubmit = () => {
  if (!validate()) return
  const now = new Date()
  const orderData = {
    order_number: `#${Math.floor(1000 + Math.random() * 9000)}`,
    time: `${String(now.getHours()).padStart(2, '0')}.${String(now.getMinutes()).padStart(2, '0')}`,
    customer_name: form.customer_name.trim(),
    menu: form.menu,
    quantity: form.quantity,
    total_price: selectedMenuPrice.value * form.quantity,
    status: form.status,
    notes: form.notes.trim() || 'Tanpa catatan khusus'
  }
  emit('create-order', orderData, resetForm)
}

const resetForm = () => {
  form.customer_name = ''
  form.quantity = 1
  form.notes = ''
  errors.customer_name = ''
  errors.quantity = ''
}
</script>

<template>
  <div class="border border-border bg-surface-1 p-5">
    <SectionHeading eyebrow="Formulir" title="Pesanan baru" subtitle="Isi detail pesanan pelanggan" level="h3" class="border-b border-border pb-4" />

    <p v-if="serverError" role="alert" class="mt-4 border border-danger bg-white p-3 text-[15px] leading-[23px] text-danger">{{ serverError }}</p>

    <form @submit.prevent="handleSubmit" class="mt-4 space-y-4" novalidate>
      <div>
        <label for="customer_name" :class="labelClass">Nama pelanggan</label>
        <input id="customer_name" v-model="form.customer_name" type="text" placeholder="Contoh: Nabila Putri"
          :class="fieldClass" :aria-invalid="!!errors.customer_name" />
        <span v-if="errors.customer_name" class="mt-1 block text-[15px] leading-[23px] text-danger">{{ errors.customer_name }}</span>
      </div>

      <UiSelect id="menu" v-model="form.menu" label="Pilih menu" :options="menuOptions" />

      <div class="grid grid-cols-2 gap-4">
        <QuantityStepper v-model="form.quantity" label="Jumlah" id="quantity" :error="errors.quantity" />
        <UiSelect id="status" v-model="form.status" label="Status" :options="STATUS_OPTIONS" />
      </div>

      <div>
        <label for="notes" :class="labelClass">Catatan</label>
        <textarea id="notes" v-model="form.notes" rows="3"
          placeholder="Tambahkan tingkat pedas, alergi, atau permintaan khusus..." :class="fieldClass"></textarea>
      </div>

      <div class="flex items-center justify-between border-t border-border pt-4">
        <span class="text-[15px] leading-[23px] text-muted">Total pesanan</span>
        <span class="font-serif text-xl text-primary tabular-nums">{{ totalPriceFormatted }}</span>
      </div>

      <UiButton type="submit" :disabled="isSubmitting" class="w-full">
        {{ isSubmitting ? 'Menyimpan...' : 'Tambah pesanan (POST)' }}
      </UiButton>
    </form>
  </div>
</template>
