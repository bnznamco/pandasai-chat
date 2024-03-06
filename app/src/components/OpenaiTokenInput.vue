<template>
    <section class="api-key-component">
        <span class="api-key-value" v-show="hasUserToken"> Using Api Key: 👍 </span>

        <div class="instructions" :class="{ initialized: hasUserToken }">
            <span class="clear-btn" @click="clearSession" v-show="hasUserToken"> Change Api Token </span>
            <p v-show="!hasUserToken">
                To get started, create an openai account and paste your api key in the
                input below.
            </p>
            <div v-show="!hasUserToken" class="api-token-input">
                <input @keyup.enter="sendToken" v-model="token" type="password" spellcheck="false" />
                <span @click="sendToken" class="go-btn">&rarr;</span>
            </div>
        </div>
    </section>
</template>


<script setup>
import { ref } from 'vue'

import { $fileUploaded, $hasUserToken } from '../stores/store.js';
import { useStore } from '@nanostores/vue';

const API_URL = '/api';

const emit = defineEmits(['success']);

const token = ref('');
const hasUserToken = useStore($hasUserToken);

function clearSession() {
    fetch(`${API_URL}/clear-session`, {
        method: 'POST'
    }).then(async (res) => {
        if (res.status === 200) {
            $hasUserToken.set(false);
            $fileUploaded.set(null);
            emit('success', false);
        } else {
            const data = await res.json();
            alert(data.detail || 'Something went wrong!');
        }
    });
}

function sendToken() {
    fetch(`${API_URL}/set-openai-token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: token.value })
    }).then(async (res) => {
        if (res.status === 200) {
            emit('success', true);
            $hasUserToken.set(true);
        } else {
            const data = await res.json();
            $hasUserToken.set(false);
            emit('success', false);
            alert(data.detail || 'Something went wrong!');
        }
    });
}
</script>

<style scoped>
.api-key-component {
    display: flex;
    align-items: center;
}

.api-key-value {
    font-size: .7em;
    margin-right: 0.5em;
}

.instructions {
    margin-bottom: 2rem;
    border: 1px solid rgba(var(--accent-light), 25%);
    background: linear-gradient(rgba(var(--accent-dark), 66%),
            rgba(var(--accent-dark), 33%));
    padding: 1.5rem;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.instructions.initialized {
    width: 180px;
    font-size: .7em;
    padding: 0.2em;
    margin: auto 0 auto auto;
}

.api-token-input {
    display: flex;
    width: 72%;

    .go-btn {
        display: flex;
        align-items: center;
        border: 1px solid rgba(var(--accent-light), 25%);
        border-radius: 5px;
        padding: 0 1em;
        margin-left: 0.2em;

        &:hover {
            cursor: pointer;
            background: linear-gradient(rgba(var(--accent-dark), 66%),
                    rgba(var(--accent-dark), 33%));
        }
    }

    input {
        outline: none;
        width: 100%;
        height: 32px;
        margin: auto;
        background: linear-gradient(rgba(var(--accent-light), 66%),
                rgba(var(--accent-light), 33%));
        border: 1px solid rgba(var(--accent-dark), 25%);
        border-radius: 5px;
        color: rgb(var(--accent-dark));
        font-family: monospace;
        font-size: 1em;
        font-weight: 300;
    }

    input::placeholder {
        color: rgba(var(--accent-dark), 90%);
    }
}

.instructions code {
    font-size: 0.8em;
    font-weight: bold;
    background: rgba(var(--accent-light), 12%);
    color: rgb(var(--accent-light));
    border-radius: 4px;
    padding: 0.3em 0.4em;
}

.instructions strong {
    color: rgb(var(--accent-light));
}

.clear-btn {
    cursor: pointer;
}
</style>