<template>
    <section v-if="hasUserToken" class="upload-component" :class="{ initialized: fileUploaded }">
        <input @change="uploadFile($event.target.files[0])" ref="input" accept=".csv,.xls,.xlsx,.xlsm,.xlsb" type="file"
            tabindex="-1" style="display: none;">
        <span v-show="fileUploaded" class="file-uploaded">File uploaded: <code>{{ fileName }}</code> </span>
        <button v-if="fileUploaded" @click="selectFile" class="upload-btn change">Change file</button>
        <div v-else :data-active="active" :class="{ active }" @dragenter.prevent="setActive"
            @dragover.prevent="setActive" @dragleave.prevent="setInactive" @drop.prevent="dropFile"
            aria-label="Upload a Data file" class="dropzone" tabindex="0">
            <div class="upload-icon">
                <span class="upload-icon__inner">
                    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg" color="inherit" class="upload-icon-svg">
                        <path fill="none" d="M0 0h24v24H0V0z"></path>
                        <path
                            d="M19.35 10.04A7.49 7.49 0 0012 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 000 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95A5.469 5.469 0 0112 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11A2.98 2.98 0 0122 15c0 1.65-1.35 3-3 3zM8 13h2.55v3h2.9v-3H16l-4-4z">
                        </path>
                    </svg>
                </span>
                <div class="desc-wrapper">
                    <span class="desc-l1">Drag and drop file here</span>
                    <small class="desc-l2">Limit 200MB per file • CSV only</small>
                </div>
            </div>
            <button @click="selectFile" class="upload-btn">Browse files</button>
        </div>
    </section>
</template>


<script setup>

import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useStore } from '@nanostores/vue'
import { $hasUserToken, $fileUploaded } from '../stores/store.js';

const hasUserToken = useStore($hasUserToken);
const fileUploaded = useStore($fileUploaded);

const API_URL = '/api';

const emit = defineEmits(['success']);

const active = ref(false);
const input = ref(null);

const fileName = computed(() => fileUploaded.value?.file_name || '');

function setActive(e) {
    active.value = true
}
function setInactive(e) {
    active.value = false
}

function selectFile(e) {
    input.value.click();
}

function uploadFile(file) {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    fetch(`${API_URL}/upload-file`, {
        method: 'POST',
        body: formData
    }).then(async (res) => {
        if (res.status === 200) {
            $fileUploaded.set(await res.json());
        } else {
            const data = await res.json();
            alert(data.detail || 'Something went wrong!');
        }
    });
}

function dropFile(e) {
    preventDefaults(e)
    uploadFile(e.dataTransfer.files[0]);
}

function preventDefaults(e) {
    e.preventDefault()
}

const events = ['dragenter', 'dragover', 'dragleave', 'drop']

onMounted(() => {
    events.forEach((eventName) => {
        document.body.addEventListener(eventName, preventDefaults)
    })
})

onUnmounted(() => {
    events.forEach((eventName) => {
        document.body.removeEventListener(eventName, preventDefaults)
    })
})


</script>

<style scoped>
.dropzone {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    padding: 1rem;
    background-color: rgb(38, 39, 48);
    border-radius: 0.5rem;
    color: rgb(250, 250, 250);
    transition: all 0.2s ease 0s;
}

.dropzone.active {
    transform: translateY(-0.25rem);
    border: 1px solid rgba(250, 250, 250, 0.2);
}

.upload-icon {
    margin-right: auto;
    -webkit-box-align: center;
    align-items: center;
    display: flex;
}

.upload-icon__inner {
    color: rgb(172, 177, 195);
    margin-right: 1rem;
}

.desc-wrapper {
    display: flex;
    flex-direction: column;
}

.desc-l1 {
    margin-bottom: 0.25rem;
}

.desc-l2 {
    color: rgba(250, 250, 250, 0.6);
    font-size: 14px;
    line-height: 1.25;
}

.upload-btn {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    color: inherit;
    width: auto;
    user-select: none;
    background-color: rgb(19, 23, 32);
    border: 1px solid rgba(250, 250, 250, 0.2);
}

.initialized .upload-btn {
    margin-left: auto;
    margin-right: 0;
}

.initialized {
    display: flex;
    align-items: flex-end;

}

.upload-btn:hover {
    background-color: rgb(19, 23, 32);
    border: 1px solid rgba(250, 250, 250, 0.4);
    cursor: pointer;
}

.file-uploaded {
    font-size: .7em;
}
</style>