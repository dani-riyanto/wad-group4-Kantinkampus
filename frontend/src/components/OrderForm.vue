<script setup>
import { reactive, computed } from 'vue'
import { MENU_OPTIONS } from '../constants.js'

const emit = defineEmits(['create-order'])
const props = defineProps({ isSubmitting: Boolean, serverError: String })

const form = reactive({ customer_name: '', menu: MENU_OPTIONS[0].name, quantity: 1, status: 'Baru', notes: '' })
const errors = reactive({ customer_name: '', quantity: '' })

const selectedMenuPrice = computed(() => {
  const found = MENU_OPTIONS.find(m => m.name === form.menu)
  return found ? found.price : 0
})

const totalPriceFormatted = computed(() => {
  const total = selectedMenuPrice.value * form.quantity
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(total)
})

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
  const timeStr = `${String(now.getHours()).padStart(2, '0')}.${String(now.getMinutes()).padStart(2, '0')}`
  const orderData = {
    order_number: `#${Math.floor(1000 + Math.random() * 9000)}`,
    time: timeStr,
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
  <div class="bg-[#22211b] p-6 rounded-2xl border border-[#333129] text-[#f3f3f0]">
    <div class="flex items-center space-x-3 mb-6 pb-4 border-b border-[#333129]">
      <span class="w-7 h-7 rounded-full bg-[#d94814] text-white font-bold text-xs flex items-center justify-center">01</span>
      <div>
        <h3 class="font-serif text-xl text-white">Pesanan baru</h3>
        <p class="text-xs text-[#9e9b8f]">Isi detail pesanan pelanggan</p>
      </div>
    </div>

    <p v-if="serverError" class="mb-4 p-3 bg-red-950/50 border border-red-700/50 rounded-lg text-xs text-red-300">
      ⚠️ {{ serverError }}
    </p>

    <form @submit.prevent="handleSubmit" class="space-y-4" novalidate>
      <div>
        <label for="customer_name" class="block text-xs font-medium text-[#9e9b8f] mb-1">Nama pelanggan</label>
        <input id="customer_name" v-model="form.customer_name" type="text" placeholder="Contoh: Nabila Putri"
          class="w-full bg-[#181712] border border-[#3c3a30] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#d94814]" />
        <span v-if="errors.customer_name" class="text-xs text-red-400 mt-1 block">{{ errors.customer_name }}</span>
      </div>

      <div>
        <label for="menu" class="block text-xs font-medium text-[#9e9b8f] mb-1">Pilih menu</label>
        <select id="menu" v-model="form.menu"
          class="w-full bg-[#181712] border border-[#3c3a30] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#d94814]">
          <option v-for="m in MENU_OPTIONS" :key="m.name" :value="m.name">{{ m.name }} — Rp {{ m.price.toLocaleString('id-ID') }}</option>
        </select>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label for="quantity" class="block text-xs font-medium text-[#9e9b8f] mb-1">Jumlah</label>
          <div class="flex items-center bg-[#181712] border border-[#3c3a30] rounded-lg overflow-hidden">
            <button type="button" @click="form.quantity = Math.max(1, form.quantity - 1)"
              class="px-3 py-2 text-gray-400 hover:text-white focus-visible:ring-2 focus-visible:ring-[#d94814]">-</button>
            <input id="quantity" v-model.number="form.quantity" type="number" min="1"
              class="w-full bg-transparent text-center text-sm text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#d94814]" />
            <button type="button" @click="form.quantity++"
              class="px-3 py-2 text-gray-400 hover:text-white focus-visible:ring-2 focus-visible:ring-[#d94814]">+</button>
          </div>
          <span v-if="errors.quantity" class="text-xs text-red-400 mt-1 block">{{ errors.quantity }}</span>
        </div>

        <div>
          <label for="status" class="block text-xs font-medium text-[#9e9b8f] mb-1">Status</label>
          <select id="status" v-model="form.status"
            class="w-full bg-[#181712] border border-[#3c3a30] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#d94814]">
            <option value="Baru">Baru</option>
            <option value="Diproses">Diproses</option>
            <option value="Selesai">Selesai</option>
          </select>
        </div>
      </div>

      <div>
        <label for="notes" class="block text-xs font-medium text-[#9e9b8f] mb-1">Catatan</label>
        <textarea id="notes" v-model="form.notes" rows="3" placeholder="Tambahkan tingkat pedas, alergi, atau permintaan khusus..."
          class="w-full bg-[#181712] border border-[#3c3a30] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#d94814]"></textarea>
      </div>

      <div class="flex items-center justify-between pt-2">
        <span class="text-xs text-[#9e9b8f]">Total pesanan</span>
        <span class="text-lg font-bold text-white">{{ totalPriceFormatted }}</span>
      </div>

      <button type="submit" :disabled="isSubmitting"
        class="w-full bg-[#d94814] hover:bg-[#c2410c] text-white font-semibold py-3 px-4 rounded-xl transition duration-150 flex items-center justify-center space-x-2 disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-white">
        <span>+ {{ isSubmitting ? 'Menyimpan...' : 'Tambah pesanan (POST)' }}</span>
      </button>
    </form>
  </div>
</template>
