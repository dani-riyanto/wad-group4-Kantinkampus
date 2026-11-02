<script setup>
import { reactive, computed, ref, onMounted } from 'vue'
import SectionHeading from './SectionHeading.vue'
import QuantityStepper from './QuantityStepper.vue'
import UiSelect from './UiSelect.vue'
import UiButton from './UiButton.vue'
import { fetchMenus } from '../services/api.js'

const emit = defineEmits(['create-order'])
const props = defineProps({ isSubmitting: Boolean, serverError: String })

// 1. State untuk menyimpan menu dari database
const daftarMenu = ref([])

// 2. Mengambil data dari backend saat komponen dimuat
onMounted(async () => {
  try {
    const data = await fetchMenus()
    daftarMenu.value = data
    
    // Set pilihan default ke menu pertama jika datanya ada
    if (daftarMenu.value.length > 0) {
      form.menu_id = daftarMenu.value[0].id
    }
  } catch (error) {
    console.error("Gagal mengambil data menu dari database:", error)
  }
})

// Ubah form.menu menjadi form.menu_id (karena kita mengirim ID, bukan string nama menu)
const form = reactive({ customer_name: '', menu_id: '', quantity: 1, notes: '' })
const errors = reactive({ customer_name: '', quantity: '' })

const labelClass = 'mb-2 block text-[15px] leading-[23px] text-muted'
const fieldClass = 'w-full appearance-none border border-border bg-white px-4 py-2.5 text-base text-primary placeholder:text-muted focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary'

// 3. Mengubah list menu dari database menjadi format { value, label } untuk komponen UiSelect
const menuOptions = computed(() => {
  return daftarMenu.value.map(m => ({
    value: m.id, 
    label: `${m.nama} — Rp ${m.harga.toLocaleString('id-ID')}`
  }))
})

// 4. Mencari harga berdasarkan ID menu yang dipilih dari database
const selectedMenuPrice = computed(() => {
  // Gunakan '==' (dua sama dengan) agar angka dan teks bisa dicocokkan
  const selected = daftarMenu.value.find(m => m.id == form.menu_id)
  return selected ? selected.harga : 0
})
const totalPriceFormatted = computed(() => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(selectedMenuPrice.value * form.quantity))

const validate = () => {
  let valid = true
  errors.customer_name = ''
  errors.quantity = ''
  
  if (!form.customer_name.trim()) { errors.customer_name = 'Nama pelanggan wajib diisi'; valid = false }
  if (form.quantity < 1) { errors.quantity = 'Jumlah minimal 1'; valid = false }
  
  // pengecekan harga
  if (!form.menu_id || selectedMenuPrice.value <= 0) { 
    alert('Pilih menu terlebih dahulu!'); 
    valid = false 
  }
  return valid
}

const handleSubmit = () => {
  if (!validate()) return
  
  const orderData = {
    customer_name: form.customer_name.trim(),
    menu_item_id: form.menu_id, 
    quantity: form.quantity,
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
  // Kembalikan pilihan menu ke default (menu pertama)
  if (daftarMenu.value.length > 0) {
    form.menu_id = daftarMenu.value[0].id
  }
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

      <!-- Perhatikan perubahan v-model menjadi form.menu_id -->
      <UiSelect id="menu" v-model="form.menu_id" label="Pilih menu" :options="menuOptions" />

      <QuantityStepper v-model="form.quantity" label="Jumlah" id="quantity" :error="errors.quantity" />

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