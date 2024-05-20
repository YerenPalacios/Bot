<script setup lang="ts">
import { onMounted } from 'vue'
import { initFlowbite } from 'flowbite'

// initialize components based on data attribute selectors
onMounted(() => {
  initFlowbite();
})
</script>

<template>


  <div class="w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <div class="sm:hidden">
      <label for="tabs" class="sr-only">Select tab</label>
      <select id="tabs"
        class="bg-gray-50 border-0 border-b border-gray-200 text-gray-900 text-sm rounded-t-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <option>Courses</option>
        <option>Processes</option>
      </select>
    </div>
    <ul
      class="hidden text-sm font-medium text-center text-gray-500 divide-x divide-gray-200 rounded-lg sm:flex dark:divide-gray-600 dark:text-gray-400 rtl:divide-x-reverse"
      id="fullWidthTab" data-tabs-toggle="#fullWidthTabContent" role="tablist">
      <li class="w-full">
        <button id="stats-tab" data-tabs-target="#stats" type="button" role="tab" aria-controls="stats"
          aria-selected="true"
          class="inline-block w-full p-4 rounded-ss-lg bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">Courses</button>
      </li>
      <li class="w-full">
        <button id="processes-tab" data-tabs-target="#processes" type="button" role="tab" aria-controls="processes"
          aria-selected="false"
          class="inline-block w-full p-4 bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">Processes</button>
      </li>
    </ul>
    <div id="fullWidthTabContent" class="border-t border-gray-200 dark:border-gray-600">
      <div class="hidden p-4 bg-white rounded-lg md:p-8 dark:bg-gray-800" id="stats" role="tabpanel"
        aria-labelledby="stats-tab">
        <dl
          class="grid max-w-screen-xl grid-cols-2 gap-8 p-4 mx-auto text-gray-900 sm:grid-cols-3 xl:grid-cols-6 dark:text-white sm:p-8">
          <div class="flex flex-col items-center justify-center">
            <dt class="mb-2 text-3xl font-extrabold">73M+</dt>
            <dd class="text-gray-500 dark:text-gray-400">Developers</dd>
          </div>
          <div class="flex flex-col items-center justify-center">
            <dt class="mb-2 text-3xl font-extrabold">100M+</dt>
            <dd class="text-gray-500 dark:text-gray-400">Public repositories</dd>
          </div>
          <div class="flex flex-col items-center justify-center">
            <dt class="mb-2 text-3xl font-extrabold">1000s</dt>
            <dd class="text-gray-500 dark:text-gray-400">Open source projects</dd>
          </div>
          <div class="flex flex-col items-center justify-center">
            <dt class="mb-2 text-3xl font-extrabold">1B+</dt>
            <dd class="text-gray-500 dark:text-gray-400">Contributors</dd>
          </div>
          <div class="flex flex-col items-center justify-center">
            <dt class="mb-2 text-3xl font-extrabold">90+</dt>
            <dd class="text-gray-500 dark:text-gray-400">Top Forbes companies</dd>
          </div>
          <div class="flex flex-col items-center justify-center">
            <dt class="mb-2 text-3xl font-extrabold">4M+</dt>
            <dd class="text-gray-500 dark:text-gray-400">Organizations</dd>
          </div>
        </dl>
      </div>
      <div class="hidden p-4 bg-white rounded-lg md:p-8 dark:bg-gray-800" id="processes" role="tabpanel"
        aria-labelledby="about-tab">
        <h2 class="mb-5 text-2xl font-extrabold tracking-tight text-gray-900 dark:text-white">We invest in the world’s
          potential</h2>
        <!-- List -->
        <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
          <li class="flex space-x-2 rtl:space-x-reverse items-center">
            <svg class="flex-shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
            </svg>
            <span class="leading-tight">Dynamic reports and dashboards</span>
          </li>
          <li class="flex space-x-2 rtl:space-x-reverse items-center">
            <svg class="flex-shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
            </svg>
            <span class="leading-tight">Templates for everyone</span>
          </li>
          <li class="flex space-x-2 rtl:space-x-reverse items-center">
            <svg class="flex-shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
            </svg>
            <span class="leading-tight">Development workflow</span>
          </li>
          <li class="flex space-x-2 rtl:space-x-reverse items-center">
            <svg class="flex-shrink-0 w-3.5 h-3.5 text-blue-600 dark:text-blue-500" aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
            </svg>
            <span class="leading-tight">Limitless business automation</span>
          </li>
        </ul>
      </div>
    </div>
  </div>

</template>
