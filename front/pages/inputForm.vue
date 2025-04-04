<template>
    <div class="container">
      <div class="left-container">
        <div class="form-container">
            <h1 class="form-title">Fill out the form:</h1>
            <div class="form">
                <UInput v-model="value" placeholder="" :ui="{ base: 'peer' }" color="neutral">
                    <label class="pointer-events-none absolute left-0 -top-2.5 text-(--ui-text-highlighted) text-xs font-medium px-1.5 transition-all peer-focus:-top-2.5 peer-focus:text-(--ui-text-highlighted) peer-focus:text-xs peer-focus:font-medium peer-placeholder-shown:text-sm peer-placeholder-shown:text-(--ui-text-dimmed) peer-placeholder-shown:top-1.5 peer-placeholder-shown:font-normal">
                    <span class="inline-flex bg-(--ui-bg) px-1">From</span>
                    </label>
                </UInput>
                <UInput v-model="value" placeholder="" :ui="{ base: 'peer' }" color="neutral">
                    <label class="pointer-events-none absolute left-0 -top-2.5 text-(--ui-text-highlighted) text-xs font-medium px-1.5 transition-all peer-focus:-top-2.5 peer-focus:text-(--ui-text-highlighted) peer-focus:text-xs peer-focus:font-medium peer-placeholder-shown:text-sm peer-placeholder-shown:text-(--ui-text-dimmed) peer-placeholder-shown:top-1.5 peer-placeholder-shown:font-normal">
                    <span class="inline-flex bg-(--ui-bg) px-1">To</span>
                    </label>
                </UInput>
                <UInput v-model="value" placeholder="" :ui="{ base: 'peer' }" color="neutral">
                    <label class="pointer-events-none absolute left-0 -top-2.5 text-(--ui-text-highlighted) text-xs font-medium px-1.5 transition-all peer-focus:-top-2.5 peer-focus:text-(--ui-text-highlighted) peer-focus:text-xs peer-focus:font-medium peer-placeholder-shown:text-sm peer-placeholder-shown:text-(--ui-text-dimmed) peer-placeholder-shown:top-1.5 peer-placeholder-shown:font-normal">
                    <span class="inline-flex bg-(--ui-bg) px-1">Cargo weight</span>
                    </label>
                </UInput>
                <UPopover>
                    <UButton color="neutral" variant="subtle" icon="i-lucide-calendar">
                    {{ modelValue ? df.format(modelValue.toDate(getLocalTimeZone())) : 'Select a date' }}
                    </UButton>

                    <template #content>
                    <UCalendar v-model="modelValue" class="p-2" />
                    </template>
                </UPopover>
                <USelect v-model="valueSelect" :items="items" class="w-90" />
                <UButton class="centered-button" size="xl">Calculate Route</UButton>
            </div>
        </div>
      </div>
      <div class="right-container">

      </div>
    </div>
  </template>
  
  <script setup lang="ts">
    import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'

    const df = new DateFormatter('en-US', {
    dateStyle: 'medium'
    })

    const modelValue = shallowRef(new CalendarDate(2022, 1, 10))
    const value = ref('')

    const items = ref(['Scania', 'Volvo', 'Mercedes', 'Man', 'Renault'])
    const valueSelect = ref('Volvo')
  </script>
  
 