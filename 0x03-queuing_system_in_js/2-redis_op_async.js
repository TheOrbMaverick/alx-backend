import redis from 'redis';
import {promisify } from 'util';

const client = redis.createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server')
});

client.on('error', () => {
    console.log(`Redis client not connected to the server: ${err.message}`)
})

function setNewSchool(scholName, value) {
    client.set(scholName)
}

// Convert the client.get function to return a Promise
const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(scholName) {
    try {
        const value = await getAsync(scholName);
        console.log(value)
    } catch (err) {
        console.error(err);
    }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
