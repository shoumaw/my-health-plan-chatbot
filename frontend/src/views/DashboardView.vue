<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlans } from '@/composables/usePlans'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const router = useRouter()
const { plans, loading, error, fetchPlans } = usePlans()

onMounted(fetchPlans)

function goToChat(planId: string, planName: string) {
  router.push({ name: 'chat', params: { planId }, query: { planName } })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-2xl font-semibold text-gray-900">Your Health Plans</h1>
        <p class="mt-1 text-sm text-gray-500">Select a plan to chat with an AI benefits advisor</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <!-- Loading state -->
      <div v-if="loading" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="n in 3"
          :key="n"
          class="h-52 rounded-xl bg-gray-200 animate-pulse"
        />
      </div>

      <!-- Error state -->
      <div
        v-else-if="error"
        class="rounded-lg border border-red-200 bg-red-50 px-6 py-4 text-sm text-red-700"
      >
        {{ error }}
      </div>

      <!-- Empty state -->
      <div
        v-else-if="plans.length === 0"
        class="text-center py-16 text-gray-500 text-sm"
      >
        No health plans are currently available for your account.
      </div>

      <!-- Plan cards grid -->
      <div
        v-else
        class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
      >
        <Card
          v-for="plan in plans"
          :key="plan.id"
          class="flex flex-col"
        >
          <CardHeader>
            <div class="flex items-start justify-between gap-2">
              <CardTitle class="text-lg leading-tight">{{ plan.name }}</CardTitle>
              <Badge variant="secondary" class="shrink-0">{{ plan.plan_year }}</Badge>
            </div>
            <p class="text-xs text-muted-foreground mt-1">{{ plan.provider }}</p>
          </CardHeader>

          <CardContent class="flex-1">
            <CardDescription class="text-sm leading-relaxed line-clamp-3">
              {{ plan.description || 'No description available for this plan.' }}
            </CardDescription>
          </CardContent>

          <CardFooter>
            <Button class="w-full" @click="goToChat(plan.id, plan.name)">Chat about this plan</Button>
          </CardFooter>
        </Card>
      </div>
    </main>
  </div>
</template>
