// Crear DB y usuarios personalizados
db = db.getSiblingDB('moviesdb');

db.createUser({
  user: 'usuario_app',
  pwd: 'contraseña_segura',
  roles: [{ role: 'readWrite', db: 'moviesdb' }]
});
