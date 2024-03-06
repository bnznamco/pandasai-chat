<template>
    <div :class="computedClass" v-html="compiledHtml"></div>
</template>

<script setup>
import { computed } from "vue";
import MarkdownIt from "markdown-it";

const md = new MarkdownIt();

const props = defineProps({
    content: {
        type: String,
        required: true
    },
    type: {
        type: String,
        required: true
    },
    sender: {
        type: String,
        required: true
    }
});


const computedClass = computed(() => ({
    "chat-message": true,
    [props.sender + "-msg"]: true,
    [props.type + "-msg"]: true
}));

const compiledHtml = computed(() => {
    switch (props.type) {
        case "text":
            return props.content;
        case "markdown":
            return `${md.render(props.content)}`;
        case "image":
            return `<img class="plot-img" src="data:image/png;base64,${props.content}"/>`;
    }
});


</script>

<style>
.image-msg {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    align-items: flex-start;

    .plot-img {
        max-width: 100%;
        max-height: 100%;
        border-radius: 8px;
    }
}

.markdown-msg {
    overflow-x: auto;
    min-height: 300px;

    table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        font-size: 1.1em;

        th,
        td {
            padding: 0.5rem;
            text-align: left;
            border: rgba(var(--accent), 33%) solid 1px;
        }
    }
}
</style>