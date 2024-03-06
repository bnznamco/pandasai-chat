<template>
    <div class="title" :class="{ active: !hasUserToken }">
        <img :class="{ begin: hasUserToken }" class="astro-a" :src="'/public/panda.webp'" alt="" />
        <h1>Welcome to <span class="text-gradient">PandasAi</span></h1>
    </div>
    <OpenaiTokenInput />
    <Upload />
    <Chat />
</template>

<script setup>
import Chat from './Chat.vue';
import OpenaiTokenInput from './OpenaiTokenInput.vue'
import Upload from './Upload.vue'
import { useStore } from '@nanostores/vue'
import { $hasUserToken } from '../stores/store.js';


const hasUserToken = useStore($hasUserToken);
</script>

<style>
.title {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: all 0.5s;
}

.astro-a {
    position: absolute;
    left: 50%;
    transform: translatex(-50%);
    width: 220px;
    height: auto;
    z-index: -1;
}

h1 {
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    margin-bottom: 1em;
    margin-top: 3em;
}

.text-gradient {
    background-image: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-size: 400%;
    background-position: 0%;
}

section {
    margin-bottom: .5em;
}
</style>