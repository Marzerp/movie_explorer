// Conectarse a la base de datos definida por la variable DATABASE
db = db.getSiblingDB("MoviesDatabase");

// Crear usuario con permisos de escritura
db.createUser({
  user: "writer",
  pwd: "writerpass",
  roles: [
    {
      role: "readWrite",
      db: "MoviesDatabase"
    }
  ]
});

// Crear usuario con permisos de solo lectura
db.createUser({
  user: "reader",
  pwd: "readerpass",
  roles: [
    {
      role: "read",
      db: "MoviesDatabase"
    }
  ]
});
