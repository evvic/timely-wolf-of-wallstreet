import adapter from "@sveltejs/adapter-node";
import { svelte, vitePreprocess } from "@sveltejs/vite-plugin-svelte";

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: [vitePreprocess({})],

  kit: {
    adapter: adapter()
  }
};
