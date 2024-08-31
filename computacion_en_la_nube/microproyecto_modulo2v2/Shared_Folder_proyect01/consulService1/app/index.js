const Consul = require('consul');
const express = require('express');
const NODO = 'NODO1';
const PUERTO = process.argv[2] || 3000;
const SERVICE_NAME='mymicroservice';
const SERVICE_ID='m'+process.argv[2];
const SCHEME='http';
const HOST='192.168.100.19';
const PORT=process.argv[2]*1;
const PID = process.pid;

/* Inicializacion del server */
const app = express();
const consul = new Consul();

app.get('/health', function (req, res) {
    console.log('Health check!');
    res.end( "Ok." );
    });

app.get('/', (req, res) => {
  console.log('GET /', Date.now());
  res.setHeader('Content-Type', 'text/html');
  res.send(`
    <html>
      <body>
        <p>data: ${Math.floor(Math.random() * 8999 + 1000)}</p>
        <p>data_pid: ${PID}</p>
        <p>data_service: ${SERVICE_ID}</p>
        <p>data_host: ${HOST}</p>
        <p>data_nodo: <span style="color:purple; font-weight:bold; font-size:24px">${NODO.toUpperCase()}</span></p>
        <p>data_puerto: <span style="color:purple; font-weight:bold; font-size:24px">${PUERTO.toString().toUpperCase()}</span></p>
      </body>
    </html>
  `);
});


app.listen(PORT, function () {
    console.log('Servicio iniciado en:'+SCHEME+'://'+HOST+':'+PORT+'!');
    });

/* Registro del servicio */
var check = {
  id: SERVICE_ID,
  name: SERVICE_NAME,
  address: HOST,
  port: PORT, 
  check: {
	   http: SCHEME+'://'+HOST+':'+PORT+'/health',
	   ttl: '5s',
	   interval: '5s',
     timeout: '5s',
     deregistercriticalserviceafter: '1m'
	   }
  };
 
consul.agent.service.register(check, function(err) {
  	if (err) throw err;
  	});
