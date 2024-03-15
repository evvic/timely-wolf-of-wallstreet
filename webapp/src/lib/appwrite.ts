import { Client, Account, ID } from 'appwrite';

const client = new Client();
client
  .setEndpoint('https://cloud.appwrite.io/v1')
  .setProject('market-hunters-dev');

export const account = new Account(client);
export { ID };