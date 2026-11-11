import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { connect } from 'node:net';

const bytes = await readFile(process.argv[2]);
const server = createServer((req, res) => {
  console.log(JSON.stringify({ method: req.method, target: req.url }));
  res.end();
  server.close();
});
server.listen(0, '127.0.0.1', () => {
  const socket = connect(server.address().port, '127.0.0.1', () => socket.end(bytes));
  socket.on('error', (error) => { throw error; });
});
