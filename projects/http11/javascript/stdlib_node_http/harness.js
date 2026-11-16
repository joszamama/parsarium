"use strict";
const http = require("node:http");
const net = require("node:net");

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) return null;
  return await new Promise((resolve, reject) => {
    const server = http.createServer((request, response) => {
      const result = { method: request.method, target: request.url };
      response.end();
      finish(result);
    });
    let client;
    let timer;
    let done = false;
    function finish(value) {
      if (done) return;
      done = true;
      clearTimeout(timer);
      client?.destroy();
      server.close();
      resolve(value);
    }
    server.on("clientError", (_error, socket) => {
      socket.destroy();
      finish(null);
    });
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => {
      client = net.connect(server.address().port, "127.0.0.1", () => client.end(data));
      client.on("error", () => finish(null));
      timer = setTimeout(() => finish(null), 1000);
    });
  });
}

module.exports = { parseData };
