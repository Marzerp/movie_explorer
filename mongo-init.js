// Obtener variables de entorno
const dbName = process.env.MONGO_APP_DB;
const username = process.env.MONGO_APP_USER;
const password = process.env.MONGO_APP_PASSWORD;

// Crear DB 
print("*** INICIO mongo-init.js ***");
db = db.getSiblingDB(dbName);

// Crear usuario y password de acceso a dbName
db.createUser({
  user: username,
  pwd: password,
  roles: [{ role: 'readWrite', db: dbName},
          { role: 'dbAdmin', db: dbName}
         ]          
});

print("*** FIN mongo-init.js ***");

