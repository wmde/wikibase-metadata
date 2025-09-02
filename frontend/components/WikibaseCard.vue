<script setup lang="ts">
import { computed } from "vue";
import { CdxCard } from "@wikimedia/codex";
import { Wikibase } from "../types";

const props = defineProps<{ w: Wikibase }>();

const showTotals = computed(() => props.w.hasQuantity());
const showRc = computed(() => props.w.hasRecentChanges());
</script>

<template>
  <CdxCard class="flex flex-col h-full">
    <template #title>
      <a
        :href="props.w.urls?.baseUrl"
        target="_blank"
        rel="noreferrer noopener"
        class="text-indigo-600 underline hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
      >
        {{ props.w.baseHost() || "Unknown" }}
      </a>
    </template>
    <template #description> </template>
    <template #supporting-text>
      <div class="flex flex-col h-full">
        <div>
          <p
            v-if="props.w.timeToFirstValueObservations?.mostRecent?.initiationDate"
            class="text-xs text-black"
          >
            Online since:
            {{ props.w.fmtDate(props.w.timeToFirstValueObservations?.mostRecent?.initiationDate) }}
          </p>
          <p v-if="props.w.description" class="mt-1 text-sm text-black">
            {{ props.w.description }}
          </p>
        </div>
        <div class="mt-auto space-y-2">
          <div v-if="showTotals">
            <p class="mb-1 text-[10px] font-semibold uppercase tracking-wide text-black">
              Totals{{ props.w.obsHeadlineSuffix('quantity') }}
            </p>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div v-if="props.w.quantityObservations?.mostRecent?.totalItems">
                <p class="text-black">Items</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.quantityObservations?.mostRecent?.totalItems) }}</p>
              </div>
              <div v-if="props.w.quantityObservations?.mostRecent?.totalProperties">
                <p class="text-black">Properties</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.quantityObservations?.mostRecent?.totalProperties) }}</p>
              </div>
              <div v-if="props.w.quantityObservations?.mostRecent?.totalLexemes">
                <p class="text-black">Lexemes</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.quantityObservations?.mostRecent?.totalLexemes) }}</p>
              </div>
              <div v-if="props.w.quantityObservations?.mostRecent?.totalTriples">
                <p class="text-black">Triples</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.quantityObservations?.mostRecent?.totalTriples) }}</p>
              </div>
            </div>
          </div>

          <div v-if="showRc">
            <p class="mb-1 text-[10px] font-semibold uppercase tracking-wide text-black">
              Recent changes (last 30 days){{ props.w.obsHeadlineSuffix('rc') }}
            </p>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div v-if="props.w.recentChangesObservations?.mostRecent?.humanChangeCount">
                <p class="text-black">Human changes</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.recentChangesObservations?.mostRecent?.humanChangeCount) }}</p>
              </div>
              <div v-if="props.w.recentChangesObservations?.mostRecent?.humanChangeUserCount">
                <p class="text-black">Human users</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.recentChangesObservations?.mostRecent?.humanChangeUserCount) }}</p>
              </div>
              <div v-if="props.w.recentChangesObservations?.mostRecent?.botChangeCount">
                <p class="text-black">Bot changes</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.recentChangesObservations?.mostRecent?.botChangeCount) }}</p>
              </div>
              <div v-if="props.w.recentChangesObservations?.mostRecent?.botChangeUserCount">
                <p class="text-black">Bot users</p>
                <p class="font-semibold text-base">{{ props.w.fmt(props.w.recentChangesObservations?.mostRecent?.botChangeUserCount) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </CdxCard>
  
</template>

<style scoped></style>
