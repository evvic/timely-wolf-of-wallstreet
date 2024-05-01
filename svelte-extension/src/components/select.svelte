<script lang="js">
// @ts-nocheck

    import * as Select from "$lib/components/ui/select/index.js";

    import { onMount, onDestroy } from 'svelte';
   
    const time_windows = [
        { value: "12", label: "3 months" },
        { value: "26", label: "6 months" },
        { value: "52", label: "1 year" }
    ];

    let cnt = 0;
    let label = undefined;

    export let window = undefined;

    $: window = window;

    onMount(() => {
        chrome.storage.local.get(["selector_label"], (data) => {
            const lbl = data["selector_label"];
            label     = lbl ? lbl : label;
        });

    })

    /*
     * time_window is an object of { value, label }
     */
    function handleClick(time_window) {
        cnt++;

        chrome.storage.local.set({ num_weeks: time_window.value });
        chrome.storage.local.set({ selector_label: time_window.label });

        window = time_window.value;
        label = time_window.label;
    }

</script>

<Select.Root portal={null}>
    <Select.Trigger class="w-[150px]">
        <!-- <Select.Value placeholder="Select a time window" /> -->
        <Select.Value placeholder={label === undefined ? "Select a time window" : `${label}`} />
    </Select.Trigger>   
    <Select.Content>
        <Select.Group>
            <Select.Label>Time windows</Select.Label>
            {#each time_windows as time_window}
            <Select.Item value={time_window.value} label={time_window.label} on:click={() => handleClick(time_window)}>
                {time_window.label}
            </Select.Item>
            {/each}
        </Select.Group>
    </Select.Content>
    <Select.Input name="time_windows" bind:value={window} placeholder={label}/>
</Select.Root>
