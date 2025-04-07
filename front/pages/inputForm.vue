<template>
    <div class="container">
      <div class="left-container">
        <div class="form-container">
            <h1 class="form-title">Fill out the form:</h1>
            <div class="form">
                <UInput v-model="valueFrom" placeholder="" :ui="{ base: 'peer' }" color="neutral">
                    <label class="pointer-events-none absolute left-0 -top-2.5 text-(--ui-text-highlighted) text-xs font-medium px-1.5 transition-all peer-focus:-top-2.5 peer-focus:text-(--ui-text-highlighted) peer-focus:text-xs peer-focus:font-medium peer-placeholder-shown:text-sm peer-placeholder-shown:text-(--ui-text-dimmed) peer-placeholder-shown:top-1.5 peer-placeholder-shown:font-normal">
                    <span class="inline-flex bg-(--ui-bg) px-1">From</span>
                    </label>
                </UInput>
                <UInput v-model="valueTo" placeholder="" :ui="{ base: 'peer' }" color="neutral">
                    <label class="pointer-events-none absolute left-0 -top-2.5 text-(--ui-text-highlighted) text-xs font-medium px-1.5 transition-all peer-focus:-top-2.5 peer-focus:text-(--ui-text-highlighted) peer-focus:text-xs peer-focus:font-medium peer-placeholder-shown:text-sm peer-placeholder-shown:text-(--ui-text-dimmed) peer-placeholder-shown:top-1.5 peer-placeholder-shown:font-normal">
                    <span class="inline-flex bg-(--ui-bg) px-1">To</span>
                    </label>
                </UInput>
                <USelect v-model="valueSelectCargo" :items="cargoItems" class="w-90" />
                <UInput v-model="valueCargo" placeholder="" :ui="{ base: 'peer' }" color="neutral">
                    <label class="pointer-events-none absolute left-0 -top-2.5 text-(--ui-text-highlighted) text-xs font-medium px-1.5 transition-all peer-focus:-top-2.5 peer-focus:text-(--ui-text-highlighted) peer-focus:text-xs peer-focus:font-medium peer-placeholder-shown:text-sm peer-placeholder-shown:text-(--ui-text-dimmed) peer-placeholder-shown:top-1.5 peer-placeholder-shown:font-normal">
                    <span class="inline-flex bg-(--ui-bg) px-1">Cargo weight (kg)</span>
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
                <UButton class="centered-button" size="xl" @click="handleCalculateRoute">Calculate Route</UButton>
            </div>
        </div>
      </div>
      <div class="right-container">
        <div v-if="responseData" class="response-card">
                <div class="card-header">
                    <img :src="getTruckImage(valueSelect)" alt="Truck" class="truck-image" />
                    <div class="company-info">
                        <span class="company-name">Euro Lines</span>
                        <span class="route-info">{{ responseData.from }} > {{ responseData.to }}</span>
                    </div>
                </div>
                <div class="card-body">
                    <p><strong>Expected Arrival:</strong> {{ responseData.deadline }}</p>
                    <p><strong>Truck:</strong> {{ responseData.truck }}</p>
                    <p><strong>Cargo:</strong> {{ responseData.cargo }}</p>
                    <p><strong>Cargo Weight:</strong> {{ responseData.cargo_weight }} kg</p>
                </div>
                <div class="card-footer">
                    <span class="distance"><strong>Distance:</strong> {{ responseData.distance }}</span>
                    <span class="duration"><strong>Duration:</strong> {{ formatDuration(Number(responseData.duration)) }}</span>
                </div>
            </div>
        </div>
    </div>
  </template>
  
  <script setup lang="ts">
    import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'
    import axios from 'axios'
    import { ref, shallowRef} from 'vue'

    import truckImage1 from '../assets/img/1.png'
    import truckImage2 from '../assets/img/2.png'
    import truckImage3 from '../assets/img/3.png'
    import truckImage4 from '../assets/img/4.png'
    import truckImage5 from '../assets/img/5.png'
    

    interface RouteResponse {
    from: string;
    to: string;
    cargo_weight: number;
    deadline: string;
    truck: string;
    distance: string; 
    duration: string; 
    cargo: string
}

    const df = new DateFormatter('en-US', {
    dateStyle: 'medium'
    })

    const modelValue = shallowRef(new CalendarDate(new Date().getFullYear(), new Date().getMonth() + 1, new Date().getDate()));
    const valueFrom = ref('')
    const valueTo = ref('')
    const valueCargo = ref('')

    const items = ref<string[]>([])
    const valueSelect = ref('')
    const cargoItems = ref<string[]>([])
    const valueSelectCargo = ref('')

    const responseData = ref<RouteResponse | null>(null) 

    const fetcTrucks = async () => {
      try {
        const response = await axios.get('http://localhost:8000/trucks/')
        items.value = response.data.map((truck: {brand: string}) => truck.brand)
        if(items.value.length > 0) {
          valueSelect.value = items.value[0]
        } 
      } catch (error) {
        console.error("An error occured while fetching trucks: ", error)
      }
    }

    const fetchCargo = async () => {
      try {
        const response = await axios.get('http://localhost:8000/cargo_types/')
        cargoItems.value = response.data.map((cargo: {cargo_name: string}) => cargo.cargo_name)
        if(cargoItems.value.length > 0) {
          valueSelectCargo.value = cargoItems.value[0]
        } 
      } catch (error) {
        console.error("An error occured while fetching cargo: ", error)
      }
    }

    const handleCalculateRoute = async () => {
      const driversRoute = {
        from_location: valueFrom.value,
        to_location: valueTo.value,
        cargo_weight: valueCargo.value,
        deadline: modelValue.value.toString(),
        truck: valueSelect.value,
        cargo: valueSelectCargo.value
      }

      try {
        const response = await axios.post('http://localhost:8000/calculateRoute', driversRoute)
        responseData.value = response.data
      } catch (error) {
        responseData.value = null
        console.error("An error occured while calculating the route.")
      }
    }

    const getTruckImage = (truckBrand: string) => {
      const brandToImageMap: {[key: string]: string} = {
        'Scania': truckImage1,
        'Volvo': truckImage2,
        'Mercedes': truckImage3,
        'MAN': truckImage4,
        'Renault': truckImage5
      }
      return brandToImageMap[truckBrand] || truckImage1
    }

    const formatDuration = (seconds: number): string => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    }

    onMounted(() => {
      fetcTrucks(),
      fetchCargo()
    })
  </script>
  
 