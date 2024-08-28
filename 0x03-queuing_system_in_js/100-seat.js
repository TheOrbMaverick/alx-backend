import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';
import express from 'express';

const client = redis.createClient();
const reserveSeat = (number) => client.set('available_seats', number);
const getCurrentAvailableSeats = promisify(client.get).bind(client);

reserveSeat(50);
let reservationEnabled = true;

const queue = kue.createQueue();

const app = express();
const PORT = 1245;

app.get('/available_seats', async (req, res) => {
    const seats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: "Reservation are blocked" });
    }
    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: "Reservation failed" });
        }
        res.json({ status: "Reservation in process" });
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err}`);
    });
});

app.get('/process', (req, res) => {
    res.json({ status: "Queue processing" });

    queue.process('reserve_seat', async (job, done) => {
        const availableSeats = await getCurrentAvailableSeats();
        const seatsLeft = parseInt(availableSeats, 10) - 1;

        if (seatsLeft >= 0) {
            reserveSeat(seatsLeft);
            if (seatsLeft === 0) reservationEnabled = false;
            done();
        } else {
            done(new Error("Not enough seats available"));
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
