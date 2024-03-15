<script lang="ts">
    import { account, ID } from '../lib/appwrite';

    let loggedInUser: any = null;

    async function login(email: string, password: string) {
        await account.createSession(email, password);
        loggedInUser = await account.get();
    }

    async function register(email: string, password: string) {
        await account.create(ID.unique(), email, password);
        login(email, password);
    }

    function submit(e: SubmitEvent & { currentTarget: EventTarget & HTMLFormElement }) {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const type = (e.submitter as HTMLButtonElement)?.dataset.type;
        if (type === "login") {
            login(formData.get('email') as string, formData.get('password') as string);
        } else if (type === "register") {
            register(formData.get('email') as string, formData.get('password') as string);
        }
    }

    async function logout() {
        await account.deleteSession('current');
        loggedInUser = null;
    }
</script>

<p>{loggedInUser ? `Logged in as ${loggedInUser.name}` : 'Not logged in'}</p>

<form on:submit={submit}>
    <input type="email" placeholder="Email" name="email" required />
    <input type="password" placeholder="Password" name="password" required />
    <button type="submit" data-type="login">Login</button>
    <button type="submit" data-type="register">Register</button>
</form>

<button on:click={logout}>Logout</button>