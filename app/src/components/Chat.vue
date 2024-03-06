<template>
    <section v-show="fileUploaded" class="chat">
        <div class="chat-body">
            <div ref="chat" class="chat-messages">
                <ChatMessage v-for="(message, i) in messages" :key="i" :sender="message.from"
                    :content="message.data.content" :type="message.data.type" />
                <div class="chat-message bot-msg loading-msg" v-show="loading">
                    <DotFlashing />
                </div>

            </div>
            <div class="chat-input">
                <input :disabled="loading" v-model="question" @keyup.enter="sendMessage" type="text"
                    placeholder="Type a message..." />
                <span @click="sendMessage" class="go-btn">&rarr;</span>
            </div>
        </div>
    </section>
</template>


<script setup>
import ChatMessage from './ChatMessage.vue';
import DotFlashing from './DotFlashing.vue';
import { ref, nextTick, watch } from 'vue'
import { useStore } from '@nanostores/vue'
import { $fileUploaded } from '../stores/store.js';

const fileUploaded = useStore($fileUploaded);

const question = ref('');

const loading = ref(false);

const chat = ref(null);

const messages = ref([]);

watch(fileUploaded, async (val) => {
    messages.value = [{
        data: { content: `Hi there! Ask me anything about "${val.file_name}"!`, type: 'text' },
        from: 'bot'
    }]
})

async function scrollToBottom() {
    await nextTick();
    chat.value.scrollTop = chat.value.scrollHeight;
}

async function sendMessage() {
    if (loading.value) return;
    if (!question.value) return;
    messages.value.push({
        data: {
            type: 'text',
            content: question.value
        },
        from: 'user'
    });
    loading.value = true;
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: question.value })
    }).then(async (res) => {
        const data = await res.json();
        messages.value.push({
            data,
            from: 'bot'
        });
        loading.value = false;
        scrollToBottom()
    });
    question.value = '';
    scrollToBottom()
}

</script>



<style>
.chat-messages {
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    overflow-y: auto;
    max-height: 300px;
    height: 300px;
    background: linear-gradient(rgba(var(--accent-dark), 11%),
            rgba(var(--accent-dark), 1%));
    border: 1px solid rgba(var(--accent-light), 25%);

}

.chat-input {
    margin-top: 1em;
    display: flex;

    input {
        outline: none;
        width: 100%;
        height: 32px;
        margin: auto;
        background: linear-gradient(rgba(var(--accent-dark), 66%),
                rgba(var(--accent-dark), 33%));
        border-radius: 5px;
        color: rgb(var(--accent-light));
        font-size: .7em;
        font-weight: 300;
        border: 1px solid rgba(var(--accent-light), 25%);
        padding: 0 0.5em;
    }

    input::placeholder {
        color: rgba(var(--accent-light), 50%);
    }

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

}

.chat-message {
    padding: 1rem;
    border-radius: 8px;
    max-width: 70%;
    font-size: .7em;
    max-height: 700px;
    color: rgba(var(--accent-light), 80%);

}

.user-msg {
    align-self: flex-end;
    background: linear-gradient(rgba(var(--accent), 66%),
            rgba(var(--accent), 33%));
}

.bot-msg {
    align-self: flex-start;
    background: linear-gradient(rgba(var(--accent-dark), 66%),
            rgba(var(--accent-dark), 33%));
}

.loading-msg {
    width: 100px;
    display: flex;
    justify-content: center;
}
</style>