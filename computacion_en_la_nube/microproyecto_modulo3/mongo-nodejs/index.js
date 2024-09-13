import express from 'express'
import mongoose from 'mongoose'
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);



const Animal = mongoose.model('Animal', new mongoose.Schema({
  tipo: String,
  estado: String,
}))

const app = express()

mongoose.connect('mongodb://nico:password@mongo-service:27017/miapp?authSource=admin')
app.use(express.json())
app.use(express.urlencoded({extended:false}))

app.get('/', async (_req, res) => {
  console.log('listando... animales...')
  const animales = await Animal.find();
  return res.send(animales)
})

// Lista de animales
const animales = ['Gato', 'Perro', 'Chanchito', 'Pajaro', 'Aguila'];

// Lista de estados
const estados = ['Feliz', 'Triste', 'Enojado', 'Cansado', 'Sorprendido'];


app.get('/crear', async (_req, res) => { 
  //console.log('creando...')
 // const animalAleatorio = animales[Math.floor(Math.random() * animales.length)];
 // const estadoAleatorio = estados[Math.floor(Math.random() * estados.length)];
 // await Animal.create({ tipo: animalAleatorio, estado: estadoAleatorio })
  return res.sendFile(path.join(__dirname, 'prueba.html'));
})

app.post('/crear', async (_req, res) => {
  console.log('creando animal con un estado...')
  //console.log(_req.body.animal)


  //const animalAleatorio = animales[Math.floor(Math.random() * animales.length)];
  //const estadoAleatorio = estados[Math.floor(Math.random() * estados.length)];
  await Animal.create({ tipo: _req.body.animal, estado: _req.body.estado })
  return res.send('El animal ha sido creado')
})


app.listen(3000, () => console.log('listening...'))
